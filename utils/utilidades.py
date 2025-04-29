import json
import os
import time


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


def buscar_paciente_dni(dni, datos):
    for i, paciente in enumerate(datos):
        if paciente["dni"] == dni:
            return paciente, i
    return f"No se encontró el paciente con DNI: {dni}"


def generar_id(datos):
    if datos:
        max_id = 0
        for elemento in datos:
            if elemento["id"] > max_id:
                max_id = elemento["id"]
        nuevo_id = max_id + 1
    else:
        nuevo_id = 1

    return nuevo_id


def fecha_actual():
    tiempo_actual = time.localtime()

    # datos actuales
    anio = tiempo_actual.tm_year
    mes = tiempo_actual.tm_mon
    dia = tiempo_actual.tm_mday

    # Asegurarse de que el día y mes siempre tengan 2 dígitos
    fecha = f"{dia:02d}/{mes:02d}/{anio}"
    return fecha


def calcular_edad(fecha_nacimiento):
    # Datos actuales
    tiempo_actual = time.localtime()

    anio_actual = tiempo_actual.tm_year
    mes_actual = tiempo_actual.tm_mon
    dia_actual = tiempo_actual.tm_mday

    # datos recibidos
    dia = int(fecha_nacimiento[:2])
    mes = int(fecha_nacimiento[3:5])
    anio_nacimiento = int(fecha_nacimiento[6:])

    # calcular edad
    edad = anio_actual - anio_nacimiento

    # Ajustar la edad si no ha cumplido años aún este año
    if (mes_actual, dia_actual) < (mes, dia):
        edad -= 1

    return edad
