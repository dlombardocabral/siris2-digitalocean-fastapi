def exportNdviPng(pNdviLote, pLote, pSalida):
    
    import matplotlib.pyplot as plt
    import rioxarray as rio
    import geopandas as gpd; import fiona
    fiona.drvsupport.supported_drivers['libkml'] = 'rw'
    fiona.drvsupport.supported_drivers['LIBKML'] = 'rw'
    
    ndviLote = rio.open_rasterio(pNdviLote)
    lote = gpd.read_file(pLote)
    
    # Para el titulo
    idLote = pNdviLote.split("/")[-1].split("-")[1]
    fecha = pNdviLote.split("/")[-1].split("-")[0] + "-" + pNdviLote.split("/")[-1].split("-")[1].split(".")[0]
    fname = pNdviLote.split("/")[::-1][0].split(".")[0]

    cmts = 1/2.54
    plt.rcParams.update({"font.size": 8})
    f, ax = plt.subplots(figsize = (16*cmts, 9*cmts))
    
    ndviLote.plot(cmap="RdYlGn", vmin = 0, vmax = 1, ax = ax)
    lote.plot(ax = ax, facecolor = "None")
    
    ax.set_title(f"NDVI - IDLote {idLote}" + "\n " + fecha)
    ax.set_xlabel("Longitudes"); ax.set_ylabel("Latitudes")
    
    plt.savefig(f'{pSalida}{fname}.png', dpi = 500, bbox_inches = 'tight')