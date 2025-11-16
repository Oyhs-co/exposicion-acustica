import json
import csv
import logging
from shapely.geometry import shape
import os

def setup_logger(log_file="geojson_to_csv.log"):
    """Configura el logger para escribir en consola y en un archivo."""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Evitar duplicar handlers si se llama más de una vez
    if logger.hasHandlers():
        logger.handlers.clear()

    # Formato común
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Handler para archivo
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

# Crear logger global
logger = setup_logger()

def geojson_to_csv(geojson_path, csv_path, log_file="geojson_to_csv.log"):
    global logger
    # Si deseas un archivo de log personalizado por llamada, reconfigura el logger
    if log_file != "geojson_to_csv.log":
        logger = setup_logger(log_file)

    logger.info(f"Iniciando conversión de {geojson_path} a {csv_path}")

    if not os.path.isfile(geojson_path):
        logger.error(f"El archivo GeoJSON no existe: {geojson_path}")
        raise FileNotFoundError(f"No se encontró el archivo: {geojson_path}")

    try:
        with open(geojson_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info("Archivo GeoJSON cargado correctamente")
    except Exception as e:
        logger.error(f"Error al leer o parsear el archivo GeoJSON: {e}")
        raise

    if 'features' not in data:
        logger.error("El archivo GeoJSON no contiene la clave 'features'")
        raise ValueError("GeoJSON inválido: falta 'features'")

    features = data['features']
    logger.info(f"Se encontraron {len(features)} features en el GeoJSON")

    if not features:
        logger.warning("No hay features para procesar")
        return

    # Recopilar propiedades
    all_properties = set()
    for i, feature in enumerate(features):
        props = feature.get('properties') or {}
        if not isinstance(props, dict):
            logger.warning(f"Feature {i} tiene 'properties' no válido (no es un diccionario). Se omitirá.")
            continue
        all_properties.update(props.keys())

    all_properties = sorted(all_properties)
    logger.info(f"Propiedades detectadas: {all_properties}")

    fieldnames = all_properties + ['geometry_wkt']
    rows = []

    for i, feature in enumerate(features):
        try:
            row = {}
            props = feature.get('properties') or {}
            for prop in all_properties:
                row[prop] = props.get(prop, '')

            geom = feature.get('geometry')
            if geom:
                try:
                    shapely_geom = shape(geom)
                    row['geometry_wkt'] = shapely_geom.wkt
                except Exception as geom_error:
                    logger.warning(f"Error al convertir geometría de feature {i}: {geom_error}")
                    row['geometry_wkt'] = f"Error: {geom_error}"
            else:
                row['geometry_wkt'] = ''

            rows.append(row)

        except Exception as row_error:
            logger.error(f"Error al procesar feature {i}: {row_error}")
            continue

    logger.info(f"Procesamiento completado. Total de filas listas para escribir: {len(rows)}")

    try:
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        logger.info(f"Archivo CSV guardado exitosamente en: {csv_path}")
    except Exception as e:
        logger.error(f"Error al escribir el archivo CSV: {e}")
        raise

# Ejemplo de uso
if __name__ == "__main__":
    geojson_file = "track.geojson"   # Cambia por tu archivo de entrada
    csv_file = "datos.csv"           # Cambia por tu archivo de salida
    log_output = "conversion.log"    # Nombre del archivo de log (opcional)

    try:
        geojson_to_csv(geojson_file, csv_file, log_file=log_output)
    except Exception as e:
        logger.critical(f"Falló la conversión: {e}")
