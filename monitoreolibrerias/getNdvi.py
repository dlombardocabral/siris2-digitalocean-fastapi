import ee
import geemap
import pandas as pd
from datetime import datetime, timedelta
#ee.Authenticate(auth_mode=locals)
ee.Initialize()

def getNdviS2(lote, fecha, pSalida):

    ## Parametros inciales
    nombreLote = lote.split("/")[-1::][0].split(".")[0]
    endDate = pd.to_datetime(fecha).strftime("%Y-%m-%d")
    initDate = (pd.to_datetime(fecha)+timedelta(days=-30)).strftime("%Y-%m-%d")
    
    # Carga el lote a geemap de acuerdo a su extension
    extLote = lote.split("/")[::-1][0].split(".")[::-1][0]
    if extLote == "geojson":
        roi = geemap.geojson_to_ee(lote)
    elif extLote == "kml":
        roi = geemap.kml_to_ee(lote)
    else :
        print(f"La extension '.{extLote}' no es valida \n Exec app")
        exit()
    ##

    # Defino el dataset principal
    dataset = ee.ImageCollection('COPERNICUS/S2_SR').filterDate(initDate, endDate).filterBounds(roi).filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))

    # Función para calcular NDVI y agregarlo como una banda a la imagen.
    def addNDVI(image):
        ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
        return image.addBands(ndvi)

    # Aplicar la función addNDVI a cada imagen en el dataset.
    ndvi = dataset.map(addNDVI)

    ## Para cada imagen de la ImageCollection, guardo en local
    listaImagenes = ndvi.select("NDVI").toList(ndvi.size())
    #print(listaImagenes.getInfo())
    for i in range(len(listaImagenes.getInfo())):
        

        imagen = ee.Image(listaImagenes.get(i))
  
        fechaObjeto = imagen.getInfo()['properties']['GRANULE_ID'].split("_")[3]
        fechaParseada = str(datetime.strptime(fechaObjeto, "%Y%m%dT%H%M%S").strftime("%Y-%m-%dT%H:%M:%S"))

        #===================================================
        #pSalida='siris2-digitalocean-fastapi/assets/monitoreo/1/ndvi-tif'
        geemap.ee_export_image(imagen, filename=f"{pSalida}{fechaParseada}.tif", scale=10, region=roi.geometry(), crs="EPSG:4326", unzip=True, timeout=3000)
