from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField
from wtforms.validators import DataRequired

class CategoryForm(FlaskForm):
    category_id = IntegerField("Категоря №")
    category = TextField("Категория", validators=[DataRequired()])