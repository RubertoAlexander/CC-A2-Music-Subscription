from app.models import dynamodb_login, dynamodb_music, dynamodb_subscriptions, s3_music_images
from flask import render_template, request, redirect
import urllib.parse

from app import app

@app.route('/', methods=['GET', 'POST'])
def index():
    user_email = request.cookies.get('email')

    # Load page if user logged in
    if user_email:
        # Retrieve username from db given stored email
        username = dynamodb_login.get_user(user_email).get('user_name')

        # Get all subscribed songs for user
        sub_result = dynamodb_subscriptions.get_user_subscriptions(user_email)

        # Retrieve all details to show to screen
        subs = []
        for sub_song in sub_result:
            # Get artist and title from joined key
            artist, title = separate_song_key(sub_song['artist#title'])

            # Get all details of song from the key
            full_song = dynamodb_music.get_song(artist, title)
            full_song['db_url'] = s3_music_images.get_image_url(artist + '.jpg')
            subs.append(full_song)
        
        scan_error = ''
        scan_songs = None
        # POST if query was entered
        if request.method == 'POST':
            artist_query = request.form['artist'] if 'artist' in request.form else None
            title_query = request.form['title'] if 'title' in request.form else None
            year_query = request.form['year'] if 'year' in request.form else None

            scan_songs = dynamodb_music.scan_music(artist_query, title_query, year_query)
            if scan_songs:
                for song in scan_songs:
                    song['db_url'] = s3_music_images.get_image_url(song['artist'] + '.jpg')
            else:
                scan_error = 'No result is retrieved. Please query again'

        return render_template('main.html', 
            user_name=username,
            subscriptions=subs,
            scan_songs=scan_songs,
            scan_error=scan_error
        )
    else:
        return redirect('/login')

@app.route('/remove', methods=['POST'])
def remove_subscription():
    song_key = request.form['song_key']
    user_email = request.cookies.get('email')
    dynamodb_subscriptions.remove_subscription(user_email, song_key)

    return redirect('/')

@app.route('/subscribe', methods=['POST'])
def add_subscription():
    song_key = request.form['song_key']
    user_email = request.cookies.get('email')
    dynamodb_subscriptions.add_subscription(user_email, song_key)

    return redirect('/')

def separate_song_key(song_key):
    key_splits = song_key.split('#', 1)
    return key_splits[0], key_splits[1]