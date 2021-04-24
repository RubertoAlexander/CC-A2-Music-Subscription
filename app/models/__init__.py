import boto3

dynamodb = boto3.resource('dynamodb')

from . import dynamodb_login