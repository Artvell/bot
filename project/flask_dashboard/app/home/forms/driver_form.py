from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField
from wtforms.validators import DataRequired

class DriverForm(FlaskForm):
    driver_id = IntegerField("Водитель №")
    phone = TextField("Телефон", validators=[DataRequired()])