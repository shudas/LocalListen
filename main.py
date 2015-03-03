__author__ = 'Shu'

from flask import Flask, render_template, request, session, flash, redirect, url_for
app = Flask(__name__)
app.secret_key = "MY SECRET KEY WHICH SHOULD BE CHANGED"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        session['logged_in'] = True
        flash('You were logged in')
        session['access_token'] = request
        return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/home', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        app.logger.debug(request.data)
        print(request.data)
        flash("Got here")
        session['access_token'] = request.data['accessToken']
    return render_template('home.html')

if __name__ == '__main__':
    app.run()
