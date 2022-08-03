// Default initial parameters
console.log("Setting default parameters...")
var domain = document.location;
var current_rcp = "RCP85";
var current_models = [];
var current_metric = "frac_extreme";
var current_region_group = "CA_Bulletin_118_Groundwater_Basins";
var current_info_index = "all"
var current_region_name = "";
var current_info_avg_value = "";
var current_info_agree_value = "";
var current_metric_pretty = "";

var current_avg = "";
var current_agree_dataset = [];
var data1_loaded = false;
var data2_loaded = false;
var region_index = 0;

var region_fill_color = "#9e9e9e";
var region_line_color = "#383838";
var region_fill_unselected_opacity = 0.1;
var region_fill_selected_opacity = 0.7;
var region_line_opacity = 0.2;
var current_overlay = "frac_extreme_RCP85-overlay";
var current_legend = "frac_extreme_RCP85-legend";
var overlay_opacity = 0.8;
var [overlay_l, overlay_r, overlay_t, overlay_b] = [-124.6, -113.77, 42.3, 32.05];
var overlay_dir_path = "overlay_images/";
let overlay_names = ['frac_extreme_RCP85-overlay', 'max_threeday_precip_RCP85-overlay', 'nov_mar_percent_RCP85-overlay', 'rainfall_ratio_RCP85-overlay', 'num_ros_events_RCP85-overlay', 'norm_rain_on_snow_RCP85-overlay', 'SWE_total_RCP85-overlay', 'et_RCP85-overlay', 'frac_extreme_RCP45-overlay', 'max_threeday_precip_RCP45-overlay', 'nov_mar_percent_RCP45-overlay', 'rainfall_ratio_RCP45-overlay', 'num_ros_events_RCP45-overlay', 'norm_rain_on_snow_RCP45-overlay', 'SWE_total_RCP45-overlay', 'et_RCP45-overlay'];



// All information panes to the left of the map
let panes = ["primary-pane", "choose-models-pane", "choose-metric-pane"];

// Initialize current variables using methods
buttonChangeMetric("frac_extreme");
setRCP85();

// Initialize dataset
updateDataset(current_metric, current_rcp, current_region_group, current_info_index);

// =============== Initialize Mapbox API ===============
// Get  API token
mapboxgl.accessToken = 'pk.eyJ1Ijoib3h5Z2VuMSIsImEiOiJja25jMmh3b28wenFlMnFvaGowN3B6bmc1In0.MKaFBCRkpp4gZWA3hIT-iA';

console.log("V1")
// Load map  -> old style: 'mapbox://styles/mapbox/light-v10'
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/dark-v10',
    center: [-121, 37.830348],
    zoom: 4.9
});
var hoveredStateId  = null;
// =============== End of Initialization ===============

// Displays specified pane and hides all others
function focusOnPane(focus_pane) {
    for (const pane of panes){
        if (pane == focus_pane){
            document.getElementById(pane).style.display = "inline";
        }else{
            document.getElementById(pane).style.display = "none";
        }
    }
}

/*
id="info-section"
id="info-region_name"></div></h2>
id="info-metric"></div></h4>
id="info-model_average"></div></h4>
id="info-model_agremeent"></div></h4>
*/

// Sets which regions to display on the map
function setMapRegions(spec_region){
    document.getElementById(current_region_group + "-checkbox").checked = false;
    map.setLayoutProperty(current_region_group + "-borders", 'visibility', 'none');
    map.setLayoutProperty(current_region_group + "-fills", 'visibility', 'none');
    current_region_group = spec_region;
    map.setLayoutProperty(spec_region + "-borders", 'visibility', 'visible');
    map.setLayoutProperty(spec_region + "-fills", 'visibility', 'visible');
    updateInfo();
}


// Sets overlay to match metric and RCP
function setOverlay(){
    try{
        map.setLayoutProperty(current_overlay + "-layer", 'visibility', 'none');
        current_overlay = current_metric + "_" + current_rcp + "-overlay";
        current_legend = current_metric + "_" + current_rcp + "-legend";
        map.setLayoutProperty(current_overlay + "-layer", 'visibility', 'visible');
        document.getElementById("legend-img").src = domain + "download/" + overlay_dir_path + current_legend + ".png";
        document.getElementById("metric-selected").innerHTML = document.getElementById(current_metric + "-button").innerHTML;
    } catch (error){
        console.log(error);
    }
}


// Sets selected RCP to RCP 4.5
function setRCP45() {
    console.log("Switching to RCP 4.5")
    document.getElementById('rcp85-checkbox').checked = false;
    current_rcp = "RCP45";
    updateInfo();
    setOverlay();
}


// Sets selected RCP to RCP 8.5
function setRCP85() {
    console.log("Switching to RCP 8.5")
    document.getElementById('rcp45-checkbox').checked = false;
    current_rcp = "RCP85";
    updateInfo();
    setOverlay();
}


// Displays metrics pane with options to choose metric
function displayMetricsPane() {
    focusOnPane("choose-metric-pane");
}


// Displays models pane with options to choose models
function displayModelsPane() {
    focusOnPane("choose-models-pane");
}


// Initiates information update with metric selection and shifts focus back to primary pane
function buttonChangeMetric(metric){
    focusOnPane("primary-pane");
    document.getElementById(current_metric + '-button').disabled = false;
    document.getElementById(metric + '-button').disabled = true;
    current_metric = metric;
    current_metric_pretty = document.getElementById(current_metric + "-button").innerHTML;
    updateInfo();
    setOverlay();
}


// Initiates information update with model selections and shifts focus back to primary pane
function buttonChangeModels(){
    console.log("Confirming model change (doesn't do anything for now)")
    updateInfo();
    focusOnPane("primary-pane");
}


// Updates the current dataset
function updateDataset(metric, rcp, region_group, index){
    // frac_extreme_RCP85_WBD_USGS_HUC10_CA_totalaverage
    url = domain + "/data/" + metric + "-"+ rcp + "-" + region_group + "-totalaverage/" + index;
    console.log(url);
    //url2 = domain + "/data/" + metric + "-"+ rcp + "_" + region_group + "_" + data[1];
    fetch(url).then(response => response.text())
        .then(textString => {
            current_avg = textString;
            data1_loaded = true;
            document.getElementById("info-section").style.display = "inline";
            document.getElementById("info-region_name").innerHTML = current_region_name;
            document.getElementById("info-metric").innerHTML = current_metric_pretty;
            document.getElementById("info-model_average").innerHTML = current_avg;
            document.getElementById("info-model_agreement").innerHTML = current_info_agree_value;
    });
}


// Updates all info tags in the HTML to reflect 'current_' variables
function updateInfo() {
    updateDataset(current_metric, current_rcp, current_region_group, region_index);
}

/* ===================================== Mapbox API ===================================== */

map.on('load', function () {
    for (name of overlay_names){
        var visibility = "none";
        if (name == current_overlay){
            visibility = "visible";
        }
        map.addSource(name, {
            'type': 'image',
            'url': domain + "download/" + overlay_dir_path + name + ".png",
            'coordinates': [
                [overlay_l, overlay_t],
                [overlay_r, overlay_t],
                [overlay_r, overlay_b],
                [overlay_l, overlay_b]]
        });
        map.addLayer({
            id: name + '-layer',
                'type': 'raster',
                'source': name,
                'layout': {'visibility': visibility},
                'paint': {
                    'raster-fade-duration': 0,
                    'raster-opacity': overlay_opacity
            }
        });
    }
    
    setOverlay();
    
    // ================== Groundwater Basin data, layers (fill and borders), and mouse functions ==================
    map.addSource('CA_Bulletin_118_Groundwater_Basins', {
        type: 'geojson',
        data: domain + "download/geojsons/CA_Bulletin_118_Groundwater_Basins.geojson",
        generateId: true
        });
    map.addLayer({
        'id': 'CA_Bulletin_118_Groundwater_Basins-fills',
        'type': 'fill',
        'source': 'CA_Bulletin_118_Groundwater_Basins',
        'layout': {'visibility': 'visible'},
        'paint': {
            'fill-color': region_fill_color,
            'fill-opacity': ['case', ['boolean', ['feature-state', 'hover'], false], region_fill_selected_opacity, region_fill_unselected_opacity ]
        }
    });
    map.addLayer({
        'id': 'CA_Bulletin_118_Groundwater_Basins-borders',
        'type': 'line',
        'source': 'CA_Bulletin_118_Groundwater_Basins',
        'layout': {'visibility': 'visible'},
        'paint': {
            'line-color': region_line_color,
            'line-width': 2,
            'line-opacity': region_line_opacity
        }
    });
    // When a user moves their mouse into one of the regions specified in this group
    map.on('mousemove', 'CA_Bulletin_118_Groundwater_Basins-fills', function (e) {
        if (e.features.length > 0) {
            if (hoveredStateId !== null) {
                map.setFeatureState(
                    { source: 'CA_Bulletin_118_Groundwater_Basins', id: hoveredStateId },
                    { hover: false });
            }
            hoveredStateId = e.features[0].id;
            map.setFeatureState(
                { source: 'CA_Bulletin_118_Groundwater_Basins', id: hoveredStateId },
                { hover: true });
        }
    });
    // When a user moves their mouse out of one of the regions specified in this group
    map.on('mouseleave', 'CA_Bulletin_118_Groundwater_Basins-fills', function () {
        console.log("Left in CA_Bulletin_118_Groundwater_Basins")
    });
    // When a user clicks on one of the regions specified in this group
    map.on('click', 'CA_Bulletin_118_Groundwater_Basins-fills', function (e){
        if (e.features.length == 1){
            region_index = e.features[0].id;
            current_region_name = e.features[0]["properties"]["Basin_Su_1"];
            updateInfo();
        }
    });



    // ================== County data, layers (fill and borders), and mouse functions ==================
    map.addSource('CA_Counties_TIGER2016', {
        type: 'geojson',
        data: domain + "download/geojsons/CA_Counties_TIGER2016.geojson",
        generateId: true
        });
    map.addLayer({
        'id': 'CA_Counties_TIGER2016-fills',
        'type': 'fill',
        'source': 'CA_Counties_TIGER2016',
        'layout': {'visibility': 'none'},
        'paint': {
            'fill-color': region_fill_color,
            'fill-opacity': ['case', ['boolean', ['feature-state', 'hover'], false], region_fill_selected_opacity, region_fill_unselected_opacity ]
        }
    });
    map.addLayer({
        'id': 'CA_Counties_TIGER2016-borders',
        'type': 'line',
        'source': 'CA_Counties_TIGER2016',
        'layout': {'visibility': 'none'},
        'paint': {
            'line-color': region_line_color,
            'line-width': 2,
            'line-opacity': region_line_opacity
        }
    });
    // When a user moves their mouse into one of the regions specified in this group
    map.on('mousemove', 'CA_Counties_TIGER2016-fills', function (e) {
        if (e.features.length > 0) {
            if (hoveredStateId !== null) {
                map.setFeatureState(
                    { source: 'CA_Counties_TIGER2016', id: hoveredStateId },
                    { hover: false });
            }
            hoveredStateId = e.features[0].id;
            map.setFeatureState(
                { source: 'CA_Counties_TIGER2016', id: hoveredStateId },
                { hover: true });
        }
    });
    // When a user moves their mouse out of one of the regions specified in this group
    map.on('mouseleave', 'CA_Counties_TIGER2016-fills', function () {
        console.log("Left in CA_Counties_TIGER2016")
    });
    // When a user clicks on one of the regions specified in this group
    map.on('click', 'CA_Counties_TIGER2016-fills', function (e){
        if (e.features.length == 1){
            region_index = e.features[0].id;
            current_region_name = e.features[0]["properties"]["NAMELSAD"];
            updateInfo();
        }
    });



    // ================== Places data, layers (fill and borders), and mouse functions ==================
    map.addSource('CA_Places_TIGER2016', {
        type: 'geojson',
        data: domain + "download/geojsons/CA_Places_TIGER2016.geojson",
        generateId: true
        });
    map.addLayer({
        'id': 'CA_Places_TIGER2016-fills',
        'type': 'fill',
        'source': 'CA_Places_TIGER2016',
        'layout': {'visibility': 'none'},
        'paint': {
            'fill-color': region_fill_color,
            'fill-opacity': ['case', ['boolean', ['feature-state', 'hover'], false], region_fill_selected_opacity, region_fill_unselected_opacity ]
        }
    });
    map.addLayer({
        'id': 'CA_Places_TIGER2016-borders',
        'type': 'line',
        'source': 'CA_Places_TIGER2016',
        'layout': {'visibility': 'none'},
        'paint': {
            'line-color': region_line_color,
            'line-width': 2,
            'line-opacity': region_line_opacity
        }
    });
    // When a user moves their mouse into one of the regions specified in this group
    map.on('mousemove', 'CA_Places_TIGER2016-fills', function (e) {
        if (e.features.length > 0) {
            if (hoveredStateId !== null) {
                map.setFeatureState(
                    { source: 'CA_Places_TIGER2016', id: hoveredStateId },
                    { hover: false });
            }
            hoveredStateId = e.features[0].id;
            map.setFeatureState(
                { source: 'CA_Places_TIGER2016', id: hoveredStateId },
                { hover: true });
        }
    });
    // When a user moves their mouse out of one of the regions specified in this group
    map.on('mouseleave', 'CA_Places_TIGER2016-fills', function () {
        console.log("Left in CA_Places_TIGER2016")
    });
    // When a user clicks on one of the regions specified in this group
    map.on('click', 'CA_Places_TIGER2016-fills', function (e){
        if (e.features.length == 1){
            region_index = e.features[0].id;
            current_region_name = e.features[0]["properties"]["NAMELSAD"];
            updateInfo();
        }
    });



    // ================== Watershed data, layers (fill and borders), and mouse functions ==================
    map.addSource('WBD_USGS_HUC10_CA', {
        type: 'geojson',
        data: domain + "download/geojsons/WBD_USGS_HUC10_CA.geojson",
        generateId: true
        });
    map.addLayer({
        'id': 'WBD_USGS_HUC10_CA-fills',
        'type': 'fill',
        'source': 'WBD_USGS_HUC10_CA',
        'layout': {'visibility': 'none'},
        'paint': {
            'fill-color': region_fill_color,
            'fill-opacity': ['case', ['boolean', ['feature-state', 'hover'], false], region_fill_selected_opacity, region_fill_unselected_opacity ]
        }
    });
    map.addLayer({
        'id': 'WBD_USGS_HUC10_CA-borders',
        'type': 'line',
        'source': 'WBD_USGS_HUC10_CA',
        'layout': {'visibility': 'none'},
        'paint': {
            'line-color': region_line_color,
            'line-width': 2,
            'line-opacity': region_line_opacity
        }
    });
    // When a user moves their mouse into one of the regions specified in this group
    map.on('mousemove', 'WBD_USGS_HUC10_CA-fills', function (e) {
        if (e.features.length > 0) {
            if (hoveredStateId !== null) {
                map.setFeatureState(
                    { source: 'WBD_USGS_HUC10_CA', id: hoveredStateId },
                    { hover: false });
            }
            hoveredStateId = e.features[0].id;
            map.setFeatureState(
                { source: 'WBD_USGS_HUC10_CA', id: hoveredStateId },
                { hover: true });
        }
    });
    // When a user moves their mouse out of one of the regions specified in this group
    map.on('mouseleave', 'WBD_USGS_HUC10_CA-fills', function () {
        console.log("Left in WBD_USGS_HUC10_CA")
    });
    // When a user clicks on one of the regions specified in this group
    map.on('click', 'WBD_USGS_HUC10_CA-fills', function (e){
        if (e.features.length == 1){
            region_index = e.features[0].id;
            current_region_name = e.features[0]["properties"]["Name"];
            updateInfo();
        }
    });

});