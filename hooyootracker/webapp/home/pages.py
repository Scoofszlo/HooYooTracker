from flask import Blueprint, render_template, request, redirect, url_for
from hooyootracker.constants import CONFIG_FILE_PATH
from hooyootracker.data_processor.presenter import DataPresenter


bp = Blueprint("pages", __name__)


@bp.route("/", methods=['GET', 'POST'])
@bp.route("/gi")
def home():
    dp = DataPresenter(
        game="gi",
        config_path=CONFIG_FILE_PATH
    )
    data = dp.get_data()

    if request.method == 'POST':
        if request.form.get('refresh_data_gi') == 'Refresh data':
            dp.update_data()
            return redirect(url_for('pages.home'))

    return render_template('gi.html', title='Genshin Impact — HooYooTracker', data=data)


@bp.route("/zzz", methods=['GET', 'POST'])
def zzz_page():
    dp = DataPresenter(
        game="zzz",
        config_path=CONFIG_FILE_PATH
    )
    data = dp.get_data()

    if request.method == 'POST':
        if request.form.get('refresh_data_zzz') == 'Refresh data':
            dp.update_data()
            return redirect(url_for('pages.zzz_page'))

    return render_template('zzz.html', title='ZZZ — HooYooTracker', data=data)
