from flask import Blueprint,render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
#from flask_dashboard.app import login_manager
from jinja2 import TemplateNotFound
from models import Order, User, UserGrowth, Order, SuperUser, CategStats, SearchStats
from datetime import datetime
from dateutil import relativedelta

main_page = Blueprint("app_main",__name__)

@main_page.route("/main/")
@main_page.route("/dashboard/")
@login_required
def main(**kwargs):
    #try:
    users = User.select().count()
    now = datetime.today()
    print("!!!",now)
    now_month = now.month
    prev = now - relativedelta.relativedelta(months=1)
    prev_month = prev.month
    prev_month_data = UserGrowth.select(UserGrowth.counter).where(UserGrowth.date.month == prev_month)
    now_month_data = UserGrowth.select(UserGrowth.counter).where(UserGrowth.date.month == now_month)
    now_summ = sum((n.counter for n in now_month_data))
    prev_summ = sum((p.counter for p in prev_month_data))
    print(now_summ)
    if prev_summ != 0:
        user_percent = (now_summ - prev_summ)/prev_summ*100
    else:
        user_percent = 0
    now_orders = Order.select(Order.order_summ).where(
        (Order.status == 3) &
        (Order.order_created.month == now_month)
    )
    prev_orders = Order.select(Order.order_summ).where(
        (Order.status == 3) &
        (Order.order_created.month == prev_month)
    )
    now_order_summ = sum((n.order_summ for n in now_orders))
    prev_order_summ = sum((p.order_summ for p in prev_orders))
    if prev_order_summ != 0:
        order_percent = (now_order_summ - prev_order_summ)/prev_order_summ*100
    else:
        order_percent = 0
    all_order_summ = sum((order.order_summ for order in Order.select()))
    categories = CategStats.select().order_by(CategStats.counter.desc())
    admins = SuperUser.select().order_by(SuperUser.full_name)
    good_search = SearchStats.select().where(SearchStats.success == True).order_by(SearchStats.counter.desc()).limit(5)
    bad_search = SearchStats.select().where(SearchStats.success == False).order_by(SearchStats.counter.desc()).limit(5)
    good_search_data = [(s.query,s.counter) for s in good_search]
    bad_search_data = [(s.query,s.counter) for s in bad_search]
    return render_template(
        "dashboard.html",
        segment="dashboard",
        users=users,
        users_percent=user_percent,
        ammount=all_order_summ,
        orders_percent=order_percent,
        categories=categories,
        admins=admins,
        good_search=good_search_data,
        bad_search=bad_search_data
        )
    """except TemplateNotFound:
        return render_template('page-404.html'), 404
    except Exception as e:
        print(e)
        return render_template('page-500.html'), 500 """  


@main_page.route("/searchInfo/")
@login_required
def search_info():
    good_search = SearchStats.select().where(SearchStats.success == True).order_by(SearchStats.counter.desc()).limit(5)
    bad_search = SearchStats.select().where(SearchStats.success == False).order_by(SearchStats.counter.desc()).limit(5)
    return jsonify({
        "good":[s.counter for s in good_search],
        "bad":[s.counter for s in bad_search]
    }),200

@main_page.route("/orderStats/")
@login_required
def order_stats():
    now = datetime.today()
    now_week = now.isocalendar()[1]
    prev = now - relativedelta.relativedelta(months=1)
    prev_week = prev.isocalendar()[1]
    prev_w = Order.select(Order.id).where(Order.order_closed.isocalendar()[1] == prev_week)
    now_week = Order.select(Order.id).where(Order.order_closed.isocalendar()[1] == now_week)
    prev_week_data, now_week_date = [], []
    """if prev_w.count()>0:
        for p in prev_w:"""

