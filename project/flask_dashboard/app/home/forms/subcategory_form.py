from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField,SelectField
from wtforms.validators import DataRequired
from models import Category

class SubcategoryForm(FlaskForm):
    subcategory_id = IntegerField("Категоря №")
    category = SelectField(
        "Категория",
        choices=[(cat.id,cat.category) for cat in Category.select()],
        validators=[DataRequired()]
    )
    subcategory = TextField("Подкатегория", validators=[DataRequired()])
