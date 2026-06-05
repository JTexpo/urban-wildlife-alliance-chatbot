"""
a dependency inversion for s3
"""

import boto3
import os

from io import BytesIO

RAG_INFO_BUCKET_NAME = os.environ["RAG_INFO_BUCKET_NAME"]


def get_s3_bucket(bucket_name: str):
    """
    Get an S3 client.

    Returns:
    boto3.resource.Bucket: The S3 Bucket.
    """
    return boto3.resource("s3").Bucket(bucket_name)


def bucket_get_file(bucket, key: str) -> BytesIO:
    """
    Get a file from an S3 bucket.

    Parameters:
    s3_client (boto3.client): The S3 client.
    bucket_name (str): The name of the bucket.
    key (str): The key of the file.

    Returns:
    BytesIO: a filelike object
    """
    filelike_object: BytesIO = BytesIO()

    bucket.download_fileobj(Key=key, Fileobj=filelike_object)

    filelike_object.seek(0)

    return filelike_object
