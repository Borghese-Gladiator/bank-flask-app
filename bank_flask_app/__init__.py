from flask import Flask

from bank_flask_app import pages

def create_app():
    app = Flask(__name__)

    app.register_blueprint(pages.bp)
    return app