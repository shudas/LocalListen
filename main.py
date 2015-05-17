__author__ = 'Shu'
"""Routing"""
import auth
from flask import Flask, render_template, request, session, redirect, url_for
app = Flask(__name__)
app.secret_key = "MY SECRET KEY WHICH SHOULD BE CHANGED"
app.debug = True


# redirects to /listen on success
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', redir="/listen")

@app.route('/listen', methods=['GET', 'POST'])
def listen():
    if request.method == 'POST':
        try:
            token = request.form['accessToken']
            uid = request.form['userID']
            app.logger.debug('token from POST: ' + token)
            if auth.valid_token(token, uid):
                session['access_token'] = token
                session['user_id'] = uid
                session['logged_in'] = True
                return render_template('listen.html')
        except Exception:
            app.logger.debug("Could not parse the POST params properly")
            return redirect(url_for('index', redir="/listen"))
    elif session.get('logged_in'):
        return render_template('listen.html')
    # by default, go to index in case not logged in
    return redirect(url_for('index', redir="/listen"))

if __name__ == '__main__':
    app.run()
