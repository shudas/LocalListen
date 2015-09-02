from config import config
from flask import current_app as app
from urlparse import parse_qs
import requests


def valid_token(token, uid):
    """
    Determines if the given access token is valid for the given user id
    :param token: access token to check
    :param uid: fb user id to check against
    :return: True if the token is valid for the given user. Otherwise False.
    """
    if token is None or uid is None:
        app.logger.debug("Token or user id is none")
        return False
    app_access = '{}|{}'.format(config.Facebook.app_id, config.Facebook.app_secret)
    args = {'input_token': token, 'access_token': app_access}
    r = requests.get("https://graph.facebook.com/debug_token", params=args)
    # something weird going on if status code isnt OK. Just sayin
    if r.status_code != requests.codes.ok:
        app.logger.debug("Something strange is happening when validating token. Status code is not OK")
        return False
    data = r.json().get('data', {})
    # Yay it's valid
    if data.get('is_valid') and str(data.get('user_id')) == str(uid) \
            and str(config.Facebook.app_id) == str(data.get('app_id')):
        app.logger.debug("Valid FB credentials")
        return True
    else:
        app.logger.debug("Incorrect FB creds")
        app.logger.debug('is_valid: {}, user_id_fb: {}, user_id_given: {}, app_id_fb: {}, app_id_stored: {}'
                         .format(data.get('is_valid'), data.get('user_id'), uid,
                                 data.get('app_id'), config.Facebook.app_id))
    return False


def get_long_lived_token(access_token):
    """
    returns a long lived token from the given short lived access token.
    if the fetch for the long lived token fails, the provided short lived token is returned
    :param access_token: short lived access token
    :return:
    """
    args = {'grant_type': 'fb_exchange_token',
            'client_id': config.Facebook.app_id,
            'client_secret': config.Facebook.app_secret,
            'fb_exchange_token': access_token}
    r = requests.get("https://graph.facebook.com/oauth/access_token", params=args)
    # returns text in the form of access_token=xxx&expires_in=###
    try:
        new_token = parse_qs(r.text).get('access_token')[0]
        app.logger.debug(new_token)
        return new_token
    except IndexError:
        return access_token
