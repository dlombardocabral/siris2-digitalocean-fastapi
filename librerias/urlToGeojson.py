import geopandas as gpd
import requests 

def urlToGeojson(idLote,jsonPath):
   
    response = requests.get(f"http://www.sistemasiris.org/api/getgeojson/{idLote}", verify=False)
    geojson = gpd.GeoDataFrame.from_features(response.json()["features"])
    return geojson.to_file( jsonPath , driver="GeoJSON")