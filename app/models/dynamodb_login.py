from . import dynamodb

from botocore.exceptions import ClientError

LOGIN_TABLE = dynamodb.Table('login')

def authenticate_user(email: str, password: str) -> bool:
    
    user = get_user(email=email)
    if user:
        if user['password'] == password:
            return True
        else:
            return False
    else:
        return False

def get_user(email: str) -> dict:
    user_key = {
        'email' : email
    }
    response = LOGIN_TABLE.get_item(Key=user_key)

    user = None
    if 'Item' in response:
        user = response['Item']
    
    return user

def put_user(email: str, username: str, password: str) -> bool:
    new_user = {
        'email': email,
        'user_name': username,
        'password': password
    }
    try:
        LOGIN_TABLE.put_item(Item=new_user, ConditionExpression='attribute_not_exists(email)')
    except ClientError:
        return False
    else:
        return True