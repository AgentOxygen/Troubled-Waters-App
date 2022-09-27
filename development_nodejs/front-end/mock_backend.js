const hostname = 'localhost';
const port = 7999;

const express = require('express');
const app = express();

var path_index_html = "C:/Users/Cameron/Documents/Troubled-Waters-App/development_nodejs/front-end/index.html";
var path_caligwbasin_geojson = "C:/Users/Cameron/Documents/Troubled-Waters-App/development_nodejs/front-end/geojson/CA_Bulletin_118_Groundwater_Basins.json"

app.get('/cal_gwb_geojson', function(request, response){
	response.sendFile(path_caligwbasin_geojson);
});

app.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`)
})