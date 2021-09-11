function init (from_lon,from_lat,to_lon,to_lat,point_lon,point_lat) {
    /**
     * Создаем мультимаршрут.
     * Первым аргументом передаем модель либо объект описания модели.
     * Вторым аргументом передаем опции отображения мультимаршрута.
     * @see https://api.yandex.ru/maps/doc/jsapi/2.1/ref/reference/multiRouter.MultiRoute.xml
     * @see https://api.yandex.ru/maps/doc/jsapi/2.1/ref/reference/multiRouter.MultiRouteModel.xml
     */
    var multiRoute = new ymaps.multiRouter.MultiRoute({
        // Описание опорных точек мультимаршрута.
        referencePoints: [
            [from_lon,from_lat],
            [to_lon,to_lat]
        ],
        // Параметры маршрутизации.
        params: {
            // Ограничение на максимальное количество маршрутов, возвращаемое маршрутизатором.
            results: 5
        }
    }, {
        // Автоматически устанавливать границы карты так, чтобы маршрут был виден целиком.
        boundsAutoApply: true
    });

    myGeoObject = new ymaps.GeoObject({
            // Описание геометрии.
            geometry: {
                type: "Point",
                coordinates: [point_lon,point_lat]
            },
            // Свойства.
            properties: {
                // Контент метки.
                iconContent: 'Водитель',
                hintContent: 'Ваш заказ'
            }
        }, {
            // Опции.
            // Иконка метки будет растягиваться под размер ее содержимого.
            preset: 'islands#blackStretchyIcon',
            // Метку можно перемещать.
            draggable: false
        });

    // Создаем карту с добавленными на нее кнопками.
    var myMap = new ymaps.Map('map', {
        center: [41.3082, 69.2598],
        zoom: 10
    }, {
        buttonMaxWidth: 300
    });

    // Добавляем мультимаршрут на карту.
    myMap.geoObjects.add(multiRoute);
    myMap.geoObjects.add(myGeoObject);
    //myGeoObject.geometry.setCoordinates([41.297018,69.272743])
    console.log(1,myGeoObject);
    return myGeoObject;
}


function new_coordinates(point,long,lat){
    console.log(3,point, long, lat)
    point.geometry.setCoordinates([long,lat]);
}
