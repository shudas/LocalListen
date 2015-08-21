"""Authenticating users"""

from flask import Blueprint, session, request, current_app as app, render_template, render_template_string
from flask_restful import Resource

from helper.config_parser import get_config
import constants
import requests


# auth_blueprint = Blueprint('auth', __name__)
#
# @auth_blueprint.route('/login', methods=['POST'])
# def login():
#     # already logged in and creds still valid
#     if session.get(constants.STR_LOGGED_IN) and \
#             valid_fb_token(session.get(constants.STR_ACCESS_TOKEN), session.get(constants.STR_USER_ID)):
#         app.logger.debug("User already logged in")
#         return render_template_string('True')
#     # form was not right
#     if not all(k in request.form for k in (constants.STR_FB_ACCESS_TOKEN, constants.STR_FB_USER_ID)):
#         app.logger.debug("POST request did not contain all of the necessary data")
#         app.logger.debug(request.form)
#         return render_template_string('False')
#     # validate creds provided
#     token = request.form.get(constants.STR_FB_ACCESS_TOKEN)
#     uid = request.form.get(constants.STR_FB_USER_ID)
#     if valid_fb_token(token, uid):
#         session[constants.STR_ACCESS_TOKEN] = token
#         session[constants.STR_USER_ID] = uid
#         session[constants.STR_LOGGED_IN] = True
#         return render_template_string('True')
#     else:
#         session[constants.STR_LOGGED_IN] = False
#         return render_template_string('False')


def valid_fb_token(token, uid):
    """Determine if the given user token is valid for the given user id"""
    if token is None or uid is None:
        app.logger.debug("Token or user id is none")
        return False
    app_access = '{}|{}'.format(get_config()['Facebook']['app_id'], get_config()['Facebook']['app_secret'])
    args = {'input_token': token, 'access_token': app_access}
    r = requests.get(constants.FB_DEBUG_ENDPOINT, params=args)
    # something weird going on if status code isnt OK. Just sayin
    if r.status_code != requests.codes.ok:
        app.logger.debug("Something strange is happening when validating token. Status code is not OK")
        return False
    data = r.json().get('data', {})
    # Yay it's valid
    if data.get('is_valid') and str(data.get('user_id')) == str(uid) \
            and str(get_config()['Facebook']['app_id']) == str(data.get('app_id')):
        app.logger.debug("Correct FB creds. YAY")
        return True
    else:
        app.logger.debug("Incorrect FB creds. BOO")
        app.logger.debug('is_valid: {}, user_id_fb: {}, user_id_given: {}, app_id_fb: {}, app_id_stored: {}'
                         .format(data.get('is_valid'), data.get('user_id'), uid,
                                 data.get('app_id'), get_config()['Facebook']['app_id']))
    return False


class LoginResource(Resource):
    def post(self):
        # already logged in and creds still valid
        if session.get(constants.STR_LOGGED_IN) and \
                valid_fb_token(session.get(constants.STR_ACCESS_TOKEN), session.get(constants.STR_USER_ID)):
            app.logger.debug("User already logged in")
            return True
        # form was not right
        if not all(k in request.form for k in (constants.STR_FB_ACCESS_TOKEN, constants.STR_FB_USER_ID)):
            app.logger.debug("POST request did not contain all of the necessary data")
            app.logger.debug(request.form)
            session[constants.STR_LOGGED_IN] = False
            return False
        # validate creds provided
        token = request.form.get(constants.STR_FB_ACCESS_TOKEN)
        uid = request.form.get(constants.STR_FB_USER_ID)
        if valid_fb_token(token, uid):
            session[constants.STR_ACCESS_TOKEN] = token
            session[constants.STR_USER_ID] = uid
            session[constants.STR_LOGGED_IN] = True
            return True
        else:
            session[constants.STR_LOGGED_IN] = False
            return False
