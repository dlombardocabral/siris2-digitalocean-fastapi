import subprocess
from sys import argv; argv = argv[1::]
from utils import clipTif
import os

## Argumentos de entrada
fini = argv[0] # "2020-01-01"
ffin = argv[1] # "2021-01-01"
pLote = argv[2] # "path/to/lote.geojson"

## complementarios
lote = pLote.split("/")[-1]
idLote = lote.split(".")[0]
yini = fini.split("-")[0]; yfin = ffin.split("-")[0]
parseDateI = fini.replace("-", ""); parseDateF = ffin.replace("-", "")
pSalida = f"assets/{idLote}/"

## 1. Bajar el campo NDVI (tif)
subprocess.check_output(["python", "main.py", "--getNdvi", pLote, fini, ffin, pSalida+"ndvi-tif/"])

## 2. Segmentar el NDVI para calcular productividad (tif)
subprocess.check_output(["python", "main.py", "--getProductividad", f"{pSalida}ndvi-tif/{fini.replace("-", "")}-{ffin.replace("-", "")}.tif", "0.5", "0.75", pSalida+"productividad-tif/"])

## 3. Grafico NDVI PNG
subprocess.run(["python", "main.py", "--exportNdviPng", f"{pSalida}ndvi-tif/{fini.replace("-", "")}-{ffin.replace("-", "")}.tif", pLote, pSalida+"ndvi-png/"])

## 4. Grafico NDVI recortado solo lote PNG
subprocess.check_output(["python", "main.py", "--exportNdviPngClipped", f"{pSalida}ndvi-tif/{fini.replace("-", "")}-{ffin.replace("-", "")}.tif", pLote, pSalida+"ndvi-png-recortado/"])

## 5. Grafico Productividad PNG
subprocess.run(["python", "main.py", "--exportProductividadPng", f"{pSalida}productividad-tif/{fini.replace("-", "")}-{ffin.replace("-", "")}.tif", pLote, pSalida+"productividad-png/"])

## 6. una vez generadas las imagenes, se recortan los tiff solo en el area de la parcela
for tif in os.listdir(f"assets/{idLote}/ndvi-tif/"):
    clipTif(f"assets/{idLote}/ndvi-tif/{tif}", pLote)
for tif in os.listdir(f"assets/{idLote}/productividad-tif/"):
    clipTif(f"assets/{idLote}/productividad-tif/{tif}", pLote)