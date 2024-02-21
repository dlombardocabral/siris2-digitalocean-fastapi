import geopandas as gpd; import fiona; import numpy as np
fiona.drvsupport.supported_drivers['libkml'] = 'rw' 
fiona.drvsupport.supported_drivers['LIBKML'] = 'rw' 
import rioxarray as rio; import xarray as xr
import json

def exportJsonStatics(pTif, pLote, pSalida):
    # Para exportar
    fname = pTif.split("/")[::-1][0].split(".")[0]
    idLote = pLote.split("/")[-1].split(".")[0]
    fecha = fname.split("T")[0]

    tifClipped = xr.where(rio.open_rasterio(pTif).rio.clip(gpd.read_file(pLote).geometry, drop=True)==0, np.nan, rio.open_rasterio(pTif).rio.clip(gpd.read_file(pLote).geometry, drop=True))

    ndviStatics = dict()
    ndviStatics['idLote'] = idLote
    ndviStatics['ndviFecha'] = fecha
    ndviStatics['ndviMin'] = float(tifClipped.min().values)
    ndviStatics['ndviMean'] = float(tifClipped.mean().values)
    ndviStatics['ndviMedian'] = float(tifClipped.median().values)
    ndviStatics['ndviStd'] = float(tifClipped.std().values)
    ndviStatics['ndviMax'] = float(tifClipped.max().values)

    # Guardar el JSON
    with open(pSalida + f'{fname}.json', 'w') as outfile:
        json.dump(ndviStatics, outfile)
