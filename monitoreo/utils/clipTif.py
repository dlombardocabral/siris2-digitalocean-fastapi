def clipTif(pTif, pLote):

    import rioxarray as rio
    import xarray as xr
    import geopandas as gpd
    import numpy as np

    tifClipped = xr.where(rio.open_rasterio(pTif).rio.clip(gpd.read_file(pLote).geometry, drop=True)==0, np.nan, rio.open_rasterio(pTif).rio.clip(gpd.read_file(pLote).geometry, drop=True))

    tifClipped = tifClipped.rio.write_crs('epsg:4326', inplace = True)
    tifClipped.rio.to_raster(pTif)