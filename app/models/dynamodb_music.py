from boto3.dynamodb.conditions import Attr
from . import dynamodb

MUSIC_TABLE = dynamodb.Table('music')

def get_song(artist: str, title: str):
    song_key = {
        'artist': artist,
        'title': title
    }
    response = MUSIC_TABLE.get_item(Key=song_key)

    song = None
    if 'Item' in response:
        song = response['Item']

    return song

def scan_music(artist: str, title: str, year: str):
    filter_list = []
    # Add conditions to filters if entered
    if artist: filter_list.append(Attr('artist').contains(artist))
    if title: filter_list.append(Attr('title').contains(title))
    if year: filter_list.append(Attr('year').contains(year))

    first = True
    filter_expression = None
    for condition in filter_list:
        if first:
            filter_expression = condition
            first = False
        else:
            # Combine filters
            filter_expression = filter_expression | condition

    if filter_expression:
        response = MUSIC_TABLE.scan(
            FilterExpression=filter_expression
        )
    else:
        response = MUSIC_TABLE.scan()

    result = None
    if 'Items' in response:
        result = response['Items']
    
    return result