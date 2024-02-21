import geopandas as gpd; import fiona; import numpy as np
fiona.drvsupport.supported_drivers['libkml'] = 'rw' 
fiona.drvsupport.supported_drivers['LIBKML'] = 'rw' 
import rioxarray as rio; import xarray as xr
import matplotlib.pyplot as plt


def exportNdviPngClipped(pTif, pLote, pSalida):

    tifClipped = xr.where(rio.open_rasterio(pTif).rio.clip(gpd.read_file(pLote).geometry, drop=True)==0, np.nan, rio.open_rasterio(pTif).rio.clip(gpd.read_file(pLote).geometry, drop=True))
    # Para el titulo
    fname = pTif.split("/")[::-1][0].split(".")[0]
    idLote = pLote.split("/")[-1].split(".")[0]
    fecha = fecha = fname.split("T")[0]

    #
    fig, ax = plt.subplots()
    tifClipped.plot(ax = ax, cmap = 'RdYlGn', vmin = 0, vmax = 1)

    ax.set_title(f"NDVI - IDLote {idLote}" + "\n " + fecha)
    ax.set_xlabel("Longitudes"); ax.set_ylabel("Latitudes")

    plt.savefig(f"{pSalida}{fname}.png", dpi = 500, bbox_inches = "tight")
    plt.close()