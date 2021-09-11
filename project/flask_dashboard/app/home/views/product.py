from flask import Blueprint,render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from models import Post, Category, Subcategory
from flask_dashboard.app.home.forms import ProductForm
from flask_peewee.utils import PaginatedQuery

product = Blueprint("app_product",__name__)

@product.route("/products/")
@product.route("/products/<int:x>/")
@product.route("/product/<int:product>/")
@login_required
def products(**kwargs):
    #try:
    index = int(kwargs.get("x",5))
    product_id = kwargs.get("product","!")
    if product_id != "!":
        products = Post.select().where(Post.id == product_id).order_by(Post.id.desc())
    else:
        products = Post.select().order_by(Post.id.desc())
    pagination = PaginatedQuery(products,index)
    result = pagination.get_list()
    all_count = products.count()
    return render_template(
        "products.html",
        elements=result,
        index=index,
        page_count = int(all_count/index) + 1 if all_count % index > 0 else int(all_count/index),
        segment="products",
        form=ProductForm(),
        pagination = pagination
        )
    """except TemplateNotFound:
        return render_template('page-404.html'), 404
    except Exception as e:
        print(e)
        return render_template('page-500.html'), 500"""


@product.route("/product/subcateg/",methods = ['POST'])
@login_required
def subcateg():
    categ_id = request.json.get("categ_id")
    data = [[sub.id,sub.subcategory] for sub in Subcategory.select().where(Subcategory.category==categ_id)]
    return jsonify(data),200


@product.route("/product/delete/",methods = ['POST'])
@login_required
def delete_order():
    product_id = request.form.get("product_id")
    try:
        product = Post.get_or_none(Post.id == product_id)
        if product is not None:
            product.delete_instance()
            return "Ok"
        else:
            return "No"
    except TemplateNotFound:
        return render_template('page-404.html'), 404
    except Exception as e:
        print(e)
        return render_template('page-500.html'), 500

@product.route("/get_product/", methods = ["GET"])
@login_required
def get_product():
    name = request.args.get("term","!")
    products = Post.select(Post.id, Post.name, Post.links).where(Post.name.contains(name))
    data = [{"value":p.id,"label":p.name,"icon":p.links[0],"cost":p.cost} for p in products]
    #data = [p.name for p in products]
    return jsonify(data),200

@product.route("/product/change/", methods = ['POST'])
@login_required
def change_product():
    #order_id = request.form.get("order_id")
    post_id = request.form["product_id"]
    name = request.form["name"]
    telegraph = request.form["telegraph"]
    cost = request.form["cost"]
    is_available = True if request.form.get("is_available",False) == "y" else False
    is_visible = True if request.form.get("is_visible",False) == "y" else False
    category = request.form.get("category", None)
    subcategory = request.form.get("subcategory", None)
    links = request.form.getlist("links[]")
    text = request.form.get("text"," ")
    print("@@ ",links)
    form = ProductForm()
    try:
        product = Post.get_or_none(Post.id == post_id)
        if product is not None:
            product.name = name
            product.telegraph = telegraph
            product.links = links
            product.category = category
            product.subcategory = subcategory
            product.cost = cost
            product.is_available = is_available
            product.is_visible = is_visible
            product.save()
            return "Ok"
        else:
            return "No"
    except TemplateNotFound:
        return render_template('page-404.html'), 404
    except Exception as e:
        print(e)
        return render_template('page-500.html'), 500