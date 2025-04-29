from utils.constantes import HISTORIAS_PATH, PACIENTES_PATH, MEDICOS_PATH
from utils.utilidades import (
    validar_archivo,
    leer_json,
    escribir_json,
    generar_id,
    buscar_paciente_dni,
    fecha_actual,
)
import os


def agregar_historial_clinico():
    # Datos del paciente
    dni_paciente = input("Ingresar DNI del paciente: ")

    # Cargamos los pacientes
    pacientes = leer_json(PACIENTES_PATH)

    # Retorna un string si no se encontro, o una tupla si se encontro (paciente, indice).
    resultado_busqueda = buscar_paciente_dni(dni_paciente, pacientes)

    # Verificar si no se encontro el paciente
    if isinstance(resultado_busqueda, str):
        print(resultado_busqueda)
        return

    # Si se encontro recuperamos su id
    id_paciente = resultado_busqueda[0]["id"]

    print("Paciente encontrado...")
    for clave, valor in resultado_busqueda[0].items():
        print(f"{clave} - {valor}")

    # Datos del medico
    nombre_medico = input("Nombre del medico que lo trato: ")
    apellido_medico = input("Ingresar apellido del medico que lo trato: ")
    especialidad_medico = input("Ingresar especialidad del medico: ")

    # Obtener los datos existentes del archivo (medicos)
    medicos = leer_json(MEDICOS_PATH)

    # Verificar si ya existe el médico
    medico_encontrado = None
    for elemento in medicos:
        if (
            elemento["nombre"].lower() == nombre_medico.lower()
            and elemento["apellido"].lower() == apellido_medico.lower()
            and elemento["especialidad"].lower() == especialidad_medico.lower()
        ):
            medico_encontrado = elemento
            break

    if medico_encontrado is None:
        print("No se encontro el medico.")
        return

    # recuperamos el id del medico
    id_medico = medico_encontrado["id"]

    # Datos de la historia clinica
    enfermedad_aficcion = input("Ingresar enfermedad o aficcion que padece: ")
    observaciones = input("ingresar obersvaciones: ")
    fecha = input("Ingresar fecha en que fue atendido, si es hoy ignorar este campo:")

    # Recuperamos las historias existentes
    datos_existentes = leer_json(HISTORIAS_PATH)

    # Generar un id para la nueva historia
    nuevo_id = generar_id(datos_existentes)

    # Creamos la estructura de datos para la nueva historia clinica
    nueva_historia = {
        "id": nuevo_id,
        "id_medico": id_medico,
        "id_paciente": id_paciente,
        "enfermedad_aficcion": enfermedad_aficcion,
        "observaciones": observaciones,
        "fecha": fecha if fecha else fecha_actual(),
    }

    # Agergamos la nueva historia clinica a lods datos existentes
    datos_existentes.append(nueva_historia)

    # Actualizamos la informacion en el archivo
    escribir_json(HISTORIAS_PATH, datos_existentes)
    print("Historia clinica agregada correctamente")


def listar_historial_clinico():
    datos_existentes = leer_json(HISTORIAS_PATH)

    if not datos_existentes:
        print("No hay historiales clinicos registrados.")
        return

    print("\nLista de historiales clinico...")

    for elemento in datos_existentes:
        print(elemento)
    print()


def menu_historial_clinico():
    # Verificar si el archivo existe, si no, crearlo
    validar_archivo(HISTORIAS_PATH)

    while True:
        print("Eliga una opcion:")
        print("1. Agregar una historia clinica a un paciente.")
        print("2. Listar historiales clinicos")
        print("3. Volver al menu anterior.")
        print("4. Salir del programa (directamente).")

        try:
            opcion = int(input("Ingrese una opción: "))

            if opcion == 1:
                agregar_historial_clinico()

            elif opcion == 2:
                listar_historial_clinico()

            elif opcion == 3:
                os.system("cls")
                break

            elif opcion == 4:
                print("Cerrando el programa...")
                exit()

        except ValueError:
            print("No se ingresó un número válido.")
            continue
