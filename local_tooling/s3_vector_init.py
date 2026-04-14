import os
import json
from pathlib import Path

import boto3

from dotenv import load_dotenv

load_dotenv("local_tooling/.env")

S3_VECTOR_INDEX_ARN = os.environ["S3_VECTOR_INDEX_ARN"]
INFO_DIR = Path(os.environ["INFO_DIR"])

"""
S3 VECTOR
---------
"""


def get_vector_client() -> boto3.client:
    """
    Get an S3 client.

    Returns:
    boto3.client: The S3 vector client.
    """
    return boto3.client("s3vectors")


def s3_vector_put_vector(s3_client, index_arn, file_name, vector, meta):
    return s3_client.put_vectors(
        indexArn=index_arn,
        vectors=[{"key": file_name, "data": {"float32": vector}, "metadata": meta}],
    )


""" 
TITAN
-----
"""


def get_bedrock_runtime_client() -> boto3.client:
    """
    Get a bedrock runtime client.

    Returns:
    boto3.client: The bedrock runtime client.
    """
    return boto3.client("bedrock-runtime")


def titan_embed(bedrock, text):
    return json.loads(bedrock.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        contentType="application/json",
        accept="application/json",
        body=json.dumps({"inputText": text}),
    )["body"].read())["embedding"]


"""
MAIN
----
"""


def main():
    bedrock = get_bedrock_runtime_client()
    s3_vector_client = get_vector_client()

    if not INFO_DIR.exists():
        raise FileNotFoundError(f"{INFO_DIR} does not exist")

    for root, _, files in os.walk(INFO_DIR):
        for file in files:
            input_path = Path(root) / file

            with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

                vector = titan_embed(bedrock, content)
                s3_vector_put_vector(
                    s3_vector_client,
                    S3_VECTOR_INDEX_ARN,
                    file,
                    vector,
                    {},
                )

if __name__ == "__main__":
    main()