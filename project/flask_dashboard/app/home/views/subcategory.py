from flask import Blueprint,render_template, redirect, url_for, request
from flask_login import login_required, current_user
#from flask_dashboard.app import login_manager
from jinja2 import TemplateNotFound
from models import Subcategory
from flask_dashboard.app.home.forms import SubcategoryForm
from flask_peewee.utils import PaginatedQuery

subcategory = Blueprint("app_subcategories",__name__)

@subcategory.route("/subcategories/")
@subcategory.route("/subcategories/<int:x>/")
@login_required
def subcategories(**kwargs):
    #try:
    index = int(kwargs.get("x",5))
    products = Subcategory.select().order_by(Subcategory.id.desc())
    pagination = PaginatedQuery(products,index)
    result = pagination.get_list()
    all_count = products.count()
    form = SubcategoryForm()
    return render_template(
        "subcategories.html",
        elements=result,
        pagination=pagination,
        index=index,
        page_count = int(all_count/index) + 1 if all_count % index > 0 else int(all_count/index),
        segment="subcategories",
        form = form
        )
    """except TemplateNotFound:
        return render_template('page-404.html'), 404
    except:
        return render_template('page-500.html'), 500"""


@subcategory.route("/subcategory/delete/",methods = ['POST'])
@login_required
def delete_subcategory():
    subcategory_id = request.form.get("subcategory_id")
    try:
        subcategory = Subcategory.get_or_none(Subcategory.id == subcategory_id)
        if subcategory is not None:
            subcategory.delete_instance()
            return "Ok"
        else:
            return "No"
    except TemplateNotFound:
        return render_template('page-404.html'), 404
    except Exception as e:
        print(e)
        return render_template('page-500.html'), 500

@subcategory.route("/subcategory/change/",methods = ['POST'])
@login_required
def change_subcategory():
    print(request.form)
    subcategory_id = request.form.get("subcategory_id", None)
    category = request.form["category"]
    subcategory_text = request.form["subcategory"]
    form = SubcategoryForm()
    try:
        if subcategory_id is None:
            status = Subcategory.create(category=category,subcategory=subcategory_text)
            print(status)
            return "Ok"
        else:
            subcategory = Subcategory.get_or_none(Subcategory.id == subcategory_id)
            if category is not None and form.validate_on_submit():
                subcategory.category = category
                subcategory.subcategory = subcategory_text
                subcategory.save()
                return "Ok"
            else:
                return "No"
    except TemplateNotFound:
        return render_template('page-404.html'), 404
    except Exception as e:
        print(e)
        return render_template('page-500.html'), 500