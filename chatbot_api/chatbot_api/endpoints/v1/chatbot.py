'''
A post endpoint to converse with the chatbot
'''

from fastapi import APIRouter

from chatbot_api.models import ChatbotRequest, ChatbotResponse
from chatbot_api.aws.bedrock_runtime import get_bedrock_runtime_client,bedrock_converse, STOP_REASON_END_TURN, STOP_REASON_TOOL_USED
from chatbot_api.aws.s3 import get_s3_bucket, bucket_get_file, RAG_BUCKET_NAME

AI_MAX_CONVERSATION_COUNT = 3
def get_wildlife_guide(species: str, situation: str) -> str:
    guidance = {
        "bat": "Do not handle bare handed. Wear gloves.",
    }
    return guidance.get(species.lower(), f"For {species} please contact your local wildlife rehabilitator.")

router = APIRouter()

@router.post("")
async def chatbot(chatbot_request: ChatbotRequest) -> ChatbotResponse:

    # # Getting dependencies
     bucket = get_s3_bucket(bucket_name=RAG_BUCKET_NAME)
     bedrock_runtime_client = get_bedrock_runtime_client()

    # # Getting conversation history
     conversation: list[dict] = [
    {
        "role": c.role,
        "content": [{"text": c.content}]
    }
    for c in chatbot_request.conversation_history
]
     conversation.append({"role": "user", "content": [{"text": chatbot_request.message}]}) #list no string
    
    # # Getting tools
     tool_config = [
         {
            "toolSpec": {
                "name": "get_wildlife_guide",
                "description": "Search the wildlife guide for species advice",
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "species": {
                                "type": "string",
                                "description": "The specific animal species"
                        },
                        "situation": {
                                "type": "string",
                                "description": "The situation that is going on"
                        }
                    },
                    "required": ["species", "situation"]
                }
            }
        }
    }
]

    # # Converse
    # # NOTE - we set range to a max count, as we don't want the AI to get stuck in a loop
     for _ in range(AI_MAX_CONVERSATION_COUNT):

        chatbot_response = bedrock_converse(
             bedrock_runtime_client=bedrock_runtime_client, 
             conversation=conversation, 
             tools=tool_config
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
                result = get_wildlife_guide(
                species = tool_inputs["species"],
                situation = tool_inputs["situation"]
            )
            else: 
                result = "Tool not found"

            conversation.append(chatbot_response["output"]["message"])
        
            conversation.append({
             "role": "user",
             "content": [
                 {
                     "toolResult": {
                         "toolUseId": tool_id,
                         "content": [{"text": result}]
                     }
                 }
            ]
         })
     else:
        return ChatbotResponse(message=f"unexpected stop reason {chatbot_response['stopReason']}")
     return ChatbotResponse(message=chatbot_response["output"]["message"]["content"][-1]["text"])

