import webbrowser
from waitress import serve
from hooyootracker.logging.logger import logger
from hooyootracker.website.app import create_app

if __name__ == "__main__":
    """
    This runs the web app and is serving using the Waitress WSGI server.
    """

    logger.info("HooYooTracker has been started. Open the app via: http://localhost:8080.")

    app = create_app()
    webbrowser.open("http://127.0.0.1:8080")
    serve(app, host='0.0.0.0', port=8080)
