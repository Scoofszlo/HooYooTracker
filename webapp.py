from hooyootracker.webapp.home import create_app
from waitress import serve
import webbrowser

if __name__ == "__main__":
    app = create_app()
    webbrowser.open("http://127.0.0.1:8080")
    serve(app, host='0.0.0.0', port=8080)
