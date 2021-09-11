from aiogram import types
from models import Post, Category, Subcategory, CategStats
from functions.text_formatter import Formatter
import re

def product_message_by_category(parameter,flag,prod_id=None,side=None, is_superuser=False): #side: True -> ">"  side:False -> "<" | flag:True - category, False: subcategory
    result=[]
    print(parameter)
    if flag:
        query_field = Post.category
        category = Category.get_by_id(parameter)
        stats,created = CategStats.get_or_create(name=category.category)
        if not created:
            stats.pagination_counter += 1
            stats.save()
    else:
        query_field = Post.subcategory
        subcategory = Subcategory.get_by_id(parameter)
        stats,created = CategStats.get_or_create(name=subcategory.subcategory)
        if not created:
            stats.pagination_counter += 1
            stats.save()
    if prod_id is None:
        try:
            if is_superuser:
                post = Post.select().where(query_field==parameter).order_by(Post.id.desc()).get()
            else:
                post = Post.select().where(query_field==parameter,Post.is_visible == True).order_by(Post.id.desc()).get()
        except Post.DoesNotExist:
            post = None
    else:
        prod_id = int(prod_id)
        try:
            if side:
                if is_superuser:
                    post = Post.select().where(Post.id<prod_id,query_field==parameter).order_by(Post.id.desc()).get()
                else:
                    post = Post.select().where(Post.id<prod_id,query_field==parameter,Post.is_visible==True).order_by(Post.id.desc()).get()
            elif side is False:
                if is_superuser:
                    post = Post.select().where(Post.id>prod_id, query_field==parameter).get()
                else:
                    post = Post.select().where(Post.id>prod_id, query_field==parameter,Post.is_visible==True).get()
            elif side is None:
                post = Post.get_or_none(Post.id==prod_id, query_field==parameter)
        except Post.DoesNotExist:
            post = None
    if post is None:
        return False,False,False
    else:
        formatter = Formatter(post)
        caption_text = formatter.format()
        photo_url = post.links[0]
        if post.telegraph is None or post.telegraph == "":
            post.telegraph = re.search(r"https://telegra\.ph/[A-Za-z0-9_-]*",formatter.post_to_telegraph()).group(0)
            post.save()
        return photo_url,caption_text, post.id