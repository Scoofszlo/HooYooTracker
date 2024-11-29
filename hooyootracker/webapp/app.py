import webbrowser
from waitress import serve
from hooyootracker.logger import Logger
from hooyootracker.webapp.main import create_app


def run() -> None:
    """
    This runs the web app and is serving using the Waitress WSGI server.
    """

    app = create_app()
    webbrowser.open("http://127.0.0.1:8080")
    serve(app, host='0.0.0.0', port=8080)
