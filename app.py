from fastapi import FastAPI, File, UploadFile
from starlette.responses import FileResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from typing import Annotated
import os
import subprocess
from librerias.urlToGeojson import urlToGeojson
from monitoreo import monitoreoProcess 
from historico import historicoProcess 
import numpy as np
import rasterio


app = FastAPI()


@app.get("/")
async def read_root():
    return FileResponse('template/index.html')

app.mount("/assets", StaticFiles(directory="assets"), name="assets") 

## Ejecuta todas las funciones del run y genera las imagenes y el JSON con estadisticas
@app.get('/monitoreo/{fecha}/{idLote}')
def monitoreo(fecha:str, idLote:str):
    jsonFile= idLote + '.geojson'
    jsonPath = 'librerias/lotes/' + jsonFile
    assetPath= 'assets/monitoreo/'+ idLote
    productos = ["ndviTif", "productividadTif", "ndviPng", "ndviPngRecortado", "estadisticas", "productividadPng"]
    try:
        #descargo del endopoint el geojson de la parcela de siris
        urlToGeojson(idLote,jsonPath)

    except:
        return jsonable_encoder({f'Error': 'No se pudo procesar correctamente el geoJSON de la parcela '})
    for prod in productos:
        if not os.path.exists(f"{assetPath}/{prod}"):
            os.makedirs(f"{assetPath}/{prod}")

    #subprocess.run(["python", "monitoreo.py", fecha, jsonPath])
    monitoreoProcess(fecha, jsonPath, idLote )
    return jsonable_encoder({'status': 'Imagenes generadas correctamente'})


## Genera todas las imagenes en cascada e imprime un JSON con el status y la lista de imagenes generadas
@app.get('/historico/{fechaInicial}/{fechaFinal}/{idLote}')

def historico(fechaInicial:str, fechaFinal:str, idLote:str):
    jsonFile= idLote + '.geojson'
    jsonPath = 'librerias/lotes/' + jsonFile
    assetPath= 'assets/historico/'+ idLote
    productos = ["ndviTif", "productividadTif", "ndviPng", "ndviPngRecortado", "productividadPng"]
    try:
        urlToGeojson(idLote,jsonPath)
    except:
        return jsonable_encoder({'Error': 'No se pudo procesar correctamente el geoJSON de la parcela'})        
  
    # Verifica si las carpetas existen, si no existen, las crea
    
    for prod in productos:
            if not os.path.exists(f"{assetPath}/{prod}"):
                os.makedirs(f"{assetPath}/{prod}")
    # Ejecuta los procesos
    historicoProcess(fechaInicial, fechaFinal,jsonPath)       
    #subprocess.run(["python", "run.py", fechaInicial, fechaFinal, pathToLote])
    return jsonable_encoder({'status': "Imagenes generadas correctamente"})

## Para listar el contenido generado monitoreo
@app.get('/listFiles/{product}/{idLote}')
def get_asset(product,idLote):
    assets_path = 'assets/' + product + '/' + idLote


    data = {}
    def get_files(path):

        jsondata=[f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
  
        return jsondata
   
    if os.path.exists(assets_path):
       
        for date_range in os.listdir(assets_path):
            date_range_path = os.path.join(assets_path, date_range)

            if os.path.isdir(date_range_path):
                data[date_range] = {}
                i=0
                for lot in os.listdir(date_range_path):
                    date=lot.split('T',-1)
                    lot_path = os.path.join(date_range_path, lot)
                   
                    with rasterio.open(lot_path) as f:
                        arr = f.read(1)
                        mask = (arr != f.nodata)
                        elev = arr[mask]
                        col, row = np.where(mask)
                        x, y = f.xy(col, row)
                        uid = np.arange(f.height * f.width).reshape((f.height, f.width))[mask]

                    result = np.rec.fromarrays([uid, x, y, elev], names=['id', 'x', 'y', 'elev'])
                    data[date_range][date[0]]= {'date':date[0], 'data':lot_path,'meta':result}
                    print(result)  
                    i=i+1
                   

    
    return jsonable_encoder(data)

@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}
  
