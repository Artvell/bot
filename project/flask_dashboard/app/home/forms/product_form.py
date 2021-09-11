from flask_wtf import FlaskForm
from wtforms import IntegerField, TextField, SelectField, BooleanField, FloatField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Regexp
from wtforms.widgets import TextArea
from models import Category, Subcategory

class ProductForm(FlaskForm):
    product_id = IntegerField("Товар №")
    name = TextField("Название",validators=[DataRequired()])
    category = SelectField(
        "Категория",
        choices= [(cat.id,cat.category) for cat in Category.select()],
    )
    subcategory = SelectField(
        "Подкатегория",
        choices = []
    )
    telegraph = TextField(
        'Ссылка*', 
        validators=[
            Regexp('^(http|https):\/\/[\w.\-]+(\.[\w.\-]+)+.*$', 0,
                'Неверный формат ссылки')]
    )
    cost = FloatField("Цена: ", validators=[DataRequired()])
    is_available = BooleanField("Есть в наличии: ")
    is_visible = BooleanField("Отображать в боте: ")
    text = TextAreaField("Описание",validators=[DataRequired()])
    submit = SubmitField("Отправить")

    def choices_for_subcategory(self,categ_id):
        self.subcategory.choices = [(sub.id,sub.subcategory) for sub in Subcategory.select().where(Subcategory.category == categ_id)]

    

