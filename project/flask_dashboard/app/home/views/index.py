from flask import Blueprint,render_template, redirect, url_for, request
from flask_login import login_required, current_user
#from flask_dashboard.app import login_manager
from jinja2 import TemplateNotFound

index_page = Blueprint("app_index",__name__)

@index_page.route('/index/')
#@login_required
def index():
    return render_template('index.html', segment='index')