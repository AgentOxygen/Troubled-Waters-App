// Leaflet default coordinate system: EPSG:3857/Google Mercator 900913
// Tile layers can be selected from here https://leaflet-extras.github.io/leaflet-providers/preview/

var map = L.map('map', {
    center: [36.7783, -119.4179],
    zoom: 6
});

var Stadia_AlidadeSmooth = L.tileLayer('https://stamen-tiles.a.ssl.fastly.net/toner/{z}/{x}/{y}.png', {
	maxZoom: 10,
}).addTo(map);

var myStyle = {
    "color": "#F7FF00",
    "weight": 100,
    "opacity": 1
};

var CA_GW_Basin_layer = L.geoJSON(CA_GW_Basins_json, {
    style: myStyle
}).addTo(map);

console.log(CA_GW_Basins_json);
//CA_GW_Basin_layer.addData(CA_GW_Basins_json);