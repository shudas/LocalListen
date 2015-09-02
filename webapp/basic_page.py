"""
Basic logic for rendering a page. Renders page if it exists, otherwise 404s
"""

from flask import Blueprint, render_template, abort, current_app, session
from jinja2 import TemplateNotFound
from external_service import facebook
from security import constants

basic_page_blueprint = Blueprint('basic_page', __name__, template_folder='templates')

@basic_page_blueprint.route('/', defaults={'page': 'index'})
@basic_page_blueprint.route('/<page>')
def show(page):
    try:
        if facebook.valid_token(session.get(constants.STR_FB_ACCESS_TOKEN), session.get(constants.STR_FB_USER_ID)):
            session[constants.STR_REAUTH] = False
        else:
            session[constants.STR_REAUTH] = True
        current_app.logger.debug("page is: {}".format(page))
        return render_template('pages/{}.html'.format(page))
    except TemplateNotFound:
        abort(404)
