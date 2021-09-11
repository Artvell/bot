from flask import Blueprint,render_template, redirect, url_for, request
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from models import Driver
from flask_dashboard.app.home.forms import DriverForm
from flask_peewee.utils import PaginatedQuery

driver = Blueprint("app_drivers",__name__)

@driver.route("/drivers/")
@driver.route("/drivers/<int:page>/")
@driver.route("/drivers/<int:page>/<int:x>/")
@login_required
def drivers(**kwargs):
    #try:
    index = int(kwargs.get("x",5))
    products = Driver.select().order_by(Driver.id.desc())
    pagination = PaginatedQuery(products,index)
    result = pagination.get_list()
    all_count = products.count()
    form = DriverForm()
    return render_template(
        "drivers.html",
        elements=result,
        index=index,
        page_count = int(all_count/index) + 1 if all_count % index > 0 else int(all_count/index),
        segment="drivers",
        form = form,
        pagination = pagination
        )
    #except TemplateNotFound:
    #    return render_template('page-404.html'), 404
    #except:
    #    return render_template('page-500.html'), 500


@driver.route("/driver/delete/",methods = ['POST'])
@login_required
def delete_driver():
    driver_id = request.form.get("driver_id")
    try:
        driver = Driver.get_or_none(Driver.id == driver_id)
        if driver is not None:
            driver.delete_instance()
            return "Ok"
        else:
            return "No"
    except TemplateNotFound:
        return render_template('page-404.html'), 404
    except Exception as e:
        print(e)
        return render_template('page-500.html'), 500

@driver.route("/driver/change/",methods = ['POST'])
@login_required
def change_driver():
    print(request.form)
    driver_id = request.form.get("driver_id", None)
    driver_phone = request.form["phone"]
    form = DriverForm()
    try:
        if driver_id is None:
            Driver.create(
                phone = driver_phone,
                password = Driver.generate_pass()
                )
            return "Ok"
        else:
            driver = Driver.get_or_none(Driver.id == driver_id)
            if driver is not None and form.validate_on_submit():
                driver.phone = driver_phone
                driver.save()
                return "Ok"
            else:
                return "No"
    except TemplateNotFound:
        return render_template('page-404.html'), 404
    except Exception as e:
        print(e)
        return render_template('page-500.html'), 500