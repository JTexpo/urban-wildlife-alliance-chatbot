'''
a dependency inversion for s3 vectors
'''

import os
import boto3

S3_VECTOR_INDEX_ARN = os.environ["S3_VECTOR_INDEX_ARN"]

def get_vector_client() -> boto3.client:
    """
    Get an S3 client.

    Returns:
    boto3.client: The S3 vector client.
    """
    return boto3.client("s3vectors")

def s3_vector_query(client, index_arn:str, vector:list[float])->dict:
    """
    Query the S3 vector index.

    Parameters:
    client (boto3.client): The S3 vector client.
    index_arn (str): The ARN of the S3 vector index.
    vector (list[float]): The vector to query.

    Returns:
    dict: The response of the query operation.
    """
    return client.query_vectors(
        indexArn=index_arn,
        queryVector={"float32": vector},
        topK=1
    )