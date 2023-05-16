import tempfile

import botocore
from flask import Flask, render_template, session, request, json, url_for, redirect, flash
from flask import send_from_directory
import pymysql
import hashlib
import smtplib
from email.mime.text import MIMEText
import os
# from keras.models import load_model
# from tensorflow.keras.utils import load_img # type: ignore
# import numpy as np
# import tensorflow as tf
from datetime import datetime
#import redis  # For Redis
import Credentials
import boto3
import pytz
import secrets
from pydub import AudioSegment
import soundfile as sf
import io
import os
import os
import joblib
import ML_Model.Era_Classifier  as era_classifier
import ML_Model.Composer_Classifier  as composer_classifier
from sendgrid.helpers.mail import Mail, Email, To, Content
import ssl
import io
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from flask import Flask, request, redirect, url_for, render_template

era_model_file = era_classifier.getDirectory() + "/joblib_model_era.pkl"
# era_model = era_classifier.joblib.load(era_model_file)
composer_model_file = composer_classifier.getDirectory() + "/joblib_model_composer.pkl"

era = joblib.load(era_model_file)
composer = joblib.load(composer_model_file)
# composer_model = composer_classifier.joblib.load(composer_model_file)



databaseHost = Credentials.DB_name
databaseUser = Credentials.DB_user
databasePass = Credentials.DB_passwd
cacheHost = Credentials.DB_cachehost
cachePort = Credentials.DB_port
appSecretKey = Credentials.SecretKey
#redisCache = redis.StrictRedis(host=cacheHost, port=cachePort, db=0)
db = pymysql.connect(host=databaseHost,
                     user=databaseUser,
                     password=databasePass,
                     database='Muzera',
                     charset='utf8mb4',
                     cursorclass=pymysql.cursors.DictCursor)

dir_path = os.path.dirname(os.path.realpath(__file__))
staticURL = dir_path + '/static'
UPLOAD_FOLDER = dir_path + '/uploads'


ssl._create_default_https_context = ssl._create_unverified_context

s3 = boto3.client('s3',
                  aws_access_key_id=Credentials.ACCESS_KEY,
                  aws_secret_access_key=Credentials.SECRET_ACCESS_KEY)
bucket_name = 'muzera-s3'

app = Flask(__name__)

app.secret_key = appSecretKey


@app.route("/")
def home():
    if session:
        return render_template('home.html')
    else:
        return render_template('index.html')


@app.route('/secure-login', methods=['POST'])
def signin():
    # adding a key to secure form against injection
    # can further encrypt this key
    form_secure = 'This$#is#$my#$Secret@#Key!'
    form_key = request.form['form_secure']
    # check if form security key is present
    if form_key and form_key == form_secure:
        # collect login-form inputs
        username = request.form['username']
        password = request.form['password']
        h = hashlib.md5(password.encode())
        password = h.hexdigest()
        # user_group from database
        if request.method == 'POST' and username and password:
            # Check if account exists using MySQL
            cursor = db.cursor()
            sql = 'SELECT * FROM accounts WHERE username = %s'
            cursor.execute(sql, username)
            # Fetch one record and return result
            account = cursor.fetchone()
            # If account exists in accounts table in our database
            if account and password == account['password']:
                session['signin'] = True
                session['username'] = username
                session['sessionkey'] = password
                s3_folder_name = session['username']  # create folder with user name
                s3.put_object(Bucket=bucket_name, Key=(s3_folder_name + '/'))  # create the folder in S3
                return render_template('home.html')
            else:
                msg = "Invalid Username/Password"
                return render_template('index.html', msg=msg)
        else:
            msg = "Something went 3!"
            return render_template('index.html', msg=msg)
    else:
        msg = "Something went wrong 4!"
        return render_template('index.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('signin', None)
    session.pop('username', None)
    session.pop('sessionkey', None)
    return render_template('index.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    # adding a key to secure form against injection
    # can further encrypt this key
    form_secure = 'This$#is#$my#$Secret@#Key!'
    form_key = request.form['form_secure']
    # check if form security key is present
    if form_key and form_key == form_secure:
        username = request.form['username']
        password = request.form['password']
        # encode our user submitted password
        

        email = request.form['email']
        # check that all fields have been submitted
        if request.method == 'POST' and username and password and email:

            # Check if account exists using MySQL
            cursor = db.cursor()
            sql = 'SELECT * FROM accounts WHERE username = %s'
            cursor.execute(sql, username)
            # Fetch one record and return result
            account = cursor.fetchone()
            # If account exists in accounts table in out database
            if account:
                msg = 'Error! User account or email already exists!'
                return render_template('signup.html', msg=msg)
            
            else:
                
                h = hashlib.md5(password.encode())
                password = h.hexdigest()
                cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, NULL)', (username, password, email))
                # the connection is not autocommited by default. So we must commit to save our changes.
                db.commit()
                msg = 'Welcome to Muzera, ' + username
                return render_template('successfully_registered.html', msg=msg)
        else:
            msg = 'something went wrong'
            return render_template('signup.html', msg=msg)

    # return 'successfully registered user: '+ username
    else:
        msg = 'something went wrong'
        return render_template('signup.html', msg=msg)


@app.route('/profile')
def profile():
    username = session['username']
    sessionkey = session['sessionkey']
    # Check if account exists using MySQL
    cursor = db.cursor()
    sql = 'SELECT * FROM accounts WHERE username = %s'
    cursor.execute(sql, username)
    # Fetch one record and return result
    account = cursor.fetchone()
    # If account exists in accounts table in out database
    if account and (sessionkey == account['password']):
        # return 'Your personal details:<br>Username: ' + account[1] + '<br>' + 'Email: '+ account[3] + '<br>Password: ' + account[2] + '<br>(session pwd: '+ password +')'
        return render_template('profile.html', userid=account['id'], username=account['username'], ID=account['id'],
                               email=account['email'])

    else:
        return 'No matching record found!'

'''
@app.route('/last_check')
def lastCheck():
    userName = str(session['username'])

    cursor = db.cursor()
    sql = 'SELECT * FROM accounts WHERE username = %s'
    cursor.execute(sql, userName)
    account = cursor.fetchone()
    userID = account['id']
    cursor.execute(sql, str(session['username']))
    sql = 'select * from check_history where user_id=%s order by id desc;'
    a2 = datetime.now()
    cursor.execute(sql, (userID))
    s = cursor.fetchone()
    b2 = datetime.now()
    c2 = b2 - a2
    # with open('d:/cacheTimeLaps2.txt','w') as myfile:
    #     myfile.write(str(c2.microseconds))
    if s:
        label = s['label']
        accuracy = s['accuracy']
        fileName = s['fName']
        return render_template('predict.html', image_file_name=fileName, label=label, accuracy=accuracy)
    else:
        return render_template('NoLastSearchFound.html', pageMessage='No Search Has Been Recorded For This User!')

'''



def get_delete_link(bucket_name, key):
    s3 = boto3.client('s3')
    url = s3.generate_presigned_url(
        'delete_object',
        Params={'Bucket': bucket_name, 'Key': key},
        ExpiresIn=3600,  # 1 hour
        HttpMethod='DELETE'
    )
    return url

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        # Handle the Forgot Password request
        email = request.form['email']

        # Generate a random token
        token = secrets.token_hex(16)

        # Store the token in the database
        cur = db.cursor()
        cur.execute("UPDATE accounts SET password_reset_link = %s WHERE email = %s", (token, email))
        db.commit()

        # Email to the user with a password reset link
        reset_url = url_for('reset_password', token=token, _external=True)
        message = Mail(
            from_email=Email('puneet.tokhi@sjsu.edu', 'Muzera'),
            to_emails=To(email),
            subject='Password Reset Request',
            html_content='<p>Hello,</p><p>You recently requested a password reset for your Muzera account. To reset your password, please click the following link:</p><p><a href="{}">Reset Password</a></p><p>If you did not make this request, please ignore this email.</p><p>Best regards,</p><p>The Muzera Team</p>'.format(
                reset_url))

        # Set up SendGrid API key
        sg_api_key = Credentials.API_KEY

        # Send email via SendGrid API
        try:
            sg = SendGridAPIClient(api_key=sg_api_key)
            response = sg.send(message)
            print(response.status_code)
        except Exception as e:
            print(str(e))

        # After handling the Forgot Password request, redirect the user to the login page
        return render_template('index.html')
    else:
        # If the request method is GET, show the Forgot Password form
        return render_template('forgot_password.html')


@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        # Handle the Reset Password request
        token = request.form['token']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        h = hashlib.md5(password.encode())
        password = h.hexdigest()

        h = hashlib.md5(confirm_password.encode())
        confirm_password = h.hexdigest()

        # Check if the passwords match
        if password != confirm_password:
            return render_template('reset_password.html', token=token, error="Passwords don't match")

        # Update the user's password in the database
        cur = db.cursor()
        cur.execute("SELECT * FROM accounts WHERE password_reset_link = %s", token)
        account = cur.fetchone()
        if not account:
            flash('Invalid or expired token. Please try again.')
            return redirect(url_for('reset_password'))

        cur.execute("UPDATE accounts SET password = %s, password_reset_link = NULL WHERE id = %s",
                    (password, account['id']))
        db.commit()

        # After resetting the password, redirect the user to the login page
        return render_template('index.html', success="Password Successfully Reset")

    else:
        # If the request method is GET, show the Reset Password form
        token = request.args.get('token')
        if not token:
            return render_template('index.html')

        return render_template('reset_password.html', token=token)

def get_file_from_s3(bucket_name, key):
    # create a temporary file to download the S3 file to
    temp_file = tempfile.NamedTemporaryFile(delete=False)

    # download the S3 file to the temporary file
    s3.download_file(bucket_name, key, temp_file.name)

    # reset the file pointer to the beginning of the file
    temp_file.seek(0)

    # return the temporary file object
    return temp_file
@app.route('/music-files')
def music_files():
    success_msg = request.args.get('success_msg')

    # get the user's folder name
    folder_name = session['username']

    # list objects in the user's folder
    # response = s3.list_objects_v2(Bucket=bucket_name, Prefix=f"{folder_name}/")

    # create a Config object with signature version set to 's3v4'
    # s3_config = botocore.config.Config(signature_version='s3v4')
    # s3_client = boto3.client('s3', config=s3_config)

    # list objects in the user's folder
    # response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=f"{folder_name}/")
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=f"{folder_name}/")

    # if the user's folder is empty, return an empty list of check_results
    if 'Contents' not in response:
        checkResults = []
    else:
        checkResults = []
        for obj in response['Contents']:
            key = obj['Key']
            if key.endswith('/'):
                continue  # skip the folder itself if it appears in the list of objects

            download_link = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': key})

            pst = pytz.timezone('America/Los_Angeles')
            head_object = s3.head_object(Bucket=bucket_name, Key=key)
            creation_date = head_object['LastModified'].astimezone(pst)

            formatted_date = datetime.strftime(creation_date, "%H:%M:%S %m-%d-%Y")

            import time
            start = time.time()

            # fetch the file from S3
            response = s3.get_object(Bucket=bucket_name, Key=key)
            print(time.time()-start)
            file_contents = response['Body'].read()

            # write the contents of the S3 object to a temporary file
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(file_contents)

            composer_predicted, composer_confidence = composer_classifier.predict(tmp_file.name, composer)
            era_predicted, era_confidence = era_classifier.predict(tmp_file.name, era)

            title = os.path.basename(key)

            # s3file = get_file_from_s3(bucket_name, key)
            check_result = {
                'title': title,  # use os.path.basename to get the filename
                'composer': composer_predicted,
                'era': era_predicted,
                'id': '',
                'checked_at': formatted_date,
                'download_link': download_link,
                'Bucket': bucket_name,
                'Key': key
            }
            checkResults.append(check_result)

    return render_template('music-history.html', check_results=checkResults, success_msg=success_msg)


@app.route('/delete/<path:key>')
def delete_file(key):
    s3.delete_object(Bucket=bucket_name, Key=key)
    success_msg = 'File successfully deleted'
    return redirect(url_for('music_files', success_msg=success_msg))


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html', staticURL=staticURL)

    else:
        # cursor = db.cursor()
        file = request.files['audio']
        file_contents = file.read()

        format = file.content_type.split('/')[1].split('-')[-1]
        # Extract audio information
        audio = AudioSegment.from_file(io.BytesIO(file_contents), format=format)
        duration = audio.duration_seconds
        sample_rate = audio.frame_rate
        channels = audio.channels

        # Upload audio file to S3
        # uploaded_file = io.BytesIO(file_contents)
        key = '{}/{}'.format(session['username'], file.filename)
        s3.upload_fileobj(io.BytesIO(file_contents), bucket_name, key)

        # Format audio information for display
        duration_str = '{:.2f}'.format(duration)
        sample_rate_str = '{:,}'.format(sample_rate)
        channels_str = 'Stereo' if channels == 2 else 'Mono'

        composer_predicted, composer_accuracy = composer_classifier.predict(io.BytesIO(file_contents), composer)
        era_predicted, era_accuracy = era_classifier.predict(io.BytesIO(file_contents), era)

        # Display up to 2 decimal places
        era_accuracy = era_accuracy * 100
        composer_accuracy = (composer_accuracy * 100)

        return render_template('predict.html',
                               filename=file.filename,
                               duration=duration_str,
                               sample_rate=sample_rate_str,
                               channels=channels_str,
                               era=era_predicted,
                               composer=composer_predicted,
                               era_accuracy='{:.2f}'.format(era_accuracy),
                               composer_accuracy='{:.2f}'.format(composer_accuracy))
'''
@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
'''

if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)
    app.debug = True
