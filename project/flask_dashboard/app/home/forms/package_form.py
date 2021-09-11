from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField,FloatField
from wtforms.validators import DataRequired

class PackageForm(FlaskForm):
    package_id = IntegerField("Пакет №")
    title = TextField("Название", validators=[DataRequired()])
    cost = FloatField("Цена", validators=[DataRequired()] )