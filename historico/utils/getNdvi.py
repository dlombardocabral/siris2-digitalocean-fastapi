def getNdviL8(lote, fini, ffin, pSalida):
    
    import ee
    import geemap
    ee.Initialize()
    
    yini = fini.split("-")[0]; yfin = ffin.split("-")[0]
    idLote = lote.split("/")[-1].split(".")[0]
    
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
    dataset = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2').filterDate(fini, ffin).filterBounds(roi)

    # Funcion para aplicar factores de escala en las bandas
    def applyScaleFactors(image):
        opticalBands = image.select('SR_B.').multiply(0.0000275).add(-0.2)
        return image.addBands(opticalBands, None, True)

    # Función para calcular NDVI y agregarlo como una banda a la imagen.
    def addNDVI(image):
        ndvi = image.normalizedDifference(['SR_B5', 'SR_B4']).rename('NDVI')
        return image.addBands(ndvi)

    # Aplicar los factores de escala a las nuevas bandas de NDVI.
    datasetWithScaled = dataset.map(applyScaleFactors)
    # Aplicar la función addNDVI a cada imagen en el dataset.
    NDVI = datasetWithScaled.map(addNDVI)

    # Define una función para calcular y agregar propiedades a cada imagen de la colección
    def agregarPropiedades(imagen):
        # Selecciona la banda NDVI
        ndvi = imagen.select('NDVI')

        # Recorta la imagen utilizando la geometría predefinida (roi)
        imagenRecortada = ndvi.clip(roi)

        # Calcula la cantidad de píxeles con NDVI superior a 0.5
        pixelesSuperioresA0_5 = imagenRecortada.gt(0.5).reduceRegion(
            reducer=ee.Reducer.sum(),
            geometry=roi,
            scale=30,
            maxPixels=1e9
        )

        # Obtiene la cantidad total de píxeles de la imagen recortada
        totalPixeles = imagenRecortada.reduceRegion(
            reducer=ee.Reducer.count(),
            geometry=roi,
            scale=30,
            maxPixels=1e9
        )

        porcentaje = ee.Number(pixelesSuperioresA0_5.get('NDVI')).divide(
            ee.Number(totalPixeles.get('NDVI'))).multiply(100)

        # Agrega las propiedades al diccionario de propiedades de la imagen
        return imagen.set({
        'pixelesSuperioresA0_5': pixelesSuperioresA0_5.get('NDVI'),
        'totalPixeles': totalPixeles.get('NDVI'),
        'porcentaje': porcentaje
        })

    # Aplica la función de agregar propiedades al dataset. Luego selecciona la banda NDVI  
    NDVI = NDVI.map(agregarPropiedades).select('NDVI')

    # Filtro la coleccion de acuerdo a que porcentaje sea mayor a 70%
    ndviFiltrado = NDVI.filter(ee.Filter.gte('porcentaje', 70))

    # Obtiene el NDVI máximo de la campaña
    ndviMaxCampania = ndviFiltrado.reduce(ee.Reducer.max())

    #===================================================
    geemap.ee_export_image(ndviMaxCampania, filename=f"{pSalida}{fini.replace("-", "")}-{ffin.replace("-", "")}.tif", scale=30, region=roi.geometry())
    
    return(f"{pSalida}{fini.replace("-", "")}-{ffin.replace("-", "")}.tif")

def getNdviL5(lote, fini, ffin, pSalida):
    
    import ee
    import geemap
    ee.Initialize()
    
    yini = fini.split("-")[0]; yfin = ffin.split("-")[0]
    idLote = lote.split("/")[-1].split(".")[0]
    
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
    dataset = ee.ImageCollection('LANDSAT/LT05/C02/T1_L2').filterDate(fini, ffin).filterBounds(roi)

    # Funcion para aplicar factores de escala en las bandas
    def applyScaleFactors(image):
        opticalBands = image.select('SR_B.').multiply(0.0000275).add(-0.2)
        return image.addBands(opticalBands, None, True)

    # Función para calcular NDVI y agregarlo como una banda a la imagen.
    def addNDVI(image):
        ndvi = image.normalizedDifference(['SR_B4', 'SR_B3']).rename('NDVI')
        return image.addBands(ndvi)

    # Aplicar los factores de escala a las nuevas bandas de NDVI.
    datasetWithScaled = dataset.map(applyScaleFactors)
    # Aplicar la función addNDVI a cada imagen en el dataset.
    NDVI = datasetWithScaled.map(addNDVI)

    # Define una función para calcular y agregar propiedades a cada imagen de la colección
    def agregarPropiedades(imagen):
        # Selecciona la banda NDVI
        ndvi = imagen.select('NDVI')

        # Recorta la imagen utilizando la geometría predefinida (roi)
        imagenRecortada = ndvi.clip(roi)

        # Calcula la cantidad de píxeles con NDVI superior a 0.5
        pixelesSuperioresA0_5 = imagenRecortada.gt(0.5).reduceRegion(
            reducer=ee.Reducer.sum(),
            geometry=roi,
            scale=30,
            maxPixels=1e9
        )

        # Obtiene la cantidad total de píxeles de la imagen recortada
        totalPixeles = imagenRecortada.reduceRegion(
            reducer=ee.Reducer.count(),
            geometry=roi,
            scale=30,
            maxPixels=1e9
        )

        porcentaje = ee.Number(pixelesSuperioresA0_5.get('NDVI')).divide(
            ee.Number(totalPixeles.get('NDVI'))).multiply(100)

        # Agrega las propiedades al diccionario de propiedades de la imagen
        return imagen.set({
        'pixelesSuperioresA0_5': pixelesSuperioresA0_5.get('NDVI'),
        'totalPixeles': totalPixeles.get('NDVI'),
        'porcentaje': porcentaje
        })

    # Aplica la función de agregar propiedades al dataset. Luego selecciona la banda NDVI  
    NDVI = NDVI.map(agregarPropiedades).select('NDVI')

    # Filtro la coleccion de acuerdo a que porcentaje sea mayor a 70%
    ndviFiltrado = NDVI.filter(ee.Filter.gte('porcentaje', 70))

    # Obtiene el NDVI máximo de la campaña
    ndviMaxCampania = ndviFiltrado.reduce(ee.Reducer.max())

    #===================================================
    geemap.ee_export_image(ndviMaxCampania, filename=f"{pSalida}{fini.replace("-", "")}-{ffin.replace("-", "")}.tif", scale=30, region=roi.geometry())
    
    return(f"{pSalida}{fini.replace("-", "")}-{ffin.replace("-", "")}.tif")
