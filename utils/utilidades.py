import json
import os
from datetime import datetime


def solicitar_datos(campos):
    return {c: input(f"Ingrese {c}: ").strip() for c in campos}


def crear_registro(lista_existente, nuevo_dato, campos):
    nuevo_id = generar_id(lista_existente)
    nuevo_registro = {"id": nuevo_id, **{campo: nuevo_dato[campo] for campo in campos}}
    return lista_existente + [nuevo_registro]


def actualizar_registro(original, nuevos_valores):
    return {clave: nuevos_valores.get(clave) or original[clave] for clave in original}


def eliminar_registro(datos, registro):
    return [e for e in datos if e != registro]


def existe_dni(datos, dni):
    return any(p["dni"] == dni for p in datos)


def obtener_por_dni(datos, dni):
    return next((p for p in datos if p["dni"] == dni), None)


def validar_archivo(path):
    try:
        with open(path, "r") as file:
            json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        with open(path, "w") as file:
            json.dump([], file)


def leer_json(path):
    validar_archivo(path)
    with open(path, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []


def escribir_json(path, datos):
    with open(path, "w") as file:
        json.dump(datos, file, indent=4)


def generar_id(datos):
    if datos:
        return max(registro["id"] for registro in datos) + 1
    return 1


def fecha_actual():
    return datetime.today().strftime("%d/%n/%Y")


def calcular_edad(fecha_nacimiento):
    nacimiento = datetime.strptime(fecha_nacimiento, "%d/%m/%Y")
    hoy = datetime.today()
    edad = hoy.year - nacimiento.year
    if (hoy.month, hoy.day) < (nacimiento.month, nacimiento.day):
        edad -= 1
    return edad


def limpiar_consola():
    os.system("cls" if os.name == "nt" else "clear")
