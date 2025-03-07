from flask import Blueprint, render_template, request, redirect, url_for
from hooyootracker.constants import CONFIG_FILE_PATH, Game
from hooyootracker.data_processor.manager import CodeEntriesListManager

bp = Blueprint("pages", __name__)
dm_genshin = None
dm_zzz = None


def get_manager(game):
    global dm_genshin, dm_zzz
    if game == Game.GENSHIN_IMPACT.value:
        if dm_genshin is None:
            dm_genshin = CodeEntriesListManager(
                game=game,
                config_path=CONFIG_FILE_PATH
            )
        return dm_genshin
    elif game == Game.ZENLESS_ZONE_ZERO.value:
        if dm_zzz is None:
            dm_zzz = CodeEntriesListManager(
                game=game,
                config_path=CONFIG_FILE_PATH
            )
        return dm_zzz


def handle_page_redirect(game, page_title, page_url_name, page_template_url):
    dp = get_manager(game)
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
        game=Game.GENSHIN_IMPACT.value,
        page_title="Genshin Impact — HooYooTracker",
        page_url_name="gi_page",
        page_template_url="gi.html"
    )


@bp.route("/zzz", methods=['GET', 'POST'])
def zzz_page():
    return handle_page_redirect(
        game=Game.ZENLESS_ZONE_ZERO.value,
        page_title="Zenless Zone Zero — HooYooTracker",
        page_url_name="zzz_page",
        page_template_url="zzz.html"
    )
