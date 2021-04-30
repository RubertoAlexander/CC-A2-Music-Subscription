from . import s3

MUSIC_IMAGES_BUCKET = 'cc-music-images-s3663431'

def get_image_url(filename: str):
    response = s3.generate_presigned_url(
        'get_object', 
        Params={'Bucket': MUSIC_IMAGES_BUCKET, 'Key': filename},
        ExpiresIn=3600
    )

    return response