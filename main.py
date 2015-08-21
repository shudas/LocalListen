"""Routing"""
from flask import Flask, render_template, request, session, redirect, url_for
from security.auth import LoginResource
from webapp.basic_page import basic_page_blueprint
from flask_restful import Api

from helper import config_parser

# read the config before anything
config_parser.read_config()

app = Flask(__name__)
# app.register_blueprint(auth_blueprint, url_prefix='/svc/auth')
app.register_blueprint(basic_page_blueprint)
api = Api(app, prefix='/svc')
api.add_resource(LoginResource, '/auth/login')


# # redirects to /discover on success
# @app.route('/', methods=['GET'])
# def index():
#     if session.get('logged_in') and security.valid_token(session.get('access_token'), session.get('fb_user_id')):
#         return redirect(url_for('discover'))
#     redir_url = "/discover"
#     if request.args.get("redir"):
#         redir_url = request.args.get("redir")
#     session['logged_in'] = False
#     return render_template('index.html', redir=redir_url)
#
#
# def new_page_load_redir(redir_page):
#     redir_html = redir_page + '.html'
#     redir_url = "/" + redir_page
#     if session.get('logged_in') and security.valid_token(session.get('access_token'), session.get('fb_user_id')):
#         return render_template(redir_html)
#     elif request.method == 'POST':
#         try:
#             token = request.form['accessToken']
#             uid = request.form['userID']
#             app.logger.debug("GOT HERE")
#             if security.valid_token(token, uid):
#                 session['access_token'] = token
#                 session['fb_user_id'] = uid
#                 session['logged_in'] = True
#                 return render_template(redir_html)
#         except Exception as e:
#             app.logger.debug("Could not parse the POST params properly: ")
#             app.logger.debug(request.form)
#             return redirect(url_for('index', redir=redir_url))
#     # by default, go to index in case not logged in
#     session['logged_in'] = False
#     return redirect(url_for('index', redir=redir_url))
#
#
# @app.route('/discover', methods=['GET', 'POST'])
# def discover():
#     return new_page_load_redir("discover")
#
#
# @app.route('/upload', methods=['GET', 'POST'])
# def upload():
#     return new_page_load_redir("upload")
#
#
# @app.route('/manage', methods=['GET', 'POST'])
# def manage():
#     return new_page_load_redir("manage")


if __name__ == '__main__':
    app.config['SECRET_KEY'] = config_parser.config['Flask']['secret_key']
    app.config['DEBUG'] = bool(config_parser.config['Flask']['debug'])
    app.run()
