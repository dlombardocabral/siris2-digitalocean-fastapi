import geopandas as gpd; import fiona; import numpy as np
fiona.drvsupport.supported_drivers['libkml'] = 'rw' 
fiona.drvsupport.supported_drivers['LIBKML'] = 'rw' 
import rioxarray as rio; import xarray as xr
import matplotlib.pyplot as plt

## 
import matplotlib as mpl

def exportProductividadPng(pSegment, pLote, pSalida):

    semaforo = mpl.colors.ListedColormap(
        ["#f70505", "#f7df05", "#09941b"]
    )
    
    # Para el titulo
    fname = pSegment.split("/")[::-1][0].split(".")[0]
    idLote = pLote.split("/")[-1].split(".")[0]
    fecha = fecha = fname.split("T")[0]

    tifClipped = xr.where(rio.open_rasterio(pSegment).rio.clip(gpd.read_file(pLote).geometry, drop=True)==0, np.nan, rio.open_rasterio(pSegment).rio.clip(gpd.read_file(pLote).geometry, drop=True))

    #
    fig, ax = plt.subplots()
    cm = tifClipped.plot(ax = ax, cmap = semaforo, vmin = 10, vmax = 30, add_colorbar = False)

    ax.set_title(f"Productividad - IDLote {idLote}" + "\n " + fecha)
    ax.set_xlabel("Longitudes"); ax.set_ylabel("Latitudes")

    cbar = plt.colorbar(cm, ax = ax)
    cbar.set_ticks(ticks=[10, 20, 30], labels=["Baja", "Media", "Alta"])

    plt.savefig(f"{pSalida}{fname}.png", dpi = 500, bbox_inches = "tight")
    plt.close()