import boto3

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

from . import dynamodb_login, dynamodb_music, dynamodb_subscriptions, s3_music_images