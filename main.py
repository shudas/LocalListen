__author__ = 'Shu'
"""Routing"""
import auth
from flask import Flask, render_template, request, session
app = ""
app = Flask(__name__)
app.secret_key = "MY SECRET KEY WHICH SHOULD BE CHANGED"
app.debug = True


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            token = request.form['accessToken']
            app.logger.debug('token from POST: ' + token)
            if auth.valid_token(token):
                session['access_token'] = token
                session['logged_in'] = True
                return render_template('index.html', logged_in='True')
        except Exception:
            app.logger.debug("Could not parse the POST params properly")
            return render_template('index.html', logged_in='False')
    elif session.get('logged_in'):
        return render_template('index.html', logged_in='True')
    app.logger.debug('GOT BEFORE RENDER INDEX ELSE')
    return render_template('index.html', logged_in='False')

if __name__ == '__main__':
    app.run()
