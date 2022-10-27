from os import listdir
import xarray
import numpy as np
import rasterio
import fiona
import geopandas
import rioxarray
from shapely.geometry import mapping, Polygon
import warnings
import threading
warnings.simplefilter(action='ignore', category=FutureWarning)

DATA_DIR = "../troubled_waters_data/netcdf/"
DATA_OUTPUT_DIR = "../troubled_waters_data/output_netcdf/"
REGION_DATA_OUTPUT_DIR = "../troubled_waters_data/output_region_netcdf/"
metrics = ['frac_extreme', 'max_threeday_precip', 'nov_mar_percent',
            'rainfall_ratio', 'num_ros_events', 'norm_rain_on_snow',
            'SWE_total', 'et']
SHPFILE_DIR = "../troubled_waters_data/shapefiles/"
hist_suffix = '_now'

        
def preprocess_metric(metric_ds):
    # Interpolate to a higher resolution
    new_lat = np.linspace(metric_ds.lat[0], metric_ds.lat[-1], metric_ds.lat.size*8)
    new_lon = np.linspace(metric_ds.lon[0], metric_ds.lon[-1], metric_ds.lon.size*8)
    metric_ds = metric_ds.interp(lat=new_lat, lon=new_lon)
    # Adjust coordinates to match the shapefile coordinates
    metric_ds = metric_ds.assign_coords(lon=(((metric_ds.lon + 180) % 360) - 180)).sortby('lon')
    # Set spatial dimensions for data
    metric_ds.rio.set_spatial_dims(x_dim='lon', y_dim='lat', inplace=True)
    # Specify CRS projection to match shapefile data
    metric_ds.rio.write_crs("epsg:4326", inplace=True)
    return metric_ds


def maskToGroundwaterBasins(input_path, output_path):
    metric_ds = preprocess_metric(xarray.open_dataset(input_path))
    
    # Read ing shapefile
    shapefile_path = SHPFILE_DIR + "CA_Bulletin_118_Groundwater_Basins.shp"
    shapefile = geopandas.read_file(shapefile_path)

    # Create dictionary for storing information on each region
    reg_ids = []
    reg_names = []
    reg_means = []
    reg_stds = []
    reg_mins = []
    reg_maxs = []

    for index, ID in enumerate(shapefile["OBJECTID"]):
        # Get polygon geometry for this region
        polys = [shapefile["geometry"][index]]
        # Format geometry set
        geom = { 'OBJECTID': index, 'geometry':polys}
        # Build data frame with same CRS
        geom_dataframe = geopandas.GeoDataFrame(geom, crs=shapefile.crs)
        # Mask data to region, including all regions it touches, not just encapsulates
        mask = metric_ds.rio.clip(geom_dataframe.geometry.apply(mapping), shapefile.crs, drop=True, all_touched=True)
        means = []
        stds = []
        mins = []
        maxs = []
        for model in list(mask.keys()):
            means.append(mask[model].mean().values)
            stds.append(mask[model].std().values)
            mins.append(mask[model].min().values)
            maxs.append(mask[model].max().values)
        
        reg_ids.append(ID)
        reg_names.append(shapefile["Basin_Su_1"][index])
        reg_means.append(means)
        reg_stds.append(stds)
        reg_mins.append(mins)
        reg_maxs.append(maxs)
    data_dict = {
        "basin_name": (["basin_id"], reg_names),
        "model_mean": (["basin_id", "model"], reg_means),
        "model_std": (["basin_id", "model"], reg_stds),
        "model_min": (["basin_id", "model"], reg_mins),
        "model_max": (["basin_id", "model"], reg_maxs)
    }
    coord_dict = {
        "basin_id": ("basin_id", reg_ids),
        "model": ("model", list(mask.keys()))
    }
    ds = xarray.Dataset(data_vars=data_dict, coords=coord_dict)
    ds.to_netcdf(output_path)


def maskToCounties(input_path):
    metric_ds = preprocess_metric(xarray.open_dataset(input_path))
    
    # Read ing shapefile
    shapefile_path = SHPFILE_DIR + "CA_Counties_TIGER2016.shp"
    shapefile = geopandas.read_file(shapefile_path)

    # Create dictionary for storing information on each region
    reg_ids = []
    reg_names = []
    reg_means = []
    reg_stds = []
    reg_mins = []
    reg_maxs = []

    for index, ID in enumerate(shapefile["COUNTYFP"]):
        # Get polygon geometry for this region
        polys = [shapefile["geometry"][index]]
        # Format geometry set
        geom = { 'OBJECTID': index, 'geometry':polys}
        # Build data frame with same CRS
        geom_dataframe = geopandas.GeoDataFrame(geom, crs=shapefile.crs)
        # Mask data to region, including all regions it touches, not just encapsulates
        mask = metric_ds.rio.clip(geom_dataframe.geometry.apply(mapping), shapefile.crs, drop=True, all_touched=True)
        means = []
        stds = []
        mins = []
        maxs = []
        for model in list(mask.keys()):
            means.append(mask[model].mean().values)
            stds.append(mask[model].std().values)
            mins.append(mask[model].min().values)
            maxs.append(mask[model].max().values)
        
        reg_ids.append(ID)
        reg_names.append(shapefile["NAME"][index])
        reg_means.append(means)
        reg_stds.append(stds)
        reg_mins.append(mins)
        reg_maxs.append(maxs)
    data_dict = {
        "county_name": (["county_fp"], reg_names),
        "model_mean": (["county_fp", "model"], reg_means),
        "model_std": (["county_fp", "model"], reg_stds),
        "model_min": (["county_fp", "model"], reg_mins),
        "model_max": (["county_fp", "model"], reg_maxs)
    }
    coord_dict = {
        "county_fp": ("county_fp", reg_ids),
        "model": ("model", list(mask.keys()))
    }
    ds = xarray.Dataset(data_vars=data_dict, coords=coord_dict)
    ds.to_netcdf(output_path)


def maskToPlaces(input_path):
    metric_ds = preprocess_metric(xarray.open_dataset(input_path))
    
    # Read ing shapefile
    shapefile_path = SHPFILE_DIR + "CA_Places_TIGER2016.shp"
    shapefile = geopandas.read_file(shapefile_path)

    # Create dictionary for storing information on each region
    reg_ids = []
    reg_names = []
    reg_means = []
    reg_stds = []
    reg_mins = []
    reg_maxs = []

    for index, ID in enumerate(shapefile["PLACEFP"]):
        # Get polygon geometry for this region
        polys = [shapefile["geometry"][index]]
        # Format geometry set
        geom = { 'OBJECTID': index, 'geometry':polys}
        # Build data frame with same CRS
        geom_dataframe = geopandas.GeoDataFrame(geom, crs=shapefile.crs)
        # Mask data to region, including all regions it touches, not just encapsulates
        mask = metric_ds.rio.clip(geom_dataframe.geometry.apply(mapping), shapefile.crs, drop=True, all_touched=True)
        means = []
        stds = []
        mins = []
        maxs = []
        for model in list(mask.keys()):
            means.append(mask[model].mean().values)
            stds.append(mask[model].std().values)
            mins.append(mask[model].min().values)
            maxs.append(mask[model].max().values)
        
        reg_ids.append(ID)
        reg_names.append(shapefile["NAME"][index])
        reg_means.append(means)
        reg_stds.append(stds)
        reg_mins.append(mins)
        reg_maxs.append(maxs)
    data_dict = {
        "place_name": (["place_fp"], reg_names),
        "model_mean": (["place_fp", "model"], reg_means),
        "model_std": (["place_fp", "model"], reg_stds),
        "model_min": (["place_fp", "model"], reg_mins),
        "model_max": (["place_fp", "model"], reg_maxs)
    }
    coord_dict = {
        "place_fp": ("place_fp", reg_ids),
        "model": ("model", list(mask.keys()))
    }
    ds = xarray.Dataset(data_vars=data_dict, coords=coord_dict)
    ds.to_netcdf(output_path)


def maskToWBD(input_path):
    metric_ds = preprocess_metric(xarray.open_dataset(input_path))
    
    # Read ing shapefile
    shapefile_path = SHPFILE_DIR + "WBD_USGS_HUC10_CA.shp"
    shapefile = geopandas.read_file(shapefile_path)

    # Create dictionary for storing information on each region
    reg_ids = []
    reg_names = []
    reg_means = []
    reg_stds = []
    reg_mins = []
    reg_maxs = []

    for index, ID in enumerate(shapefile["OBJECTID"]):
        # Get polygon geometry for this region
        polys = [shapefile["geometry"][index]]
        # Format geometry set
        geom = { 'OBJECTID': index, 'geometry':polys}
        # Build data frame with same CRS
        geom_dataframe = geopandas.GeoDataFrame(geom, crs=shapefile.crs)
        # Mask data to region, including all regions it touches, not just encapsulates
        mask = metric_ds.rio.clip(geom_dataframe.geometry.apply(mapping), shapefile.crs, drop=True, all_touched=True)
        means = []
        stds = []
        mins = []
        maxs = []
        for model in list(mask.keys()):
            means.append(mask[model].mean().values)
            stds.append(mask[model].std().values)
            mins.append(mask[model].min().values)
            maxs.append(mask[model].max().values)
        
        reg_ids.append(ID)
        reg_names.append(shapefile["Name"][index])
        reg_means.append(means)
        reg_stds.append(stds)
        reg_mins.append(mins)
        reg_maxs.append(maxs)
    data_dict = {
        "wbd_name": (["wbd_id"], reg_names),
        "model_mean": (["wbd_id", "model"], reg_means),
        "model_std": (["wbd_id", "model"], reg_stds),
        "model_min": (["wbd_id", "model"], reg_mins),
        "model_max": (["wbd_id", "model"], reg_maxs)
    }
    coord_dict = {
        "wbd_id": ("wbd_id", reg_ids),
        "model": ("model", list(mask.keys()))
    }
    ds = xarray.Dataset(data_vars=data_dict, coords=coord_dict)
    ds.to_netcdf(output_path)


if __name__ =="__main__":
    print("Creating ratio netCDFs")
    for rcp in ["RCP85", "RCP45"]:
        for met_index, metric in enumerate(metrics):
            metric_models = xarray.open_dataset(f"{DATA_DIR}{metric}_{rcp}.nc")
            metric_hist_models = xarray.open_dataset(F"{DATA_DIR}{metric}_{rcp}{hist_suffix}.nc")
            if metric == "SWE_total":
                metric_hist_models = metric_hist_models.where(metric_hist_models > 1)
            ratio = metric_models / metric_hist_models
            ratio.to_netcdf(f"{DATA_OUTPUT_DIR}{metric}_{rcp}.nc")
    
    print(f"Creating multithreaded regional data")
    for met_index, metric in enumerate(metrics):
        print(f"{metric} ", end="")
        t1 = threading.Thread(target=maskToGroundwaterBasins, args=(f"{DATA_OUTPUT_DIR}{metric}_RCP45.nc", f"{REGION_DATA_OUTPUT_DIR}{metric}_RCP45_GWB.nc",))
        t2 = threading.Thread(target=maskToCounties, args=(f"{DATA_OUTPUT_DIR}{metric}_RCP45.nc", f"{REGION_DATA_OUTPUT_DIR}{metric}_RCP45_COUNTIES.nc",))
        t3 = threading.Thread(target=maskToPlaces, args=(f"{DATA_OUTPUT_DIR}{metric}_RCP45.nc", f"{REGION_DATA_OUTPUT_DIR}{metric}_RCP45_PLACES.nc",))
        t4 = threading.Thread(target=maskToWBD, args=(f"{DATA_OUTPUT_DIR}{metric}_RCP45.nc", f"{REGION_DATA_OUTPUT_DIR}{metric}_RCP45_WBD.nc",))
        
        t5 = threading.Thread(target=maskToGroundwaterBasins, args=(f"{DATA_OUTPUT_DIR}{metric}_RCP85.nc", f"{REGION_DATA_OUTPUT_DIR}{metric}_RCP85_GWB.nc",))
        t6 = threading.Thread(target=maskToCounties, args=(f"{DATA_OUTPUT_DIR}{metric}_RCP85.nc", f"{REGION_DATA_OUTPUT_DIR}{metric}_RCP85_COUNTIES.nc",))
        t7 = threading.Thread(target=maskToPlaces, args=(f"{DATA_OUTPUT_DIR}{metric}_RCP85.nc", f"{REGION_DATA_OUTPUT_DIR}{metric}_RCP85_PLACES.nc",))
        t8 = threading.Thread(target=maskToWBD, args=(f"{DATA_OUTPUT_DIR}{metric}_RCP85.nc", f"{REGION_DATA_OUTPUT_DIR}{metric}_RCP85_WBD.nc",))
        
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t6.start()
        t7.start()
        t8.start()
        
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        t6.join()
        t7.join()
        t8.join()
    print("Done!")