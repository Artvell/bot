from flask import Blueprint,render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from models import Category, Post
from flask_dashboard.app.home.forms import CategoryForm
from flask_peewee.utils import PaginatedQuery

category = Blueprint("app_categories",__name__)

@category.route("/categories/")
@category.route("/categories/<int:x>/")
@category.route("/category/<int:category>/")
@login_required
def categories(**kwargs):
    #try:
    index = int(kwargs.get("x",5))
    category_id = kwargs.get("category","!")
    if category_id != "!":
        products = Category.select().where(Category.id == category_id)
    else:
        products = Category.select()
    pagination = PaginatedQuery(products,index)
    result = pagination.get_list()
    all_count = products.count()
    form = CategoryForm()
    return render_template(
        "categories.html",
        elements=result,
        index=index,
        page_count = int(all_count/index) + 1 if all_count % index > 0 else int(all_count/index),
        segment="categories",
        form=form,
        pagination = pagination
        )
    """except TemplateNotFound:
        return render_template('page-404.html'), 404
    except:
        return render_template('page-500.html'), 500"""   

@category.route("/category/delete/",methods = ['POST'])
@login_required
def delete_category():
    category_id = request.form.get("category_id")
    try:
        category = Category.get_or_none(Category.id == category_id)
        if category is not None:
            category.delete_instance()
            return "Ok"
        else:
            return "No"
    except TemplateNotFound:
        return render_template('page-404.html'), 404
    except Exception as e:
        print(e)
        return render_template('page-500.html'), 500

@category.route("/category/change/",methods = ['POST'])
@login_required
def change_category():
    category_id = request.form.get("category_id", None)
    category_text = request.form["category"]
    form = CategoryForm()
    try:
        if category_id is None:
            Category.create(category=category_text)
            return "Ok"
        else:
            category = Category.get_or_none(Category.id == category_id)
            if category is not None and form.validate_on_submit():
                category.category = category_text
                category.save()
                return "Ok"
            else:
                return "No"
    except TemplateNotFound:
        return render_template('page-404.html'), 404
    except Exception as e:
        print(e)
        return render_template('page-500.html'), 500


@category.route("/get_category/", methods = ["GET"])
@login_required
def get_category():
    name = request.args.get("term","!")
    categories = Category.select(Category.id, Category.category).where(Category.category.contains(name))
    data = [{"value":p.id,"label":p.category} for p in categories]
    #data = [p.name for p in products]
    return jsonify(data),200