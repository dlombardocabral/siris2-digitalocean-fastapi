def urlToGeojson(idLote):

    import geopandas as gpd
    import requests

    lote = idLote
    pSalida = "db/lotes/"

    response = requests.get(f"http://www.sistemasiris.org/api/getgeojson/{lote}", verify=False)

    

    geojson = gpd.GeoDataFrame.from_features(response.json()["features"])



    geojson.to_file(f"{pSalida}{lote}.geojson", driver="GeoJSON")