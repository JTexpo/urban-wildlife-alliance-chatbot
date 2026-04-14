"""
A post endpoint to converse with the chatbot
"""

from fastapi import APIRouter

from chatbot_api.models import ChatbotRequest, ChatbotResponse
from chatbot_api.aws.bedrock_runtime import (
    get_bedrock_runtime_client,
    bedrock_converse,
    titan_embed,
    STOP_REASON_END_TURN,
    STOP_REASON_TOOL_USED,
)
from chatbot_api.aws.s3 import get_s3_bucket, bucket_get_file, RAG_INFO_BUCKET_NAME
from chatbot_api.aws.s3vectors import get_vector_client, s3_vector_query, S3_VECTOR_INDEX_ARN

AI_MAX_CONVERSATION_COUNT = 3
TOOL_CONFIG = [
    {
        "toolSpec": {
            "name": "get_wildlife_guide",
            "description": "Search the wildlife guide for species advice",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "The question to search a RAG model for wildlife advice",
                        }
                    },
                    "required": ["question"],
                }
            },
        }
    }
]

_EXAMPLE_API_INPUT = {
    "message": "what did you mean by that?",
    "conversation_history": [
        {"role": "user", "content": [{"text": "who are you?"}]},
        {"role": "assistant", "content": [{"text": "I am a chatbot"}]}
    ]
}


def get_wildlife_guide(question:str) -> str:
    vector_client = get_vector_client()
    bedrock_client = get_bedrock_runtime_client()
    s3_bucket = get_s3_bucket(RAG_INFO_BUCKET_NAME)
    embedings = titan_embed(bedrock_client, question)
    vector = s3_vector_query(vector_client, S3_VECTOR_INDEX_ARN, embedings)
    s3_bucket_key = vector["vectors"][0]["key"]
    return bucket_get_file(s3_bucket, s3_bucket_key).read().decode("utf-8")

router = APIRouter()


@router.post("")
async def chatbot(chatbot_request: ChatbotRequest) -> ChatbotResponse:

    # # Getting dependencies
    bedrock_runtime_client = get_bedrock_runtime_client()

    # # Getting conversation history
    conversation = chatbot_request.model_dump()["conversation_history"]
    conversation.append(
        {"role": "user", "content": [{"text": chatbot_request.message}]}
    )

    # # Converse
    # # NOTE - we set range to a max count, as we don't want the AI to get stuck in a loop
    for _ in range(AI_MAX_CONVERSATION_COUNT):

        chatbot_response = bedrock_converse(
            bedrock_runtime_client=bedrock_runtime_client,
            conversation=conversation,
            tools=TOOL_CONFIG,
        )
        print(chatbot_response["stopReason"])
        if chatbot_response["stopReason"] == STOP_REASON_END_TURN:
            break
        elif chatbot_response["stopReason"] == "tool_use":
            print(chatbot_response["output"]["message"]["content"][1])
            tool_use = chatbot_response["output"]["message"]["content"][1]["toolUse"]
            tool_id = tool_use["toolUseId"]
            tool_name = tool_use["name"]
            tool_inputs = tool_use["input"]

            if tool_name == "get_wildlife_guide":
                print(tool_inputs)
                result = get_wildlife_guide(
                    question=tool_inputs["question"]
                )
            else:
                result = "Tool not found"

            conversation.append(chatbot_response["output"]["message"])

            conversation.append(
                {
                    "role": "user",
                    "content": [
                        {
                            "toolResult": {
                                "toolUseId": tool_id,
                                "content": [{"text": result}],
                            }
                        }
                    ],
                }
            )
    else:
        return ChatbotResponse(
            message=f"unexpected stop reason {chatbot_response['stopReason']}"
        )
    return ChatbotResponse(
        message=chatbot_response["output"]["message"]["content"][-1]["text"]
    )
