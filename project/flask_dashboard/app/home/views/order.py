from flask import Blueprint,render_template, redirect, url_for, request,jsonify
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from models import Order, Route
from flask_dashboard.app.home.forms import OrderForm
import base64
from datetime import datetime, timedelta
from flask_peewee.utils import PaginatedQuery

order = Blueprint("app_order",__name__)

@order.route("/transactions/")
@order.route("/transactions/<int:x>/")
@order.route("/transaction/<int:order>/")
@login_required
def orders(**kwargs):
    #try:
    index = int(kwargs.get("x",5))
    order_id = kwargs.get("order","!")
    if order_id != "!":
        orders = Order.select().where(Order.id == order_id)
    else:
        orders = Order.select()
    pagination = PaginatedQuery(orders,index)
    result = pagination.get_list()
    routes = []
    drivers = []
    for order in result:
        route = Route.get_or_none(Route.order == order)
        if route is not None:
            routes.append(f"/map/{route.uuid}")
            drivers.append(route.driver.phone)
        else:
            routes.append(None)
            drivers.append(None)
    all_count = orders.count()
    return render_template(
        "transactions.html",
        elements=result,
        pagination=pagination,
        index=index,
        page_count = int(all_count/index) + 1 if all_count % index > 0 else int(all_count/index),
        routes=routes,
        phones=drivers,
        form=OrderForm(),
        segment="transactions"
        )
    """except TemplateNotFound:
        return render_template('page-404.html'), 404
    except:
        return render_template('page-500.html'), 500   """

@order.route("/order/delete/",methods = ['POST'])
@login_required
def delete_order():
    order_id = request.form.get("order_id")
    try:
        order = Order.get_or_none(Order.id == order_id)
        if order is not None:
            order.delete_instance()
            return "Ok"
        else:
            return "No"
    except TemplateNotFound:
        return render_template('page-404.html'), 404
    except Exception as e:
        print(e)
        return render_template('page-500.html'), 500

@order.route("/order/change/",methods = ['POST'])
@login_required
def change_order():
    #order_id = request.form.get("order_id")
    print(request.form)
    print(request.args)
    order_id = request.form["order_id"]
    print("!! ",order_id)
    status = request.form["status"]
    order_type = request.form["order_type"]
    payment_status = request.form["payment_status"]
    form = OrderForm()
    try:
        order = Order.get_or_none(Order.id == order_id)
        if order is not None and form.validate_on_submit():
            order.status = status
            order.order_type = order_type
            order.payment_status = payment_status
            if int(status) == 3:
                order.order_closed = datetime.now()
            order.save()
            return "Ok"
        else:
            return "No"
    except TemplateNotFound:
        return render_template('page-404.html'), 404
    except Exception as e:
        print(e)
        return render_template('page-500.html'), 500


@order.route("/order_list/<int:quantity>/")
@login_required
def order_list(quantity):
    #quantity = int(kwargs.get("quantity",7))
    min_date = datetime.today() - timedelta(days=quantity)
    orders = Order.select().where(Order.order_created > min_date)
    data = {}
    if orders.count()>0:
        tmp_date = orders[0].order_created
        data[orders[0].order_created.strftime("%m/%d/%Y")] = 1
        for order in orders:
            if order.order_created == tmp_date:
                data[order.order_created.strftime("%m/%d/%Y")] += 1
            else:
                tmp_date = order.order_created
                data[order.order_created.strftime("%m/%d/%Y")] = 1
    print(data)
    return jsonify(data),200


@order.route("/get_order/", methods = ["GET"])
@login_required
def get_order():
    status = {
        1:"предзаказ",
        2:"выполняется",
        3:"закрыт",
        4:"ожидает оплаты"
    }
    term = request.args.get("term","!")
    orders = Order.select(Order.id, Order.order_created, Order.status).where(Order.id == term)
    data = [{"value":p.id,"label":f"Заказ №{p.id} ({status[p.status]}) от {p.order_created}"} for p in orders]
    #data = [p.name for p in products]

    return jsonify(data),200