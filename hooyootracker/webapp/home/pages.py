from flask import Blueprint, render_template
from hooyootracker.data_processor import gi


bp = Blueprint("pages", __name__)


@bp.route("/")
@bp.route("/gi")
def home():
    code_list = gi.get_data()

    return render_template('gi.html', title='Genshin Impact — HooYooTracker', code_list=code_list)


@bp.route("/zzz")
def zzz():
    return render_template('zzz.html', title='ZZZ — HooYooTracker')
