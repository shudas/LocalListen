"""
Basic logic for rendering a page. Renders page if it exists, otherwise 404s
"""

from flask import Blueprint, render_template, abort, current_app
from jinja2 import TemplateNotFound

basic_page_blueprint = Blueprint('basic_page', __name__, template_folder='templates')

@basic_page_blueprint.route('/', defaults={'page': 'index'})
@basic_page_blueprint.route('/<page>')
def show(page):
    try:
        current_app.logger.debug("page is: {}".format(page))
        return render_template('pages/{}.html'.format(page))
    except TemplateNotFound:
        abort(404)
