import json
import os


def validar_archivo(path):
    if not os.path.exists(path):
        with open(path, "w") as file:
            json.dump([], file)
    else:
        try:
            with open(path, "r") as file:
                json.load(file)
        except json.JSONDecodeError:
            print("El archivo no es un JSON válido. Se creará uno nuevo.")
            with open(path, "w") as file:
                json.dump([], file)


def leer_json(path):
    # Obtener los datos existentes del archivo
    with open(path, "r") as file:
        try:
            datos_existentes = json.load(file)
        except json.JSONDecodeError:
            datos_existentes = []

    return datos_existentes


def escribir_json(path, datos):
    # Sobrescribir el archivo JSON con los datos actualizados
    with open(path, "w") as file:
        json.dump(datos, file, indent=4)
    print("Datos guardados correctamente.")
