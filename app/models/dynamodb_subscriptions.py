from . import dynamodb
from boto3.dynamodb.conditions import Key

SUBSCRIPTION_TABLE = dynamodb.Table('subscriptions')

def get_user_subscriptions(user_email: str):
    response = SUBSCRIPTION_TABLE.query(
        KeyConditionExpression=Key('email').eq(user_email)
    )

    return response['Items']

def remove_subscription(user_email: str, song_key: str):
    subscription_key = {
        'email': user_email,
        'artist#title': song_key
    }
    print(subscription_key)
    SUBSCRIPTION_TABLE.delete_item(Key=subscription_key)

def add_subscription(user_email: str, song_key: str):
    subscription_key = {
        'email': user_email,
        'artist#title': song_key
    }
    print(subscription_key)
    SUBSCRIPTION_TABLE.put_item(Item=subscription_key)
