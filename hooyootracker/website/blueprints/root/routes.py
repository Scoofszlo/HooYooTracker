from flask import Blueprint, redirect

core = Blueprint("core", __name__, url_prefix="/")


@core.route("/")
def index():
    return redirect("/gi")
