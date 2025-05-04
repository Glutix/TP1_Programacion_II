from utils.constantes import MEDICOS_PATH, MEDICOS_CAMPOS
from utils.utilidades import (
    leer_json,
    solicitar_datos,
    crear_registro,
    escribir_json,
    limpiar_consola,
)


def registrar_medico():
    # solicitar datos
    datos_formulario = solicitar_datos(MEDICOS_CAMPOS)

    # Obtener los datos existentes del archivo
    datos_existentes = leer_json(MEDICOS_PATH)

    # Verificar si ya existe el médico
    for elemento in datos_existentes:
        if (
            elemento["nombre"].lower() == datos_formulario["nombre"].lower()
            and elemento["apellido"].lower() == datos_formulario["apellido"].lower()
            and elemento["especialidad"].lower()
            == datos_formulario["especialidad"].lower()
        ):
            limpiar_consola()
            print("El médico ya está registrado.\n")
            return

    # Creamos y actualizamos el nuevo registro
    datos_actualizados = crear_registro(
        datos_existentes, datos_formulario, MEDICOS_CAMPOS
    )

    # Sobre-escribir el archivo json con los datos actualizados
    escribir_json(MEDICOS_PATH, datos_actualizados)
    limpiar_consola()
    print("Se agrego el registro correctamente.\n")
    return


def listar_medicos():
    datos_existentes = leer_json(MEDICOS_PATH)

    if not datos_existentes:
        limpiar_consola()
        print("No hay médicos registrados.\n")
        return

    limpiar_consola()
    print("\nLista de mèdicos...")

    for medico in datos_existentes:
        print(
            f"Matricula: {medico["matricula"]} | {medico["nombre"]} {medico["apellido"]} | Especialidad: {medico["especialidad"]}"
        )
    print()


def menu_medicos():
    while True:
        print("Seleccione una opcioon: ")
        print("1. Registrar a un Médico")
        print("2. Listar de Médicos.")
        print("3. Volver al menu anterior.")
        print("4. Salir del programa (directamente).")

        try:
            opcion = int(input("Ingrese una opción: "))

            if opcion == 1:
                registrar_medico()

            elif opcion == 2:
                listar_medicos()

            elif opcion == 3:
                limpiar_consola()
                break

            elif opcion == 4:
                print("Cerrando el programa...")
                exit()

        except ValueError:
            print("No se ingresó un número válido.")
            continue
