'''
A post endpoint to converse with the chatbot
'''

from fastapi import APIRouter

from chatbot_api.models import ChatbotRequest, ChatbotResponse
from chatbot_api.aws.bedrock_runtime import get_bedrock_runtime_client,bedrock_converse, STOP_REASON_END_TURN, STOP_REASON_TOOL_USED
from chatbot_api.aws.s3 import get_s3_bucket, bucket_get_file, RAG_BUCKET_NAME

AI_MAX_CONVERSATION_COUNT = 3

router = APIRouter()

@router.post("")
async def chatbot(chatbot_request: ChatbotRequest) -> ChatbotResponse:

    # # Getting dependencies
    # bucket = get_s3_bucket(bucket_name=RAG_BUCKET_NAME)
    # bedrock_runtime_client = get_bedrock_runtime_client()

    # # Getting conversation history
    # conversation:list[dict] = chatbot_request.conversation_history
    # conversation.append({"role": "user", "content": chatbot_request.message})
    
    # # Getting tools
    # tool_config = [] # todo get tools

    # # Converse
    # # NOTE - we set range to a max count, as we don't want the AI to get stuck in a loop
    # for _ in range(AI_MAX_CONVERSATION_COUNT):

    #     chatbot_response = bedrock_converse(
    #         bedrock_runtime_client=bedrock_runtime_client, 
    #         conversation=conversation, 
    #         tools=tool_config
    #     )

    #     if chatbot_response["stopReason"] == STOP_REASON_END_TURN:
    #         break
    #     elif chatbot_response["stopReason"] == STOP_REASON_TOOL_USED:
    #         # todo, execute tool here & update conversation
    #         pass
    #     else:
    #         return ChatbotResponse(message=f"unexpected stop reason {chatbot_response['stopReason']}")

    # return ChatbotResponse(message=chatbot_response["output"]["message"]["content"]["text"])

    return ChatbotResponse(message=chatbot_request.message)