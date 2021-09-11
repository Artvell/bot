from aiogram import types
from models import Post
from functions.text_formatter import Formatter
import re

def create_product_message(prod_id=None,side=None, is_superuser=False): #side: True -> ">"  side:False -> "<"
    result=[]
    if prod_id is None:
        if is_superuser:
            post = Post.select().order_by(Post.id.desc()).get()
        else:
            post = Post.select().where(Post.is_visible == True).order_by(Post.id.desc()).get()
    else:
        prod_id = int(prod_id)
        try:
            if side:
                if is_superuser:
                    post = Post.select().where(Post.id<prod_id).order_by(Post.id.desc()).get()
                else:
                    post = Post.select().where(Post.id<prod_id,Post.is_visible == True).order_by(Post.id.desc()).get()
            elif side is False:
                if is_superuser:
                    post = Post.select().where(Post.id>prod_id).get()
                else:
                    post = Post.select().where(Post.id>prod_id,Post.is_visible == True).get()
            elif side is None:
                post = Post.get_or_none(Post.id==prod_id)
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