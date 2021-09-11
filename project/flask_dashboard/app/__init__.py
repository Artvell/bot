# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Flask, url_for
from flask_login import LoginManager
#from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from logging import basicConfig, DEBUG, getLogger, StreamHandler
from os import path
from flask_dashboard.app.home.views import (
    order,
    product,
    category,
    subcategory,
    user,
    driver,
    route,
    package,
    productInPack,
    index_page,
    main_page
)
login_manager = LoginManager()
from flask_dashboard.app.base.routes import blueprint
from flask_dashboard.app.home.routes import blueprint as bp

#db = SQLAlchemy()


def register_extensions(app):
    #db.init_app(app)
    login_manager.init_app(app)

def register_blueprints(app):
    app.register_blueprint(blueprint)
    app.register_blueprint(bp)
    app.register_blueprint(index_page)
    app.register_blueprint(order)
    app.register_blueprint(product)
    app.register_blueprint(category)
    app.register_blueprint(subcategory)
    app.register_blueprint(user)
    app.register_blueprint(driver)
    app.register_blueprint(route)
    app.register_blueprint(package)
    app.register_blueprint(productInPack)
    app.register_blueprint(main_page)

"""def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()
"""
def create_app(config):
    app = Flask(__name__, static_folder='base/static')
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    #configure_database(app)
    return app
