function init (from_lon,from_lat,to_lon,to_lat) {
    console.log("!")
    var multiRoute = new ymaps.multiRouter.MultiRoute({
        referencePoints: [
            [from_lon,from_lat],
            [to_lon,to_lat]
        ],
        params: {
            results: 5
        }
    }, {
        boundsAutoApply: true
    });
    var myMap = new ymaps.Map('map', {
        center: [41.3082, 69.2598],
        zoom: 10
    }, {
        buttonMaxWidth: 300
    });
    myMap.geoObjects.add(multiRoute);
    console.log("@")
}
