import subprocess
import os
from sys import argv; argv = argv[1::]
from utils import clipTif

fecha = argv[0]
pLote = argv[1] 
lote = pLote.split("/")[-1]; idLote = lote.split(".")[0]

## 1 se bajan los datos del GEE 
subprocess.check_output(["python", "main.py", "--getNdvi", pLote, fecha, f"assets/{idLote}/ndvi-tif/"])

## 2 se segmentan las imagenes
bajados = os.listdir(f"assets/{idLote}/ndvi-tif/")
for tif in bajados:
    subprocess.run(["python", "main.py", "--getNdviSegment", f"assets/{idLote}/ndvi-tif/{tif}", "0.2", "0.5", f"assets/{idLote}/productividad-tif/"])
segmentados = os.listdir(f"assets/{idLote}/productividad-tif/")

## 3 se generan las imagenes
for tif, tifSegmented in zip(bajados, segmentados):

    ### 3.1 se genera una imagen PNG
    subprocess.run(["python", "main.py", "--exportNdviPng", f"assets/{idLote}/ndvi-tif/{tif}", pLote, f"assets/{idLote}/ndvi-png/"])

    ### 3.2 se genera una imagen PNG recortada
    subprocess.run(["python", "main.py", "--exportNdviPngClipped", f"assets/{idLote}/ndvi-tif/{tif}", pLote, f"assets/{idLote}/ndvi-png-recortado/"])
    
    ### 3.3 Jse genera unJSON con resumen estadistico
    subprocess.run(["python", "main.py", "--exportJsonStatics", f"assets/{idLote}/ndvi-tif/{tif}", pLote, f"assets/{idLote}/estadisticas/"])
    
    ### 3.4 se genera una imagen PNG con la segmentacion para productividad
    subprocess.run(["python", "main.py", "--exportProductividadPng", f"assets/{idLote}/productividad-tif/{tifSegmented}", pLote, f"assets/{idLote}/productividad-png/"])

## 4 una vez generadas las imagenes, se recortan los tiff solo en el area de la parcela
for tif in os.listdir(f"assets/{idLote}/ndvi-tif/"):
    clipTif(f"assets/{idLote}/ndvi-tif/{tif}", pLote)
for tif in os.listdir(f"assets/{idLote}/productividad-tif/"):
    clipTif(f"assets/{idLote}/productividad-tif/{tif}", pLote)


    