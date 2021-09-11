from flask import Blueprint,render_template, redirect, url_for, request
from flask_login import login_required, current_user
#from flask_dashboard.app import login_manager
from jinja2 import TemplateNotFound
from models import User
from flask_peewee.utils import PaginatedQuery

user = Blueprint("app_user",__name__)

@user.route("/users/")
@user.route("/users/<int:x>/")
@login_required
def users(**kwargs):
    try:
        index = int(kwargs.get("x",5))
        products = User.select().order_by(User.id.desc())
        pagination = PaginatedQuery(products,index)
        result = pagination.get_list()
        all_count = products.count()
        return render_template(
            "users.html",
            elements=result,
            pagination=pagination,
            index=index,
            page_count = int(all_count/index) + 1 if all_count % index > 0 else int(all_count/index),
            segment="users"
            )
    except TemplateNotFound:
        return render_template('page-404.html'), 404
    except:
        return render_template('page-500.html'), 500   
