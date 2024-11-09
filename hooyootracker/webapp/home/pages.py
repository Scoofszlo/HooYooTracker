from flask import Blueprint, render_template
from hooyootracker.data_processor import gi, zzz


bp = Blueprint("pages", __name__)


@bp.route("/")
@bp.route("/gi")
def home():
    code_list = gi.get_data()

    return render_template('gi.html', title='Genshin Impact — HooYooTracker', code_list=code_list)


@bp.route("/zzz")
def zzz_page():
    code_list = zzz.get_data()
    return render_template('zzz.html', title='ZZZ — HooYooTracker', code_list=code_list)
