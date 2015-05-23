__author__ = 'Shu'
"""Authenticating users"""
import requests, main
from config_parser import config as conf


def valid_token(token, uid):
    """Determine if the given user token is valid"""
    app_access = conf['Facebook']['app_id'] + '|' + conf['Facebook']['app_secret']
    args = {'input_token': token, 'access_token': app_access}
    r = requests.get("https://graph.facebook.com/debug_token", params=args)
    # something weird going on if status code isnt OK. Just sayin
    if r.status_code != requests.codes.ok:
        print "Something strange is happening when validating token. Status code is not OK"
        return False
    data = r.json()
    main.app.logger.debug('valid token returned: ')
    main.app.logger.debug(data)
    if (data['data']['is_valid'] and
            str(data['data']['user_id']) == str(uid) and
            str(data['data']['app_id']) == str(conf['Facebook']['app_id'])):
        return True
    else:   # How to handle invalid access token?
        return False
