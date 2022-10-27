import xarray
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import matplotlib.cm as cm
from PIL import Image


DATA_OUTPUT_DIR = "../troubled_waters_data/output_netcdf/"
IMG_OUTPUT_DIR = "../troubled_waters_data/model_mean_imgs/"
metrics = ['frac_extreme', 'max_threeday_precip', 'nov_mar_percent',
            'rainfall_ratio', 'num_ros_events', 'norm_rain_on_snow',
            'SWE_total', 'et']
norms = [Normalize(vmin=-20, vmax=20), Normalize(vmin=-100, vmax=100), Normalize(vmin=-20, vmax=20),
        Normalize(vmin=-100, vmax=100), Normalize(vmin=-100, vmax=100), Normalize(vmin=-50, vmax=50),
        Normalize(vmin=-100, vmax=100), Normalize(vmin=-50, vmax=50)]

metric_means = {}

for rcp in ["RCP85", "RCP45"]:
    for met_index, metric in enumerate(metrics):
        print(f"{metric}_{rcp}")
        metric_ds = xarray.open_dataset(f"{DATA_OUTPUT_DIR}{metric}_{rcp}.nc")*100
        model_mean = metric_ds.to_array(dim='tmp').mean('tmp')
        model_mean = model_mean.where(model_mean != np.nan)
        new_lat = np.linspace(model_mean.lat[0], model_mean.lat[-1], model_mean.lat.size*2)
        new_lon = np.linspace(model_mean.lon[0], model_mean.lon[-1], model_mean.lon.size*2)
        vals = model_mean.interp(lat=new_lat, lon=new_lon).values
        
        img = np.zeros((vals.shape[0], vals.shape[1], 4))
        cmap = cm.get_cmap('PuOr')
        norm = norms[met_index]
        for i in range(vals.shape[0]):
            for j in range(vals.shape[1]):
                value = cmap(norm(vals[i, j]))        
                img[i, j] = np.array((value[0], value[1], value[2], (1-np.isnan(vals[i, j])*1)))
        
        im = Image.fromarray((np.flip(np.rot90(img, 2), axis=1) * 255).astype(np.uint8))
        im.save(f"{IMG_OUTPUT_DIR}{metric}_{rcp}.png")