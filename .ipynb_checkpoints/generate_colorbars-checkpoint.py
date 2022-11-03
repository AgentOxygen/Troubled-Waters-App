import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import Normalize

CB_OUTPUT_DIR = "../troubled_waters_data/colorbars/"
metrics = ['frac_extreme', 'max_threeday_precip', 'nov_mar_percent',
            'rainfall_ratio', 'num_ros_events', 'norm_rain_on_snow',
            'SWE_total', 'et']
norms = [Normalize(vmin=-20, vmax=20), Normalize(vmin=-100, vmax=100), Normalize(vmin=-20, vmax=20),
        Normalize(vmin=-100, vmax=100), Normalize(vmin=-100, vmax=100), Normalize(vmin=-50, vmax=50),
        Normalize(vmin=-100, vmax=100), Normalize(vmin=-50, vmax=50)]

for index, metric in enumerate(metrics):
    fig, ax = plt.subplots(1, 1, figsize=(1, 8), dpi=80)
    #ax = fig.add_axes([0.05, 0.80, 0.9, 0.1])
    
    cb = mpl.colorbar.ColorbarBase(ax, norm=norms[index], orientation='vertical', cmap='PuOr')
    fig.savefig(f"{CB_OUTPUT_DIR}{metric}.png", dpi=fig.dpi, bbox_inches='tight', pad_inches=0.2)