from flask import Blueprint, render_template, request, redirect, url_for
from hooyootracker.constants import CONFIG_FILE_PATH
from hooyootracker.data_processor.code_entries_list_manager import CodeEntriesListManager


bp = Blueprint("pages", __name__)


def handle_page_redirect(game, page_title, page_url_name, page_template_url):
    dp = CodeEntriesListManager(
        game=game,
        config_path=CONFIG_FILE_PATH
    )
    data = dp.get_data()

    if request.method == 'POST':
        if request.form.get('refresh_data') == 'Refresh data':
            dp.update_data()
            return redirect(url_for(f'pages.{page_url_name}'))

    return render_template(f'home/{page_template_url}', title=page_title, data=data)


@bp.route("/", methods=['GET', 'POST'])
@bp.route("/gi")
def gi_page():
    return handle_page_redirect(
        game="gi",
        page_title="Genshin Impact — HooYooTracker",
        page_url_name="gi_page",
        page_template_url="gi.html"
    )


@bp.route("/zzz", methods=['GET', 'POST'])
def zzz_page():
    return handle_page_redirect(
        game="zzz",
        page_title="Zenless Zone Zero — HooYooTracker",
        page_url_name="zzz_page",
        page_template_url="zzz.html"
    )
