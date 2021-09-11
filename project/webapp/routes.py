from webapp import app
from flask import render_template, request
from models import Route
import base64
import json

@app.route('/map/<code>/')
def map(code):
    route = Route.get_or_none(Route.uuid==code)
    if route is not None:
        yandex_key = "15636904-1573-4297-9cc4-57b6ce145375"
        from_location = route.from_location
        to_location = route.to_location
        now = route.now_location
        return render_template(
            'map.html',
            yandex_key=yandex_key,
            from_location=from_location,
            to_location=to_location,
            now=now
            )
    else:
        return "Неверная ссылка"


@app.route("/new_coords",methods=['POST'])
def new_coords():
    code = request.json.get("code")
    route = Route.get_or_none(Route.uuid==code)
    response = {
        "long": route.now_location[0],
        "lat": route.now_location[1],
    }
    return response

@app.route("/route/<code>/")
def route(code):
    print(code)
    try:
        encoded_to_bytes = code.encode("UTF-8")
        bytes_decode = base64.b64decode(encoded_to_bytes)
        decoded_string = bytes_decode.decode("UTF-8")
        print(decoded_string)
        result = [data.split("|") for data in decoded_string.split("/")]
        print(result)
        if len(result) != 2:
            return "Неверная ссылка"
        else:
            yandex_key = "15636904-1573-4297-9cc4-57b6ce145375"
            return render_template(
                'route.html',
                yandex_key=yandex_key,
                from_location = result[0],
                to_location = result[1]
                )
    except Exception as e:
        return "Неверная кодировка.{}".format(e)


