import boto3
import base64
import os
import json

CACHED_SECRET = {}
SECRET_NAME = os.environ["SECRET_NAME"]
SECRET_STRING = "SecretString"


def get_secret():
    global CACHED_SECRET

    if CACHED_SECRET:
        return CACHED_SECRET

    secret = boto3.client("secretsmanager").get_secret_value(SecretId=SECRET_NAME)
    CACHED_SECRET = json.loads(secret[SECRET_STRING])
    return CACHED_SECRET


def handler(event, context):

    # Retrieve request parameters from the Lambda function input:
    authorizationToken = event["authorizationToken"]

    if not authorizationToken:
        raise ValueError("Missing Authorization header")

    basic_auth = base64.b64decode(authorizationToken.replace("Basic ", "")).decode(
        "utf-8"
    )
    username, password = basic_auth.split(":")

    allowed_users = get_secret()

    if username in allowed_users and password == allowed_users[username]:
        response = generateAllow(username, event["methodArn"])
        return response
    else:
        response = generateDeny("user", event["methodArn"])
        return response


def generatePolicy(principalId, effect, resource):

    authResponse = {}
    authResponse["principalId"] = principalId
    if effect and resource:
        policyDocument = {}
        policyDocument["Version"] = "2012-10-17"
        policyDocument["Statement"] = []
        statementOne = {}
        statementOne["Action"] = "execute-api:Invoke"
        statementOne["Effect"] = effect
        statementOne["Resource"] = resource
        policyDocument["Statement"] = [statementOne]
        authResponse["policyDocument"] = policyDocument

    authResponse["context"] = {}

    return authResponse


def generateAllow(principalId, resource):
    return generatePolicy(principalId, "Allow", resource)


def generateDeny(principalId, resource):
    return generatePolicy(principalId, "Deny", resource)
