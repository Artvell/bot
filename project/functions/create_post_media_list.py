from aiogram import types
from models import Post
from functions.text_formatter import Formatter
import emoji

def create_media_list():
    result=[]
    for post in Post.select().order_by(Post.id.desc()).limit(3):
        caption_text = Formatter(post).format()
        media_list = []
        for media in post.links:
            photo = types.InputMediaPhoto(
                media=media,
                caption=caption_text,
                parse_mode="HTML"
            )
            media_list.append(photo)
        result.append(media_list)
    return result