from flask import Flask, render_template , request , redirect, url_for , session
import db as dbs
from flask_bcrypt import Bcrypt
from googleapiclient.discovery import build

# Your YouTube Data API key
api_key = 'AIzaSyB58-ZQwCxeTzE3AUGHgLOoqiowjhC-OlM'
app = Flask(__name__)
bcrypt = Bcrypt(app)

@app.route("/", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        users = dbs.users
        login_user = users.find_one({'username' : request.form['username']})

        if login_user:
            if bcrypt.check_password_hash(login_user['password'], request.form['password']):
                session['username'] = request.form['username']
                return render_template('index.html')

        return redirect("/")
    return render_template('log.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = dbs.users
        existing_user = users.find_one({'username' : request.form['username']})
        if existing_user is None:
            hashpass = bcrypt.generate_password_hash(request.form['password'], 10)
            #hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({'username' : request.form['username'], 'password' : hashpass, 'email': request.form['email']})
            session['username'] = request.form['username']
            return f"Successful registeration of {session['username']}"
        
        return 'Username already exists!'

    return "Register HTML"

@app.route('/book', methods = ['POST', 'GET'])
def book():
    if 'username' in session:
        if request.method == 'GET':
            return render_template('book.html')
    return redirect('/')
    
@app.route('/timetable', methods = ['POST', 'GET'])
def timetable():
    if 'username' in session:
        if request.method == 'GET':
            return render_template('timetable.html')
    return redirect('/')

@app.route('/home', methods = ['POST', 'GET'])
def home():
    if 'username' in session:
        if request.method == 'GET':
            return render_template('index.html')
    return redirect('/')
    
@app.route('/lec', methods = ['POST', 'GET'])
def lec():
    if 'username' in session:
        if request.method == 'GET':
            return render_template('lecture.html')
    return redirect('/')
    
@app.route('/vid/<subject>')
def sublect(subject):
    # Initialize the YouTube Data API client
    youtube = build('youtube', 'v3', developerKey=api_key)
    searched = []
    # Example: Search for videos on a specific topic
    search_results = youtube.search().list(
        q=subject+' BTECH LECTURES SYLLABUS', 
        type='video', 
        part='snippet',
        order='videoCount',
        regionCode='IN',
        relevanceLanguage='hi',
        maxResults=10
    ).execute()

    # Extract video information
    videos = []
    for search_result in search_results.get('items', []):
        video_id = search_result['id']['videoId']
        title = search_result['snippet']['title']
        videos.append({'video_id': video_id, 'title': title})

    return render_template('vid.html', videos = videos, searched = searched)

@app.route('/ass', methods = ['POST', 'GET'])
def ass():
    if 'username' in session:
        if request.method == 'GET':
            return render_template('ass.html')
    return redirect('/')
    
# Logout User 
@app.route("/logout")
def logout():
    session.pop('username',None)
    return redirect('/')

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)