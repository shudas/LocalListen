"""Routing"""
from flask import Flask, render_template, request, session, redirect, url_for
from security.auth import LoginResource
from webapp.basic_page import basic_page_blueprint
from flask_restful import Api

from helper.config_parser import get_config

# read the config before anything

app = Flask(__name__)
app.config['SECRET_KEY'] = get_config()['Flask']['secret_key']

# app.register_blueprint(auth_blueprint, url_prefix='/svc/auth')
app.register_blueprint(basic_page_blueprint)
api = Api(app, prefix='/svc')
api.add_resource(LoginResource, '/auth/login')


if __name__ == '__main__':
    app.config['DEBUG'] = bool(get_config()['Flask']['debug'])
    app.run()
