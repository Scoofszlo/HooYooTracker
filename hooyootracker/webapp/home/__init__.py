from flask import Flask
from hooyootracker.webapp.home import pages


def create_app():
    app = Flask(__name__)

    app.register_blueprint(pages.bp)
    return app
