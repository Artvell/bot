# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_dashboard.app.home import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from flask_dashboard.app import login_manager
from jinja2 import TemplateNotFound
from models import Order

@blueprint.route('/index')
#@login_required
def index():
    print("zzzz")
    return render_template('index.html', segment='index')









# Helper - Extract current page name from request 
def get_segment( request ): 

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment    

    except:
        return None  
