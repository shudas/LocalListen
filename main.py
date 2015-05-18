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
    if session.get('logged_in') and auth.valid_token(session.get('access_token'), session.get('fb_user_id')):
        return redirect(url_for('discover'))
    redir_url = "/discover"
    if request.args.get("redir"):
        redir_url = request.args.get("redir")
    session['logged_in'] = False
    return render_template('index.html', redir=redir_url)

def new_page_load_redir(redir_page):
    redir_html = redir_page + '.html'
    redir_url = "/" + redir_page
    if session.get('logged_in') and auth.valid_token(session.get('access_token'), session.get('fb_user_id')):
        return render_template(redir_html)
    elif request.method == 'POST':
        try:
            token = request.form['accessToken']
            uid = request.form['userID']
            if auth.valid_token(token, uid):
                session['access_token'] = token
                session['fb_user_id'] = uid
                session['logged_in'] = True
                return render_template(redir_html)
        except Exception:
            app.logger.debug("Could not parse the POST params properly")
            return redirect(url_for('index', redir=redir_url))
    # by default, go to index in case not logged in
    session['logged_in'] = False
    return redirect(url_for('index', redir=redir_url))

@app.route('/discover', methods=['GET', 'POST'])
def discover():
    return new_page_load_redir("discover")

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    return new_page_load_redir("upload")

@app.route('/manage', methods=['GET', 'POST'])
def manage():
    return new_page_load_redir("manage")

if __name__ == '__main__':
    app.run()
