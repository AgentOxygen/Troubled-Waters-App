from flask import Flask, request, send_file
from datetime import date
import json
import xarray

app = Flask(__name__)


# Load data
REGION_DATA_OUTPUT_DIR = "../troubled_waters_data/output_region_netcdf/"
MEAN_IMG_DIR = "../troubled_waters_data/model_mean_imgs/"
CB_IMG_DIR = "../troubled_waters_data/colorbars/"
metrics = ['frac_extreme', 'max_threeday_precip', 'nov_mar_percent',
            'rainfall_ratio', 'num_ros_events', 'norm_rain_on_snow',
            'SWE_total', 'et']
region_labels = ["Groundwater Basins", "Counties", "Places", "Watersheds"]
regions = ["GWB", "COUNTIES", "PLACES", "WBD"]
regional_data = {}
for metric in metrics:
    for rcp in ["RCP45", "RCP85"]:
        for index, region in enumerate(regions):
            filename = f"{metric}_{rcp}_{region}"
            regional_data[filename] = xarray.open_dataset(f"{REGION_DATA_OUTPUT_DIR}{filename}.nc")
            regional_data[filename]["label"] = region_labels[index]
            

@app.route("/")
def hello_world():
    return f"UT-UCS Troubled Waters back-end Flask server: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"


@app.route("/get_region_info", methods=['GET'])
def getRegionInfo():
    """
    Returns model info on a particular region
    """
    dataset = request.args.get('ds', default='', type=str)
    region_var = request.args.get('var', default='', type=str)
    region_var_key = request.args.get('var_key', default='', type=int)
    
    data = regional_data[dataset].loc[{f"{region_var}":region_var_key}]
    reg_info = {
        "models": list(data.model.values),
        "model_means": list(data["model_mean"].values),
        "model_stds": list(data["model_std"].values),
        "model_means": list(data["model_min"].values),
        "model_means": list(data["model_max"].values),
        "model_means": list(data["model_mean"].values)
    }
    
    return json.dumps(reg_info)


@app.route("/get_region_map", methods=['GET'])
def getRegionDatasetInfo():
    """
    Returns coordinate and dimension info on a particular dataset of regions
    """
    dataset = request.args.get('ds', default='', type=str)
    label_variable_name = request.args.get('lvar', default='', type=str)
    id_variable_name = request.args.get('idvar', default='', type=str)
    ds = regional_data[dataset]
    ds_info = {
        "region_labels": list(ds[label_variable_name].values),
        "region_ids": [int(i) for i in list(ds[id_variable_name].values)],
        "models": list(ds["model"].values)
    }
    return ds_info


@app.route("/formatted/region_dropdowns", methods=['GET'])
def formattedRegionDropdowns():
    """
    Returns formatted HTML code for filling the region dropdowns
    """
    dataset = request.args.get('ds', default='', type=str)
    label_variable_name = request.args.get('lvar', default='', type=str)
    ds = regional_data[dataset]
    
    ret_str = ""
    for index, reg_name in enumerate(list(ds[label_variable_name].values)):
        l = dataset.split("_RCP")[0]
        elmt_id = f"{l}_{index}"
        fstr = f'''<a id="{elmt_id}" onclick="changeRegion('{elmt_id}', '{dataset}', '{str(ds["label"].values)}', '{reg_name}')" class="dropdown-item" href="#">{reg_name}</a>'''
        ret_str += fstr
    return ret_str


@app.route('/get_raster_img', methods=['GET'])
def getRasterImage():
    name = request.args.get('name')
    path = f"{MEAN_IMG_DIR}{name}.png"
    response = send_file(path, mimetype='image/png')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/get_colorbar_img', methods=['GET'])
def getCBImage():
    name = request.args.get('name')
    path = f"{CB_IMG_DIR}{name}.png"
    response = send_file(path, mimetype='image/png')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == "__main__":
    # Port 1024 is open on thunder for most users
    app.run(host="localhost", port=8000, debug=True)

