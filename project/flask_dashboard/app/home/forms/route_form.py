from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField
from wtforms.validators import DataRequired

class RouteForm(FlaskForm):
    route_id = IntegerField("Категоря №")
    status = SelectField(
        "Категория", 
        validators=[DataRequired()],
        choices=[(1,"Выполняется"),(2,"Закрыт")]
        )