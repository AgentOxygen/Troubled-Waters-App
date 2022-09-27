from flask import Flask, render_template, send_from_directory, request
from os.path import join, isfile
import xarray

# Load netcdf files
NETCDF_DIR_PATH = "../netcdf/"

dry_total_RCP45_ext = xarray.open_dataset(f'{NETCDF_DIR_PATH}dry_total_RCP45.extended.nc')
dry_total_RCP45 = xarray.open_dataset(f'{NETCDF_DIR_PATH}dry_total_RCP45.nc')
dry_total_RCP85_ext = xarray.open_dataset(f'{NETCDF_DIR_PATH}dry_total_RCP85.extended.nc')
dry_total_RCP85 = xarray.open_dataset(f'{NETCDF_DIR_PATH}dry_total_RCP85.nc')

dry_to_wet_whip_total_RCP45_ext = xarray.open_dataset(f'{NETCDF_DIR_PATH}dry_to_wet_whip_total_RCP45.extended.nc')
dry_to_wet_whip_total_RCP45 = xarray.open_dataset(f'{NETCDF_DIR_PATH}dry_to_wet_whip_total_RCP45.nc')
dry_to_wet_whip_total_RCP85_ext = xarray.open_dataset(f'{NETCDF_DIR_PATH}dry_to_wet_whip_total_RCP85.extended.nc')
dry_to_wet_whip_total_RCP85 = xarray.open_dataset(f'{NETCDF_DIR_PATH}dry_to_wet_whip_total_RCP85.nc')

et_RCP45 = xarray.open_dataset(f'{NETCDF_DIR_PATH}et_RCP45.nc')
et_RCP45_now = xarray.open_dataset(f'{NETCDF_DIR_PATH}et_RCP45_now.nc')
et_RCP85 = xarray.open_dataset(f'{NETCDF_DIR_PATH}et_RCP85.nc')
et_RCP85_now = xarray.open_dataset(f'{NETCDF_DIR_PATH}et_RCP85_now.nc')

frac_extreme_RCP45 = xarray.open_dataset(f'{NETCDF_DIR_PATH}frac_extreme_RCP45.nc')
frac_extreme_RCP45_now = xarray.open_dataset(f'{NETCDF_DIR_PATH}frac_extreme_RCP45_now.nc')
frac_extreme_RCP85 = xarray.open_dataset(f'{NETCDF_DIR_PATH}frac_extreme_RCP85.nc')
frac_extreme_RCP85_now = xarray.open_dataset(f'{NETCDF_DIR_PATH}frac_extreme_RCP85_now.nc')

max_threeday_precip_RCP45 = xarray.open_dataset(f'{NETCDF_DIR_PATH}max_threeday_precip_RCP45.nc')
max_threeday_precip_RCP45_now = xarray.open_dataset(f'{NETCDF_DIR_PATH}max_threeday_precip_RCP45_now.nc')
max_threeday_precip_RCP85 = xarray.open_dataset(f'{NETCDF_DIR_PATH}max_threeday_precip_RCP85.nc')
max_threeday_precip_RCP85_now = xarray.open_dataset(f'{NETCDF_DIR_PATH}max_threeday_precip_RCP85_now.nc')

MIROC5_IntraAnnual_Output_Late = xarray.open_dataset(f'{NETCDF_DIR_PATH}MIROC5_IntraAnnual_Output_Late.nc')
MIROC5_IntraAnnual_Output_Now = xarray.open_dataset(f'{NETCDF_DIR_PATH}MIROC5_IntraAnnual_Output_Now.nc')

nov_mar_percent_RCP45 = xarray.open_dataset(f'{NETCDF_DIR_PATH}nov_mar_percent_RCP45.nc')
nov_mar_percent_RCP45_now = xarray.open_dataset(f'{NETCDF_DIR_PATH}nov_mar_percent_RCP45_now.nc')
nov_mar_percent_RCP85 = xarray.open_dataset(f'{NETCDF_DIR_PATH}nov_mar_percent_RCP85.nc')
nov_mar_percent_RCP85_now = xarray.open_dataset(f'{NETCDF_DIR_PATH}nov_mar_percent_RCP85_now.nc')

num_ros_events_RCP45 = xarray.open_dataset(f'{NETCDF_DIR_PATH}num_ros_events_RCP45.nc')
num_ros_events_RCP45_now = xarray.open_dataset(f'{NETCDF_DIR_PATH}num_ros_events_RCP45_now.nc')
num_ros_events_RCP85 = xarray.open_dataset(f'{NETCDF_DIR_PATH}num_ros_events_RCP85.nc')
num_ros_events_RCP85_now = xarray.open_dataset(f'{NETCDF_DIR_PATH}num_ros_events_RCP85_now.nc')

pr_anntot_RCP45 = xarray.open_dataset(f'{NETCDF_DIR_PATH}pr_anntot_RCP45.nc')
pr_anntot_RCP45_now = xarray.open_dataset(f'{NETCDF_DIR_PATH}pr_anntot_RCP45_now.nc')
pr_anntot_RCP85 = xarray.open_dataset(f'{NETCDF_DIR_PATH}pr_anntot_RCP85.nc')
pr_anntot_RCP85_now = xarray.open_dataset(f'{NETCDF_DIR_PATH}pr_anntot_RCP85_now.nc')

pr_monthly_july_RCP45 = xarray.open_dataset(f'{NETCDF_DIR_PATH}pr_monthly_july_RCP45.nc')
pr_monthly_july_RCP45_now = xarray.open_dataset(f'{NETCDF_DIR_PATH}pr_monthly_july_RCP45_now.nc')
pr_monthly_july_RCP85 = xarray.open_dataset(f'{NETCDF_DIR_PATH}pr_monthly_july_RCP85.nc')
pr_monthly_july_RCP85_now = xarray.open_dataset(f'{NETCDF_DIR_PATH}pr_monthly_july_RCP85_now.nc')

rainfall_ratio_RCP45 = xarray.open_dataset(f'{NETCDF_DIR_PATH}rainfall_ratio_RCP45.nc')
rainfall_ratio_RCP45_now = xarray.open_dataset(f'{NETCDF_DIR_PATH}rainfall_ratio_RCP45_now.nc')
rainfall_ratio_RCP85 = xarray.open_dataset(f'{NETCDF_DIR_PATH}rainfall_ratio_RCP85.nc')
rainfall_ratio_RCP85_now = xarray.open_dataset(f'{NETCDF_DIR_PATH}rainfall_ratio_RCP85_now.nc')

SWE_total_RCP45 = xarray.open_dataset(f'{NETCDF_DIR_PATH}SWE_total_RCP45.nc')
SWE_total_RCP45_now = xarray.open_dataset(f'{NETCDF_DIR_PATH}SWE_total_RCP45_now.nc')
SWE_total_RCP85 = xarray.open_dataset(f'{NETCDF_DIR_PATH}SWE_total_RCP85.nc')
SWE_total_RCP85_now = xarray.open_dataset(f'{NETCDF_DIR_PATH}SWE_total_RCP85_now.nc')

wet_total_RCP45_ext = xarray.open_dataset(f'{NETCDF_DIR_PATH}wet_total_RCP45.extended.nc')
wet_total_RCP45 = xarray.open_dataset(f'{NETCDF_DIR_PATH}wet_total_RCP45.nc')
wet_total_RCP85_ext = xarray.open_dataset(f'{NETCDF_DIR_PATH}wet_total_RCP85.extended.nc')
wet_total_RCP85 = xarray.open_dataset(f'{NETCDF_DIR_PATH}wet_total_RCP85.nc')

wet_to_dry_whip_total_RCP45_ext = xarray.open_dataset(f'{NETCDF_DIR_PATH}wet_to_dry_whip_total_RCP45.extended.nc')
wet_to_dry_whip_total_RCP45 = xarray.open_dataset(f'{NETCDF_DIR_PATH}wet_to_dry_whip_total_RCP45.nc')
wet_to_dry_whip_total_RCP85_ext = xarray.open_dataset(f'{NETCDF_DIR_PATH}wet_to_dry_whip_total_RCP85.extended.nc')
wet_to_dry_whip_total_RCP85 = xarray.open_dataset(f'{NETCDF_DIR_PATH}wet_to_dry_whip_total_RCP85.nc')
# Set flask app name and upload folder. This tells flask where the top directory is.
app = Flask(__name__)
# In this case, we want the top directory to be the upload directory (this will also function as download)
app.config['UPLOAD_FOLDER'] = "."

# For downloading entire files within the flask directories (such as JSON or Shapefile)
@app.route('/fetch/<path:filename>', methods=['GET', 'POST'])
def fetch(filename):
    uploads = join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)

# # A basic data request that grabs key-values from the redis server using the filters specified by paramters
# @app.route('/data/<key>')
# def getData(key):
#     return rd.get(key)

# This is the main landing page, what the user sees
@app.route('/')
def main():
    # We use the HTML file as the template
    return render_template("main.html")

if __name__ == "__main__":
    app.run(host="localhost", port=1024, debug=True)

