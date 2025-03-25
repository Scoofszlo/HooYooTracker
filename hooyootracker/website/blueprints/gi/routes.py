from flask import Blueprint, render_template, request, redirect, url_for
from hooyootracker.constants import Game
from hooyootracker.codeentrieslist.manager import CodeEntriesListManager

gi = Blueprint("gi", __name__, template_folder="templates", static_folder="static", url_prefix="/gi")
dm_genshin = None


@gi.route("/", methods=['GET', 'POST'])
def gi_page():
    global dm_genshin

    if dm_genshin is None:
        dm_genshin = CodeEntriesListManager(game=Game.GENSHIN_IMPACT.value)

    dp = dm_genshin
    data = dp.get_data()

    if request.method == 'POST':
        if request.form.get('refresh_data') == 'Refresh data':
            dp.update_data()
            return redirect(url_for('gi.gi_page'))

    return render_template('gi/gi.html', title="Genshin Impact — HooYooTracker", data=data)
