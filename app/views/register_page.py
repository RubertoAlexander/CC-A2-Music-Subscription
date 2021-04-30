from flask import render_template, request, redirect

from app.models import dynamodb_login
from app import app

@app.route('/register', methods=['GET'])
def register_page():

    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    form_email = request.form['email']
    form_username = request.form['username']
    form_password = request.form['password']

    user_added = dynamodb_login.put_user(form_email, form_username, form_password)

    if user_added:
        return redirect('/login')
    else:
        return render_template('register.html', registerError='The email already exists')

