from fastapi import FastAPI
from starlette.responses import FileResponse
from fastapi.encoders import jsonable_encoder
import os
import subprocess
from utils import urlToGeojson


app = FastAPI()


@app.get("/")
async def read_root():
    return FileResponse('template/index.html')

## Ejecuta todas las funciones del run y genera las imagenes y el JSON con estadisticas
@app.get('/monitoreo/{fecha}/{idLote}')
def read_item(fecha:str, idLote:int):
    try:
        #descargo del endopoint el geojson de la parcela de siris
        urlToGeojson(idLote)
    except:
        return jsonable_encoder({'Error': 'No se pudo procesar correctamente el geoJSON de la parcela'})
    pathToLote = "db/lotes/" + idLote + ".geojson"
    # Verifica si las carpetas existen, si no existen, las crea
    productos = ["ndvi-tif", "productividad-tif", "ndvi-png", "ndvi-png-recortado", "estadisticas", "productividad-png"]
    for prod in productos:
        if not os.path.exists(f"assets/{idLote}/{prod}"):
            os.makedirs(f"assets/{idLote}/{prod}")
    # Ejecuta los procesos
    subprocess.run(["python", "run.py", fecha, pathToLote])
    return jsonable_encoder({'status': 'Imagenes generadas correctamente'})

