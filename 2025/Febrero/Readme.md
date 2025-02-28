# Proyecto: Análisis de temperatura a 2 metros en áreas urbanas de Alemania

Este proyecto tiene como objetivo analizar la temperatura a 2 metros sobre áreas urbanas de Alemania utilizando datos del reanálisis ERA5-Land. Se han utilizado dos enfoques principales:

1. **Google Earth Engine (GEE)**: Para procesar y cruzar datos de temperatura con polígonos de áreas urbanas.
2. **API del Climate Data Store (CDS) de Copernicus**: Para descargar y procesar datos de temperatura año por año.

---

## Descripción del proyecto

### Objetivo
El objetivo principal es calcular la temperatura media diaria a 2 metros sobre áreas urbanas de Alemania desde 1950, utilizando datos del reanálisis ERA5-Land. Los resultados se cruzan con polígonos de áreas urbanas para obtener estadísticas zonal (media, mínimo, máximo, std) y exportar los resultados en formato CSV.

---

## Enfoques utilizados

### 1. Google Earth Engine (GEE)
Se ha desarrollado un script en JavaScript que utiliza el dataset **ERA5-Land Hourly - ECMWF Climate Reanalysis** disponible en GEE ([enlace al dataset](https://developers.google.com/earth-engine/datasets/catalog/ECMWF_ERA5_LAND_HOURLY?hl=es-419)).

#### Pasos realizados en GEE:
1. **Cálculo de la media diaria**: A partir de los datos horarios, se calcula la temperatura media diaria en grados centígrados.
2. **Cruce con polígonos urbanos**: Se utilizan las herramientas reduceRegions de GEE para cruzar los datos de temperatura con los polígonos de áreas urbanas de Alemania.
3. **Exportación de resultados**: Los resultados se exportan en formato CSV para su análisis posterior.

#### Archivos adjuntos:
- `script_gee.js`: Código JavaScript utilizado en GEE.
- `resultados_gee.csv`: Resultados exportados desde GEE (entregado a VH). 

---

### 2. API del Climate Data Store (CDS) de Copernicus
Se ha utilizado la API del CDS para descargar datos de temperatura a 2 metros desde 1950. Debido a las limitaciones de la API (lentitud y límites de volumen), se han descargado los datos año por año y se entregan a VH los datos de la decada de 1950 y el código para su procesado en Python.

#### Pasos realizados con la API:
1. **Descarga de datos**: Se han descargado los datos de temperatura para varios años de prueba utilizando la API del CDS.
2. **Procesado de archivos**: Los archivos descargados se han procesado en Python para calcular estadísticas zonal (media, mínimo, máximo, std) y cruzarlos con los polígonos de áreas urbanas.

#### Archivos adjuntos:
- `cds_analysis.ipynb`: Código Python para la descarga y procesado de datos desde la API del CDS, y del csv descargado de Google Earth Engine.

---

## Comparación de enfoques

| Característica              | Google Earth Engine (GEE)         | API del CDS de Copernicus       |
|-----------------------------|-----------------------------------|---------------------------------|
| **Velocidad de procesado**  | Muy rápido                        | Lento (descarga año por año)    |
| **Volumen de datos**        | Sin límites (en la nube)          | Limitado por la API             |
| **Facilidad de uso**        | Fácil (herramientas integradas)   | Requiere más configuración      |
| **Exportación de resultados**| Directa a CSV                     | Requiere procesado adicional    |

---

## Instrucciones para replicar el proyecto

### Requisitos
- Cuenta en **Google Earth Engine**.
- Cuenta en el **Climate Data Store (CDS)** de Copernicus.
- Python 3.x con las siguientes librerías:
  - `xarray`
  - `netCDF4`
  - `rasterstats`
  - `geopandas`
  - `cdsapi`

### Pasos
1. **Procesado en GEE**:
   - Ejecuta el script `script_gee.js` en Google Earth Engine.
   - Exporta los resultados a CSV (`resultados_gee.csv`).

2. **Descarga y procesado con la API del CDS**:
   - Ejecuta `descarga_cds.py` para descargar los datos desde la API del CDS.
   - Procesa los archivos descargados con `procesado_netcdf.py`.
   - Los resultados se guardan en `resultados_cds.csv`.

---


## Autores
- **Diego García Díaz**: LAST-EBD.
- **VH**: Investigadora Ramón y Cajal solicitante de la consulta.

---

## Licencia
Este proyecto está bajo la licencia [MIT](https://opensource.org/licenses/MIT). Siéntete libre de usarlo y modificarlo según tus necesidades.

---

## Agradecimientos
- **Google Earth Engine**: Por proporcionar una plataforma poderosa para el análisis de datos geoespaciales.
- **Climate Data Store (CDS) de Copernicus**: Por ofrecer acceso a datos climáticos de alta calidad.
- **Comunidad de Python**: Por las increíbles librerías que hacen posible el procesado de datos.
- **Plataformas IA**: Supogo que es como agradecer al excel o a Google Docs, pero la verdad es que ayudan mucho! ;P

---

¡Gracias por revisar este proyecto! 😊
