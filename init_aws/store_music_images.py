import boto3
import requests

def get_image_urls(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('music')
    
    # Retrieve entire table
    response = table.scan()

    print('Retrieving all image urls...')
    music = response.get('Items')
    image_urls = {}
    for song in music:
        image_urls[song['artist']] = song['img_url']

    return image_urls

def upload_image_s3(bucket, data, name):
    s3 = boto3.client('s3')
    print('Uploading: ', name)
    s3.upload_fileobj(data, bucket, name)

# Task 2 - Downloading and storing all artist images in s3
if __name__ == '__main__':
    image_urls = get_image_urls()

    # Download each image from the and store in s3 before saving as file
    for key in image_urls.keys():
        with requests.get(image_urls[key], stream=True) as r:
            upload_image_s3('cc-music-images-s3663431', r.raw, key+'.jpg')

