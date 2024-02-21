import rioxarray as rio; import xarray as xr
import numpy as np

def getNdviSegment(pNdviLote, umbralMin, umbralMax, pSalida):

    umbralMin = float(umbralMin); umbralMax = float(umbralMax)
    '''
    Esta funcion realiza la segmentacion de una imagen GeoTif de acuerdo a la productividad del lote agricola. Divide en 3 segmentos distintos. Las escalas de productividad definidas son:
        10 -> Productividad baja (NDVI < umbralMin)
        20 -> Productividad media (umbralMin <= NDVI < umbralMax)
        30 -> Productividad alta (NDVI > umbralMax)
    '''
    ndviLote = rio.open_rasterio(pNdviLote)
    # Aplicar la segmentacion
    ndviSegmentado = xr.where(np.isnan(ndviLote), np.nan, xr.where(ndviLote>umbralMax, 30, xr.where((ndviLote<=umbralMax) & (ndviLote>umbralMin), 20, 10)))
    # Guardar la segmentacion
    fname = pNdviLote.split("/")[::-1][0].split(".")[0] 
    ndviSegmentado = ndviSegmentado.rio.write_crs('epsg:4326', inplace = True)
    ndviSegmentado.rio.to_raster(f'{pSalida}{fname}.tif')