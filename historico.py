import subprocess
import os
from historicolibreria import clipTif, getNdvi, exportNdviPng,exportNdviPngClipped,exportProductividadPng,getNdviProductividad

def historicoProcess (fechaInicial:str, fechaFinal:str, pathToLote:str) : 
    ## Argumentos de entrada
    fini = fechaInicial # "2020-01-01"
    ffin = fechaFinal # "2021-01-01"
    pLote = pathToLote # "path/to/lote.geojson"
    lote = pLote.split("/")[-1]
    idLote = lote.split(".")[0]
    ndviTif= f"assets/historico/{idLote}/ndvi-tif/"
    productividadTif= f"assets/historico/{idLote}/productividad-tif/"
    ndviPng=f"assets/historico/{idLote}/ndvi-png/"
    ndviPngRecortado=f"assets/historico/{idLote}/ndvi-png-recortado/"
    productividadPng=f"assets/historico/{idLote}/productividad-png/"

    ## complementarios

    yini = fini.split("-")[0]; yfin = ffin.split("-")[0]
    parseDateI = fini.replace("-", ""); parseDateF = ffin.replace("-", "")
    pSalida = f"assets/historico/{idLote}/"

    
   
    if int(fini.split("-")[0]) < 2012:
       getNdvi.getNdviL5(pLote, fini, ffin, ndviTif)
    ## Si Landsat-8
    elif int(fini.split("-")[0]) > 2013:  
        getNdvi.getNdviL8(pLote, fini, ffin, ndviTif)
    ## 1. Bajar el campo NDVI (tif)
    #subprocess.check_output(["python", "main.py", "--getNdvi", pLote, fini, ffin, pSalida+"ndvi-tif/"])
  
    ## 2. Segmentar el NDVI para calcular productividad (tif)

    getNdviProductividad(f"{ndviTif}{fini.replace("-", "")}-{ffin.replace("-", "")}.tif", int(0.5), int(0.75), productividadTif)
    #subprocess.check_output(["python", "main.py", "--getProductividad", f"{pSalida}ndvi-tif/{fini.replace("-", "")}-{ffin.replace("-", "")}.tif", "0.5", "0.75", pSalida+"productividad-tif/"])
  
    ## 3. Grafico NDVI PNG
    exportNdviPng(f"{ndviTif}{fini.replace("-", "")}-{ffin.replace("-", "")}.tif", pLote, ndviPng)
    #subprocess.run(["python", "main.py", "--exportNdviPng", f"{pSalida}ndvi-tif/{fini.replace("-", "")}-{ffin.replace("-", "")}.tif", pLote, pSalida+"ndvi-png/"])

    ## 4. Grafico NDVI recortado solo lote PNG
    exportNdviPngClipped(f"{ndviTif}{fini.replace("-", "")}-{ffin.replace("-", "")}.tif", pLote, ndviPngRecortado)
    #subprocess.check_output(["python", "main.py", "--exportNdviPngClipped", f"{pSalida}ndvi-tif/{fini.replace("-", "")}-{ffin.replace("-", "")}.tif", pLote, pSalida+"ndvi-png-recortado/"])

    ## 5. Grafico Productividad PNG
    exportProductividadPng(f"{productividadTif}{fini.replace("-", "")}-{ffin.replace("-", "")}.tif", pLote, productividadPng)
    #subprocess.run(["python", "main.py", "--exportProductividadPng", f"{pSalida}productividad-tif/{fini.replace("-", "")}-{ffin.replace("-", "")}.tif", pLote, pSalida+"productividad-png/"])

    ## 6. una vez generadas las imagenes, se recortan los tiff solo en el area de la parcela
    for tif in os.listdir(ndviTif):
        clipTif(f"{ndviTif}{tif}", pLote)
    for tif in os.listdir(productividadTif):
        clipTif(f"{productividadTif}{tif}", pLote)