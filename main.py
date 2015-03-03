__author__ = 'Shu'

from flask import Flask, render_template, request, session, flash, redirect, url_for
app = Flask(__name__)
app.secret_key = "MY SECRET KEY WHICH SHOULD BE CHANGED"
app.debug = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        app.logger.debug(request.form['accessToken'])
        session['access_token'] = request.form['accessToken']
        session['userid'] = request.form['userID']
        session['logged_in'] = True
        return redirect(url_for('home'))
    # if already logged in then go to home
    elif session.get('logged_in'):
        return redirect(url_for('home'))
    app.logger.debug('GOT BEFORE RENDER LOGIN')
    return render_template('login.html')

@app.route('/home', methods=['POST', 'GET'])
def home():
    if session.get('logged_in') and session.get('userid'):
        app.logger.debug('GOT BEFORE RENDER HOME')
        return render_template('home.html')
    # not logged in
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
