import subprocess
import os
from monitoreolibrerias import getNdviS2, getNdviSegment, exportNdviPng, exportNdviPngClipped, exportJsonStatics, exportProductividadPng, clipTif
#from monitoreo_main import *
from pathlib import Path


def monitoreoProcess (fecha:str, jsonPath:str, idLote:str) : 
   
    ndviTif= f"assets/monitoreo/{idLote}/ndvi-tif/"
    productividadTif= f"assets/monitoreo/{idLote}/productividad-tif/"
    ndviPng=f"assets/monitoreo/{idLote}/ndvi-png/"
    ndviPngRecortado=f"assets/monitoreo/{idLote}/ndvi-png-recortado/"
    estadisticas=f"assets/monitoreo/{idLote}/estadisticas/"
    productividadPng=f"assets/monitoreo/{idLote}/productividad-png/"
   
    ## 1 se bajan los datos del GEE 
    #subprocess.check_output(["python", "main.py", "--getNdvi", jsonPath, fecha, f"assets/{idLote}/ndvi-tif/"])
    getNdviS2(jsonPath,fecha,ndviTif)


    ## 2 se segmentan las imagenes
    bajados = os.listdir(ndviTif)
    for tif in bajados:
        getNdviSegment(f"{ndviTif}{tif}","0.2", "0.5",productividadTif)
        #subprocess.run(["python", "main.py", "--getNdviSegment", f"assets/{idLote}/ndvi-tif/{tif}", "0.2", "0.5", f"assets/{idLote}/productividad-tif/"])
    segmentados = os.listdir(productividadTif)

    ## 3 se generan las imagenes
    for tif, tifSegmented in zip(bajados, segmentados):

    
        ### 3.1 se genera una imagen PNG
        exportNdviPng(f"{ndviTif}{tif}",jsonPath,ndviPng)
        #subprocess.run(["python", "main.py", "--exportNdviPng", f"assets/{idLote}/ndvi-tif/{tif}", jsonPath, ])

        ### 3.2 se genera una imagen PNG recortada
        exportNdviPngClipped(f"{ndviTif}{tif}",jsonPath,ndviPngRecortado)
        #subprocess.run(["python", "main.py", "--exportNdviPngClipped", f"assets/{idLote}/ndvi-tif/{tif}", jsonPath, f"assets/{idLote}/ndvi-png-recortado/"])
        
        exportJsonStatics(f"{ndviTif}{tif}",jsonPath,estadisticas)
        ### 3.3 Jse genera unJSON con resumen estadistico
        #subprocess.run(["python", "main.py", "--exportJsonStatics", f"assets/{idLote}/ndvi-tif/{tif}", jsonPath, f"assets/{idLote}/estadisticas/"])
        
        exportProductividadPng(f"{ndviTif}{tif}",jsonPath,productividadPng)
        ### 3.4 se genera una imagen PNG con la segmentacion para productividad
        #subprocess.run(["python", "main.py", "--exportProductividadPng", f"assets/{idLote}/productividad-tif/{tifSegmented}", jsonPath, f"assets/{idLote}/productividad-png/"])

    ## 4 una vez generadas las imagenes, se recortan los tiff solo en el area de la parcela
    for tif in os.listdir(ndviTif):
        clipTif(f"{ndviTif}{tif}", jsonPath)
    for tif in os.listdir(productividadTif):
        clipTif(f"{productividadTif}{tif}", jsonPath)


    