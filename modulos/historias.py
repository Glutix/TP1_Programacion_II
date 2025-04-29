from utils.constantes import HISTORIAS_PATH
from utils.utilidades import validar_archivo, leer_json, escribir_json
import os


def agregar_historial_clinico():
    datos_existentes = leer_json(HISTORIAS_PATH)


def menu_historial_clinico():
    # Verificar si el archivo existe, si no, crearlo
    validar_archivo(HISTORIAS_PATH)

    while True:
        print("Eliga una opcion:")
        print("1. Agregar una historia clinica a un paciente.")
        print("2. Volver al menu anterior.")
        print("3. Salir del programa (directamente).")

        try:
            opcion = int(input("Ingrese una opción: "))

            if opcion == 1:
                agregar_historial_clinico()

            elif opcion == 2:
                os.system("cls")
                break

            elif opcion == 3:
                print("Cerrando el programa...")
                exit()

        except ValueError:
            print("No se ingresó un número válido.")
            continue
