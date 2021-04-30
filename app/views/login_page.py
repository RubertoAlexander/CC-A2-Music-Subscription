from app.models import dynamodb_login
from flask import render_template, request, redirect, make_response

from app import app

@app.route('/login', methods=['GET'])
def login_page():

    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    form_email = request.form['email']
    form_password = request.form['password']

    is_successful = dynamodb_login.authenticate_user(form_email, form_password)
    
    if is_successful:
        response = make_response(redirect('/'))
        response.set_cookie('email', form_email)
        return response
    else:
        return render_template('login.html', loginError='Email or password is invalid')
