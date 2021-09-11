"""Файл с пасером инсты"""
from instagram_private_api import Client, ClientCompatPatch
from functions import config
from models import Post, Story
import emoji
from datetime import datetime
import re

class Parser:
    """
    класс для получения данных со странице в инсте
    login,password - данные юзера, под которым просматриваем страницы(берутся из config.py)
    name - аккаунт, который просматриваем
    """
    def __init__(self, name):
        self.api = Client(config.login, config.password)
        self.name = name
        """try:
            self.last_post = Post.select().order_by(Post.id.desc()).get()
        except Post.DoesNotExist:
            self.last_post = None"""
        try:
            self.last_story = Story.select().order_by(Story.id.desc()).get()
        except Story.DoesNotExist:
            self.last_story = None

    def get_last_data(self,feed,last_current_element):
        data = []
        flag = True
        if last_current_element is not None:
            for elem in feed:
                if datetime.fromtimestamp(elem["taken_at"])>last_current_element.created_at:
                    data.append(elem)
                else:
                    flag = False
                    break
        else:
            data.extend(feed)
        return data, flag

    def get_feed(self) -> int:
        """Функция для получения постов со стены"""
        updates = []
        results = self.api.username_feed(self.name)
        #new_posts, flag = self.get_last_data(feed,self.last_post)
        updates.extend(results.get("items",[]))
        next_max_id = results.get('next_max_id')
        while next_max_id:
            results = self.api.username_feed(self.name, max_id=next_max_id)
            updates.extend(results.get("items",[]))
            next_max_id = results.get('next_max_id')
        number = len(updates)
        deleted = 0
        for i in range(len(updates)-1,-1,-1):
            links = []
            post = updates[i]
            instagram_id = post["pk"]
            all_likes = post['like_count']
            status = post.get('comments_disabled',False)
            if not status:
                comments_count = post['comment_count']
            else:
                comments_count = 0
            all_views = post.get("view_count",-1)
            if all_views != -1:
                number-=1
                continue
            product, created = Post.get_or_create(instagram_id=instagram_id)
            if post["media_type"] == 8:
                for media in post.get("carousel_media",[]):
                    links.append(media["image_versions2"]["candidates"][0]["url"])
            else:
                links.append(post["image_versions2"]["candidates"][0]["url"])
            
            if created:
                try:
                    name = re.search("[a-zA-Z][a-zA-Z+. ]*",post.get("caption",{}).get("text","Нет описания")).group(0)
                except AttributeError:
                    name = post.get("caption",{}).get("text","Нет описания")[:30]
                product.name = name
                product.text = post.get("caption",{}).get("text","Нет описания")
                product.likes = all_likes
                product.comments = comments_count
                product.links = links
                product.save()
            else:
                product.likes = all_likes
                product.comments = comments_count
                product.links = links
                product.save()
        return number
    
    def get_story(self) -> int:
        updates = []
        stories = self.api.user_reel_media(10513555878)
        stories_list = stories.get("items",[])
        new_stories, flag = self.get_last_data(stories_list[::-1],self.last_story)
        for story in new_stories[::-1]:
            if story["media_type"] == 2:
                Story.create(
                    created_at = story["taken_at"],
                    link=story["video_versions"][0]["url"],
                    expiry_time = story["expiring_at"],
                    type = 2
                )
            elif story["media_type"] == 1:
                Story.create(
                    created_at = story["taken_at"],
                    link=story["image_versions2"]["candidates"][0]["url"],
                    expiry_time=story["expiring_at"],
                    type=1
                )
        return len(new_stories)


#Parser("beauty_care.uz").get_story()