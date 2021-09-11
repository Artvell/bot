from flask import Blueprint,render_template, redirect, url_for, request
from flask_login import login_required, current_user
#from flask_dashboard.app import login_manager
from jinja2 import TemplateNotFound
from models import Route
from flask_dashboard.app.home.forms import RouteForm
from flask_peewee.utils import PaginatedQuery
route = Blueprint("app_routes",__name__,template_folder='templates')

@route.route("/routes/")
@route.route("/routes/<int:x>/")
@login_required
def routes(**kwargs):
    #try:
    index = int(kwargs.get("x",5))
    products = Route.select().order_by(Route.id.desc())
    pagination = PaginatedQuery(products,index)
    result = pagination.get_list()
    all_count = products.count()
    form = RouteForm()
    return render_template(
        "routes.html",
        elements=result,
        pagination=pagination,
        index=index,
        page_count = int(all_count/index) + 1 if all_count % index > 0 else int(all_count/index),
        segment="routes",
        form = form
        )
    """except TemplateNotFound:
        return render_template('page-404.html'), 404
    except:
        return render_template('page-500.html'), 500"""


@route.route("/route/delete/",methods = ['POST'])
@login_required
def delete_route():
    route_id = request.form.get("route_id")
    try:
        route = Route.get_or_none(Route.id == route_id)
        if route is not None:
            route.delete_instance()
            return "Ok"
        else:
            return "No"
    except TemplateNotFound:
        return render_template('page-404.html'), 404
    except Exception as e:
        print(e)
        return render_template('page-500.html'), 500

@route.route("/route/change/",methods = ['POST'])
@login_required
def change_route():
    print(request.form)
    route_id = request.form.get("route_id", None)
    route_status = request.form["status"]
    form = RouteForm()
    try:
        route = Route.get_or_none(Route.id == route_id)
        if route is not None and form.validate_on_submit():
            route.status = route_status
            route.save()
            return "Ok"
        else:
            return "No"
    except TemplateNotFound:
        return render_template('page-404.html'), 404
    except Exception as e:
        print(e)
        return render_template('page-500.html'), 500