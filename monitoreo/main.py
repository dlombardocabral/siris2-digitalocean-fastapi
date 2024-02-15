from sys import argv
from utils import getNdviS2, getNdviSegment, exportNdviPng, exportNdviPngClipped, exportJsonStatics, exportProductividadPng

argv = argv[1::]
funcionalidades = ["--getNdvi", "--exportNdviPng", "--exportNdviPngClipped", "--exportJsonStatics", "--exportProductividadPng"]

## ejecucion de funciones
## 1 se bajan los datos del GEE 
if argv[0] == "--getNdvi":
    getNdviS2(argv[1], argv[2], argv[3])
#=======================================
## 2 se segmentan las imagenes
if argv[0] == "--getNdviSegment":
    getNdviSegment(argv[1], argv[2], argv[3], argv[4])
#=======================================
## 3 se genera una imagen PNG
if argv[0] == "--exportNdviPng" :
    exportNdviPng(argv[1], argv[2], argv[3])
#=======================================
### 4 se genera una imagen PNG recortada
if argv[0] == "--exportNdviPngClipped":
    exportNdviPngClipped(argv[1], argv[2], argv[3])
#=======================================
### 5 Jse genera unSON con resumen estadistico
if argv[0] == "--exportJsonStatics":
    exportJsonStatics(argv[1], argv[2], argv[3])
#======================================= 
### 6 se genera una imagen PNG con la segmentacion para productividad
if argv[0] == "--exportProductividadPng" :
    exportProductividadPng(argv[1], argv[2], argv[3])