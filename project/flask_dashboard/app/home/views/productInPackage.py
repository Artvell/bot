from flask import Blueprint,render_template, redirect, url_for, request
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from models import ProductsInPackage, Package, Post
from flask_peewee.utils import PaginatedQuery
productInPack = Blueprint("app_productinpacks",__name__)

@productInPack.route("/productsinpackage/")
@productInPack.route("/productsinpackage/<int:x>/")
@login_required
def productInPacks(**kwargs):
    #try:

    index = int(kwargs.get("x",5))
    packages = Package.select().order_by(Package.id.desc())
    pagination = PaginatedQuery(packages,index)
    result = pagination.get_list()
    ordered_data = []
    for package in packages:
        ordered_data.append(
                {
                    "id":package.id,
                    "title":package.title,
                    "cost":package.cost,
                    "products": ProductsInPackage.select(ProductsInPackage.product).where(ProductsInPackage.package==package)
                }
            )
    all_count = packages.count()
    return render_template(
        "productInPack.html",
        elements=ordered_data,
        pagination=pagination,
        index=index,
        page_count = int(all_count/index) + 1 if all_count % index > 0 else int(all_count/index),
        segment="prodInPack"
        )
    """except TemplateNotFound:
        return render_template('page-404.html'), 404
    except:
        return render_template('page-500.html'), 500"""  

@productInPack.route("/add_product/", methods = ["POST"])
@login_required
def add_to_package():
    package_id = request.json.get("pack_id")
    product_id = request.json.get("prod_id")
    print(package_id, product_id)
    package = Package.get_or_none(Package.id == package_id)
    product = Post.get_or_none(Post.id == product_id)
    if package is not None and product is not None:
        status,_ = ProductsInPackage.get_or_create(
            package=package,
            product=product
            )
        return {"status":"Ok"}, 200
    else:
        return {"status":"error"},401

@productInPack.route("/delete_product_from_pack/", methods=["POST"])
@login_required
def delete_from_package():
    package_id = request.json.get("pack_id")
    product_id = request.json.get("prod_id")
    package = Package.get_or_none(Package.id == package_id)
    product = Post.get_or_none(Post.id == product_id)
    if package is not None and product is not None:
        prodInPack = ProductsInPackage.get_or_none((ProductsInPackage.package == package) & (ProductsInPackage.product == product))
        if prodInPack is not None:
            prodInPack.delete_instance()
            return {"status":"deleted"}, 200
        else:
            return {"status":"Not found"}, 404
    else:
        return {"status":"error"},401