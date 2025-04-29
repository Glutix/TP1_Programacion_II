from utils.constantes import MEDICOS_PATH
from utils.utilidades import validar_archivo, leer_json, escribir_json, generar_id
import os


def registrar_medico():
    nombre = input("Ingrese su nombre: ")
    apellido = input("Ingrese su apellido: ")
    especialidad = input("Ingrese su especialidad: ")

    # Obtener los datos existentes del archivo
    datos_existentes = leer_json(MEDICOS_PATH)

    # Verificar si ya existe el médico
    for elemento in datos_existentes:
        if (
            elemento["nombre"].lower() == nombre.lower()
            and elemento["apellido"].lower() == apellido.lower()
            and elemento["especialidad"].lower() == especialidad.lower()
        ):
            print("El médico ya está registrado.")
            return

    # Generar un ID automatico
    nuevo_id = generar_id(datos_existentes)

    # Crear la estructura de datos
    medico = {
        "id": nuevo_id,
        "nombre": nombre,
        "apellido": apellido,
        "especialidad": especialidad,
    }

    # Agregamos la nueva info
    datos_existentes.append(medico)

    # Sobre-escribir el archivo json con los datos actualizados
    escribir_json(MEDICOS_PATH, datos_existentes)


def listar_medicos():
    datos_existentes = leer_json(MEDICOS_PATH)

    if not datos_existentes:
        print("No hay médicos registrados.")
        return

    print("\nLista de mèdicos...")

    for medico in datos_existentes:
        print(
            f"ID: {medico["id"]} | {medico["nombre"]} {medico["apellido"]} | Especialidad: {medico["especialidad"]}"
        )
    print()


def menu_medicos():
    # Verificar si el archivo existe, si no, crearlo
    validar_archivo(MEDICOS_PATH)

    while True:
        print("Seleccione una opcioon: ")
        print("1. Registrar a un Médico")
        print("2. Lista de Médicos.")
        print("3. Volver al menu anterior.")
        print("4. Salir del programa (directamente).")

        try:
            opcion = int(input("Ingrese una opción: "))

            if opcion == 1:
                registrar_medico()

            elif opcion == 2:
                listar_medicos()

            elif opcion == 3:
                os.system("cls")
                break

            elif opcion == 4:
                print("Cerrando el programa...")
                exit()

        except ValueError:
            print("No se ingresó un número válido.")
            continue
