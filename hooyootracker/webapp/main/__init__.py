from flask import Flask
from hooyootracker.webapp.main.views import home


def create_app():
    app = Flask(__name__)

    app.register_blueprint(home.bp)
    return app
