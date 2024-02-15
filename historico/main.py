from sys import argv; argv = argv[1::]
from utils import getNdviL5, getNdviL8, getNdviProductividad, exportNdviPng, exportNdviPngClipped, exportProductividadPng

funcionalidades = ["--getNdvi", "--getProductividad", "--exportNdviPng", "--exportNdviPngClipped", "--exportProductividadPng"]

##=====
if argv[0] == "--getNdvi":
    ## Si Landsat-5
    if int(argv[2].split("-")[0]) < 2012:
        getNdviL5(argv[1], argv[2], argv[3], argv[4])
    ## Si Landsat-8
    elif int(argv[2].split("-")[0]) > 2013:
        print(argv[1])
        getNdviL8(argv[1], argv[2], argv[3], argv[4])
##=====
if argv[0] == "--getProductividad":
    getNdviProductividad(argv[1], float(argv[2]), float(argv[3]), argv[4])
##=====
if argv[0] == "--exportNdviPng":
    exportNdviPng(argv[1], argv[2], argv[3])
##=====
if argv[0] == "--exportNdviPngClipped":
    exportNdviPngClipped(argv[1], argv[2], argv[3])
##=====
if argv[0] == "--exportProductividadPng":
    exportProductividadPng(argv[1], argv[2], argv[3])