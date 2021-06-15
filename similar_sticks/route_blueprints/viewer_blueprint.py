from flask import Blueprint, current_app, render_template


viewer_pages = Blueprint('wah_look_at_me', __name__)


@viewer_pages.route("/")
def hello_world():
    csv_service = current_app.config['CSV_DATA_SERVICE']
    return render_template('base.html', models=csv_service.unique_models)
