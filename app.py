from fastapi import FastAPI
from starlette.responses import FileResponse
from fastapi.encoders import jsonable_encoder
import os
import subprocess
from librerias import urlToGeojson


app = FastAPI()


@app.get("/")
async def read_root():
    return FileResponse('template/index.html')

## Ejecuta todas las funciones del run y genera las imagenes y el JSON con estadisticas
@app.get('/monitoreo/{fecha}/{idLote}')
def monitoreo(fecha:str, idLote:int):
    try:
        #descargo del endopoint el geojson de la parcela de siris
        jsonlote=urlToGeojson(idLote)
    except:
        return jsonable_encoder({f'Error': 'No se pudo procesar correctamente el geoJSON de la parcela {jsonlote}'})
    pathToLote = "db/lotes/" + idLote + ".geojson"
    # Verifica si las carpetas existen, si no existen, las crea
    productos = ["ndvi-tif", "productividad-tif", "ndvi-png", "ndvi-png-recortado", "estadisticas", "productividad-png"]
    for prod in productos:
        if not os.path.exists(f"assets/{idLote}/{prod}"):
            os.makedirs(f"assets/{idLote}/{prod}")

    # Ejecuta los procesos
    subprocess.run(["python", "run.py", fecha, pathToLote])
    return jsonable_encoder({'status': 'Imagenes generadas correctamente'})


## Genera todas las imagenes en cascada e imprime un JSON con el status y la lista de imagenes generadas
@app.get('/historico/{fechaInicial}/{fechaFinal}/{idLote}')
def historico(fechaInicial:str, fechaFinal:str, idLote:int):
    try:
        urlToGeojson(idLote)
    except:
        return jsonable_encoder({'Error': 'No se pudo procesar correctamente el geoJSON de la parcela'})        
    pathToLote = "db/lotes/" + idLote + ".geojson"
    # Verifica si las carpetas existen, si no existen, las crea
    productos = ["ndvi-tif", "productividad-tif", "ndvi-png", "ndvi-png-recortado", "productividad-png"]
    for prod in productos:
            if not os.path.exists(f"assets/{idLote}/{prod}"):
                os.makedirs(f"assets/{idLote}/{prod}")
    # Ejecuta los procesos
    subprocess.run(["python", "run.py", fechaInicial, fechaFinal, pathToLote])
    return jsonable_encoder({'status': "Imagenes generadas correctamente"})

## Para listar el contenido generado monitoreo
@app.get('/listFiles/{product}/{idLote}')
def get_asset(product,idLote):
    assets_path = product + '/assets/' + idLote
    data = {}
    def get_files(path):
        return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    if os.path.exists(assets_path):
        for date_range in os.listdir(assets_path):
            date_range_path = os.path.join(assets_path, date_range)
            if os.path.isdir(date_range_path):
                data[date_range] = {}
                for lot in os.listdir(date_range_path):
                    lot_path = os.path.join(date_range_path, lot)
                    if os.path.isdir(lot_path):
                        data[date_range][lot] = get_files(lot_path)                
    
    return jsonable_encoder(data)

