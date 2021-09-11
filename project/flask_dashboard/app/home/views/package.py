from flask import Blueprint,render_template, redirect, url_for, request
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from models import Package
from flask_dashboard.app.home.forms import PackageForm
from flask_peewee.utils import PaginatedQuery

package = Blueprint("app_packages",__name__)

@package.route("/packages/")
@package.route("/packages/<int:x>/")
@login_required
def packages(**kwargs):
    #try:
    index = int(kwargs.get("x",5))
    products = Package.select().order_by(Package.id.desc())
    pagination = PaginatedQuery(products,index)
    result = pagination.get_list()
    all_count = products.count()
    form = PackageForm()
    return render_template(
        "packages.html",
        elements=result,
        pagination=pagination,
        index=index,
        page_count = int(all_count/index) + 1 if all_count % index > 0 else int(all_count/index),
        segment="packages",
        form = form
        )
    """except TemplateNotFound:
        return render_template('page-404.html'), 404
    except:
        return render_template('page-500.html'), 500"""  


@package.route("/package/delete/",methods = ['POST'])
@login_required
def delete_package():
    package_id = request.form.get("package_id")
    try:
        package = Package.get_or_none(Package.id == package_id)
        if package is not None:
            package.delete_instance()
            return "Ok"
        else:
            return "No"
    except TemplateNotFound:
        return render_template('page-404.html'), 404
    except Exception as e:
        print(e)
        return render_template('page-500.html'), 500

@package.route("/package/change/",methods = ['POST'])
@login_required
def change_package():
    print(request.form)
    package_id = request.form.get("package_id", None)
    title = request.form["title"]
    cost = request.form["cost"]
    form = PackageForm()
    try:
        if package_id is None:
            Package.create(title=title,cost=cost)
            return "Ok"
        else:
            package = Package.get_or_none(Package.id == package_id)
            if package is not None and form.validate_on_submit():
                package.title = title
                package.cost = cost
                package.save()
                return "Ok"
            else:
                return "No"
    except TemplateNotFound:
        return render_template('page-404.html'), 404
    except Exception as e:
        print(e)
        return render_template('page-500.html'), 500