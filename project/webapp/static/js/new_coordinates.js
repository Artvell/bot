function ajaxFunction(point,route_code, new_coords){
    fetch("/new_coords", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                code: route_code
            })
        })
        .then(response => response.json())
        .then(json => {
            console.log("!!", json)
            new_coords(point,json["long"],json["lat"])
            }
        )
}

