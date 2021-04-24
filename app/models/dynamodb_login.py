from . import dynamodb

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

    if 'Item' in response:
        return response['Item']
    else:
        return None