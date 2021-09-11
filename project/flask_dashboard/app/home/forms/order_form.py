from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, HiddenField, IntegerField
from wtforms.validators import DataRequired

class OrderForm(FlaskForm):
    order_id = IntegerField("Заказ №")
    status = SelectField(
        "Статус",
        choices=[
            (1,"Предзаказ"), (2,"Выполняется"), (3,"Закрыт"), (4,"Ожидает оплаты")
        ],
        validators=[DataRequired()],
        )
    order_type = SelectField(
        "Тип доставки",
        choices=[
            (1,"Самовывоз"),(2,"Доставка"),(3,"Предзаказ")
        ],
        validators=[DataRequired()]
    )
    payment_status = SelectField(
        "Статус оплаты",
        choices=[
            (0,"Не оплачен"),
            (1,"Наличные"),
            (2,"Карта"),
            (3,"Через телеграм")
        ],
        validators=[DataRequired()]
    )