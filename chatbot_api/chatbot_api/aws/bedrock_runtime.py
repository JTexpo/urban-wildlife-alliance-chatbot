'''
a dependency inversion for bedrock runtime
'''
import boto3

MODEL_ID = "amazon.nova-micro-v1:0"

STOP_REASON_END_TURN = "end_turn"
STOP_REASON_TOOL_USED = "toolUse"

def get_bedrock_runtime_client() -> boto3.client:
    """
    Get a bedrock runtime client.

    Returns:
    boto3.client: The bedrock runtime client.
    """
    return boto3.client('bedrock-runtime')

def bedrock_converse(bedrock_runtime_client, conversation, tools) -> dict:
    # good reference: https://how.wtf/a-step-by-step-guide-on-how-to-use-the-amazon-bedrock-converse-api.html
    """
    Converse a conversation given a bedrock runtime client, conversation, and tools.
    
    Parameters:
    bedrock_runtime_client (boto3.client): The bedrock runtime client.
    conversation (list[str]): The conversation to converse.
    tools (list[str]): The tools to use for the conversation.
    
    Returns:
    dict: The response of the converse operation.
    """
    return bedrock_runtime_client.converse(
        modelId=MODEL_ID,
        messages=conversation,
        toolConfig={
            "tools":tools
        },
        inferenceConfig={"maxTokens": 512, "temperature": 0.1, "topP": 0.9},
    )