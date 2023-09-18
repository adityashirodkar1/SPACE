from flask import Flask, render_template , request , redirect, url_for , session
import db as dbs
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Login User 
@app.route("/", methods=['POST'])
def login():
    users = dbs.users
    login_user = users.find_one({'username' : request.form['username']})

    if login_user:
        if bcrypt.check_password_hash(login_user['password'], request.form['password']):
            session['username'] = request.form['username']
            return "Logged in"

    return 'Invalid username/password combination'

#Register User
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

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)

