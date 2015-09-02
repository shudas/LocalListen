"""Authenticating users"""

from flask import session, request, current_app as app
from flask_restful import Resource
from external_service.facebook import valid_token, get_long_lived_token

import constants


def _clear_session():
    session[constants.STR_FB_ACCESS_TOKEN] = None
    session[constants.STR_FB_USER_ID] = None
    session[constants.STR_LOGGED_IN] = False


class LoginResource(Resource):
    def post(self):
        # already logged in and creds still valid
        if session.get(constants.STR_LOGGED_IN) and \
                valid_token(session.get(constants.STR_FB_ACCESS_TOKEN), session.get(constants.STR_FB_USER_ID)):
            app.logger.debug("User already logged in")
            return True
        # form was not right
        if not all(k in request.form for k in (constants.STR_FB_ACCESS_TOKEN, constants.STR_FB_USER_ID)):
            app.logger.error("POST request did not contain all of the necessary data")
            app.logger.debug(request.form)
            _clear_session()
            return False
        # validate creds provided
        token = request.form.get(constants.STR_FB_ACCESS_TOKEN)
        uid = request.form.get(constants.STR_FB_USER_ID)
        if valid_token(token, uid):
            session[constants.STR_FB_ACCESS_TOKEN] = get_long_lived_token(token)
            session[constants.STR_FB_USER_ID] = uid
            session[constants.STR_LOGGED_IN] = True
            return True
        else:
            _clear_session()
            return False


class LogoutResource(Resource):
    def post(self):
        _clear_session()
        return True
