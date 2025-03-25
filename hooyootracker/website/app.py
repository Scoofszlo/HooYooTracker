from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)

    from hooyootracker.website.blueprints.root.routes import core
    from hooyootracker.website.blueprints.gi.routes import gi
    from hooyootracker.website.blueprints.zzz.routes import zzz

    app.register_blueprint(core)
    app.register_blueprint(gi)
    app.register_blueprint(zzz)

    return app
