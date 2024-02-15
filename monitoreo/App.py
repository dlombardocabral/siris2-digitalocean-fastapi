from flask import Flask, jsonify, send_file
import os
import subprocess
from utils import urlToGeojson

app = Flask(__name__)

## Ejecuta todas las funciones del run y genera las imagenes y el JSON con estadisticas
@app.route('/generate/<fecha>/<idLote>', methods=['GET'])
def generate(fecha, idLote):
    try:
        urlToGeojson(idLote)
    except:
        return jsonify({'Error': 'No se pudo procesar correctamente el geoJSON de la parcela'})
    pathToLote = "db/lotes/" + idLote + ".geojson"
    # Verifica si las carpetas existen, si no existen, las crea
    productos = ["ndvi-tif", "productividad-tif", "ndvi-png", "ndvi-png-recortado", "estadisticas", "productividad-png"]
    for prod in productos:
        if not os.path.exists(f"assets/{idLote}/{prod}"):
            os.makedirs(f"assets/{idLote}/{prod}")
    # Ejecuta los procesos
    subprocess.run(["python", "run.py", fecha, pathToLote])
    return jsonify({'status': 'Imagenes generadas correctamente'})

## Para listar el contenido generado
@app.route('/listFiles', methods=['GET'])
def get_assets():
    assets_path = 'assets/'
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
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
