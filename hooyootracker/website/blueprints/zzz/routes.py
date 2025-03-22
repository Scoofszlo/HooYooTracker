from flask import Blueprint, render_template, request, redirect, url_for
from hooyootracker.constants import Game
from hooyootracker.codeentrieslist.manager import CodeEntriesListManager

zzz = Blueprint("zzz", __name__, template_folder="templates", static_folder="static", url_prefix="/zzz")
dm_zzz = None


@zzz.route("/", methods=['GET', 'POST'])
def zzz_page():
    global dm_zzz

    if dm_zzz is None:
        dm_zzz = CodeEntriesListManager(game=Game.ZENLESS_ZONE_ZERO.value)

    dp = dm_zzz
    data = dp.get_data()

    if request.method == 'POST':
        if request.form.get('refresh_data') == 'Refresh data':
            dp.update_data()
            return redirect(url_for('zzz.zzz_page'))

    return render_template('zzz/zzz.html', title="Zenless Zone Zero — HooYooTracker", data=data)
