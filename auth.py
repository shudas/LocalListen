__author__ = 'Shu'
"""Authenticating users"""
import requests, main

fb_app_id = '617235401742568'
fb_app_secret = '1f3a8f0428a1b79265f10af6863a43c2'


def valid_token(token, uid):
    """Determine if the given user token is valid"""
    app_access = fb_app_id + '|' + fb_app_secret
    args = {'input_token': token, 'access_token': app_access}
    r = requests.get("https://graph.facebook.com/debug_token", params=args)
    # something weird going on if status code isnt 200. Just sayin
    if r.status_code != requests.codes.ok:
        return False
    data = r.json()
    main.app.logger.debug('valid token returned: ')
    main.app.logger.debug(data)
    if (data['data']['is_valid'] and
            str(data['data']['user_id']) == str(uid) and
            str(data['data']['app_id']) == str(fb_app_id)):
        return True
    else:   # How to handle invalid access token?
        return False
