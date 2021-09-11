# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import jsonify, render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

from flask_dashboard.app import login_manager
from flask_dashboard.app.base import blueprint
from flask_dashboard.app.base.forms import LoginForm, CreateAccountForm
#from app.base.models import User
from models import SuperUser
from flask_dashboard.app.base.util import verify_user

#from flask_dashboard.app.base.util import verify_pass

@login_manager.user_loader
def user_loader(user_id):
    return SuperUser.get(user_id)

@login_manager.request_loader
def request_loader(request):
    user_id = request.form.get('user_id')
    user = SuperUser.get_or_none(SuperUser.user_id == user_id)
    return user if user else None

@blueprint.route('/')
def route_default():
    return redirect(url_for('base_blueprint.login'))

## Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if len(request.args) > 0 :
        tg_data = {
            "id" : request.args.get('id',None),
            "first_name" : request.args.get('first_name',None),
            "last_name" : request.args.get('last_name', None),
            "username" : request.args.get('username', None),
            "photo_url" : request.args.get('photo_url',None),
            "auth_date":  request.args.get('auth_date', None),
            "hash" : request.args.get('hash',None)
        }
        print(tg_data)
        res = verify_user(tg_data)
        print(res)
        if res:
            user = SuperUser.get_or_none(SuperUser.user_id == tg_data["id"])
            if user is not None:
                if tg_data["photo_url"] is not None:
                    if user.icon != tg_data["photo_url"]:
                        user.icon = tg_data["photo_url"]
                        user.save()
                login_user(user)
                return redirect(url_for('base_blueprint.route_default'))
            else:
                return render_template( 'accounts/login.html', msg='Отказано в доступе, Вы не администратор')
        else:
            return render_template( 'accounts/login.html', msg='Неверные параметры')
    if not current_user.is_authenticated:
        return render_template( 'accounts/login.html')
    return redirect(url_for('app_main.main'))


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('base_blueprint.login'))

@blueprint.route('/shutdown')
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

## Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    #return render_template('page-403.html'), 403
    return redirect(url_for('base_blueprint.login'))

@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('page-403.html'), 403

@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('page-404.html'), 404

@blueprint.errorhandler(500)
def internal_error(error):
    print("Скакнули сюда")
    return render_template('page-500.html'), 500
