__author__ = 'Shu'

from flask import Flask, render_template, request, session, flash
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    SECRET_KEY='development key'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        app.logger.debug(request.data)
        print(request.data)
        flash("Got here")
        # session['access_token'] = request
        # session.modified = True
    return render_template('home.html')

if __name__ == '__main__':
    app.run()
