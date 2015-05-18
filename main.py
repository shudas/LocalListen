__author__ = 'Shu'
"""Routing"""
import auth
from flask import Flask, render_template, request, session, redirect, url_for
app = Flask(__name__)
app.secret_key = "MY SECRET KEY WHICH SHOULD BE CHANGED"
app.debug = True


# redirects to /discover on success
@app.route('/', methods=['GET'])
def index():
    if session.get('logged_in'):
        return redirect(url_for('discover'))
    return render_template('index.html', redir="/discover")

def new_page_load_redir(redir_page):
    redir_html = redir_page + '.html'
    redir_url = "/" + redir_page
    if session.get('logged_in'):
        return render_template(redir_html)
    elif request.method == 'POST':
        try:
            token = request.form['accessToken']
            uid = request.form['userID']
            app.logger.debug('token from POST: ' + token)
            if auth.valid_token(token, uid):
                session['access_token'] = token
                session['user_id'] = uid
                session['logged_in'] = True
                return render_template(redir_html)
        except Exception:
            app.logger.debug("Could not parse the POST params properly")
            return redirect(url_for('index', redir=redir_url))
    # by default, go to index in case not logged in
    return redirect(url_for('index', redir=redir_url))

@app.route('/discover', methods=['GET', 'POST'])
def discover():
    return new_page_load_redir("discover")
    # if session.get('logged_in'):
    #     return render_template('discover.html')
    # elif request.method == 'POST':
    #     try:
    #         token = request.form['accessToken']
    #         uid = request.form['userID']
    #         app.logger.debug('token from POST: ' + token)
    #         if auth.valid_token(token, uid):
    #             session['access_token'] = token
    #             session['user_id'] = uid
    #             session['logged_in'] = True
    #             return render_template('discover.html')
    #     except Exception:
    #         app.logger.debug("Could not parse the POST params properly")
    #         return redirect(url_for('index', redir="/discover"))
    # # by default, go to index in case not logged in
    # return redirect(url_for('index', redir="/discover"))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    return new_page_load_redir("upload")

@app.route('/manage', methods=['GET', 'POST'])
def manage():
    return new_page_load_redir("manage")

if __name__ == '__main__':
    app.run()
