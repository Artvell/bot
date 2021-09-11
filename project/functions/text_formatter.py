"""файл с классом для форматирования текста постов"""
import re
from telegraph import Telegraph
from models import Post
from emoji import emojize
class Formatter:
    """класс для форматирования текста постов"""
    def __init__(self,post):
        self.post = post
        self.text = emojize(self.post.text.replace("Корейскаякосметика","Корейскаякосметика"))
        self.post_to_telegraph()
    def get_name(self) -> str:
        """Извлекает название товара"""
        try:
            name = re.search("[a-zA-Z][a-zA-Z+. ]*",self.text).group(0)
        except AttributeError:
            name =""
        return name

    def get_tags(self) -> str:
        """Извлекает хештэги"""
        tags = self.text.split("#")
        return "#"+" #".join(tags[1::]).strip()

    def get_title(self) -> str:
        """извлекает первый абзац описания"""
        title = self.text.split("\n")
        return title[0].strip()

    def get_volume(self) -> str:
        """Извлекает строчку с объемом
        Делает ее жирной
        """
        try:
            found = re.search('(.+?)Объем(.+?)мл', self.text).group(0)
            found = f"<b>{found}</b>"
        except AttributeError:
            found = ''
        return found
    def get_delivery(self) -> str:
        """Извлекает строку с доставкой. Делает ее жирной"""
        try:
            found = re.search('(.+?)Имеется доставка', self.text).group(0)
            found = f"<b>{found}</b>"
        except AttributeError:
            found = ''
        return found
    def post_to_telegraph(self) -> str:
        """Постит информацию в telegra.ph. Возвращает ссылку на пост"""
        if self.post.telegraph is None or self.post.telegraph == "":
            telegraph = Telegraph()
            telegraph.create_account(short_name='1337')
            images = ""
            for media in self.post.links:
                images += f'<img src="{media}">'
            response = telegraph.create_page(
                title=self.get_name(),
                html_content=f'{images}<p>{self.text}</p>'
            )
            self.post.telegraph = "https://telegra.ph/{}".format(response['path'])
            self.post.save()
            return '<a href="https://telegra.ph/{}">Подробнее...</a>'.format(response['path'])
        else:
            return '<a href="{}">Подробнее...</a>'.format(self.post.telegraph)
    def format(self) -> str:
        """Форматирует текст всеми методами"""
        is_available = "Есть в наличии" if self.post.is_available else "Нет в наличии"
        final_text = f"{self.get_title()}\nЦена: {self.post.cost} сум\n{self.get_volume()}\n{self.get_delivery()}\n<b>{is_available}</b>\n{self.post_to_telegraph()}"
        return final_text
