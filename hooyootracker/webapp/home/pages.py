from flask import Blueprint, render_template
from hooyootracker.data_processor import gi, zzz
from hooyootracker.constants import CONFIG_FILE_PATH


bp = Blueprint("pages", __name__)


@bp.route("/")
@bp.route("/gi")
def home():
    sources = gi.get_sources(config_path=CONFIG_FILE_PATH)
    code_list = gi.get_data(sources=sources)

    return render_template('gi.html', title='Genshin Impact — HooYooTracker', code_list=code_list)


@bp.route("/zzz")
def zzz_page():
    sources = zzz.get_sources(config_path=CONFIG_FILE_PATH)
    code_list = zzz.get_data(sources=sources)

    return render_template('zzz.html', title='ZZZ — HooYooTracker', code_list=code_list)
