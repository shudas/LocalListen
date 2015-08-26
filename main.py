"""Routing"""
from flask import Flask
from flask_restful import Api

from security.auth import LoginResource, LogoutResource
from webapp.basic_page import basic_page_blueprint
from config.config_parser import get_config

app = Flask(__name__)
app.config['SECRET_KEY'] = get_config()['Flask']['secret_key']

app.register_blueprint(basic_page_blueprint)
api = Api(app, prefix='/svc')

# api endpoints
api.add_resource(LoginResource, '/auth/login')
api.add_resource(LogoutResource, '/auth/logout')

if __name__ == '__main__':
    app.config['DEBUG'] = bool(get_config()['Flask']['debug'])
    app.run()
