from utils.constantes import PACIENTES_PATH, PACIENTES_CAMPOS
from utils.utilidades import (
    escribir_json,
    leer_json,
    solicitar_datos,
    actualizar_registro,
    crear_registro,
    obtener_por_dni,
    existe_dni,
    eliminar_registro,
    limpiar_consola,
)
import os


def registrar_paciente():
    # Obtener los datos existentes del archivo
    datos_existentes = leer_json(PACIENTES_PATH)
    datos_formulario = solicitar_datos(PACIENTES_CAMPOS)

    # Verificamos si el dni no esta registrado
    if existe_dni(datos_existentes, datos_formulario["dni"]):
        limpiar_consola()
        print(f"El paciente con {datos_formulario['dni']} ya esta registrado...")
        return

    # Creamos el nuevo registro
    datos_actualizados = crear_registro(
        datos_existentes, datos_formulario, PACIENTES_CAMPOS
    )

    # Sobre-escribir el archivo json con los datos actualizados
    escribir_json(PACIENTES_PATH, datos_actualizados)
    limpiar_consola()
    print("Paciente registrado correctamente.\n")


def editar_paciente():
    # Solicitar DNI al usuario
    dni = input("Ingresar DNI: ")

    # Obtener los datos existentes del archivo
    datos_existentes = leer_json(PACIENTES_PATH)

    # Verificar si existe el registro
    if not existe_dni(datos_existentes, dni):
        limpiar_consola()
        print(f"El paciente con {dni} no esta registado...\n")
        return

    # recuperar el paciente
    paciente = obtener_por_dni(datos_existentes, dni)

    limpiar_consola()
    print("Paciente encontrado...\n")
    for clave, valor in paciente.items():
        print(f"{clave} - {valor}")

    print("\nA continuación modifique los campos que crea necesario.")
    print("Si no desea modificar, No ingrese nada.\n")

    # Solicitar los nuevos valores
    paciente_editado = solicitar_datos(PACIENTES_CAMPOS)

    # Crear un diccionario para el registro modificado
    paciente_modificado = actualizar_registro(paciente, paciente_editado)

    # Mostrar la modificacion del registro
    limpiar_consola()
    print("Paciente modificado...\n")
    for clave, valor in paciente_modificado.items():
        print(f"{clave}: {valor}")

    while True:
        opcion = input("\nDesea modificar al paciente (s/n)? ").lower()

        if opcion == "n":
            limpiar_consola()
            print("Operación cancelada por el usuario.\n")
            break
        elif opcion == "s":
            # Modificar el archivo con los datos actualizados
            indice = datos_existentes.index(paciente)
            datos_existentes[indice] = paciente_modificado
            escribir_json(PACIENTES_PATH, datos_existentes)
            limpiar_consola()
            print("Paciente actualizado correctamente.\n")
            return

        else:
            print("Opcion no valida. Por favor ingrese una opcion correcta.")
            continue


def eliminar_paciente():
    # Solicitar DNI al usuario
    dni = input("Ingresar DNI: ")

    # Obtener los datos existentes del archivo
    datos_existentes = leer_json(PACIENTES_PATH)

    # Verificar si existe el registro
    if not existe_dni(datos_existentes, dni):
        print(f"El paciente con {dni} no esta registado...")
        return

    # Si existe traemos el registro
    paciente = obtener_por_dni(datos_existentes, dni)

    limpiar_consola()
    print("Paciente encontrado.\n")
    for clave, valor in paciente.items():
        print(f"{clave} - {valor}")

    while True:
        opcion = input("\nDesea eliminar al paciente (s/n)? ").lower()

        if opcion == "n":
            limpiar_consola()
            print("Operación cancelada por el usuario.\n")
            break
        elif opcion == "s":
            # remover el paciente de los datos existentes
            datos_actualizados = eliminar_registro(datos_existentes, paciente)

            # sobre escribir el archivo json
            escribir_json(PACIENTES_PATH, datos_actualizados)
            limpiar_consola()
            print("Se guardaron los cambios correctamente.\n")
            return
        else:
            print("Opcion no valida. Por favor ingrese una opcion correcta.")
            continue


def listar_pacientes():
    datos_existentes = leer_json(PACIENTES_PATH)

    if not datos_existentes:
        print("No hay pacientes registrados.")
        return

    limpiar_consola()
    print("\nLista de pacientes...")

    for paciente in datos_existentes:
        print(
            f"Nombre y Apellido: {paciente['nombre']} {paciente['apellido']} | DNI: {paciente['dni']} | Nacionalidad: {paciente['nacionalidad']}"
        )
    print()


def menu_pacientes():
    while True:
        print("Seleccione una opcion:")
        print("1. Registrar un paciente.")
        print("2. Modificar un paciente.")
        print("3. Eliminar un paciente.")
        print("4. Listar pacientes.")
        print("5. Volver al menu anterior.")
        print("6. Salir del programa (directamente).")

        try:
            opcion = int(input("Ingrese una opción: "))

            if opcion == 1:
                registrar_paciente()

            elif opcion == 2:
                editar_paciente()

            elif opcion == 3:
                eliminar_paciente()

            elif opcion == 4:
                listar_pacientes()

            elif opcion == 5:
                limpiar_consola()
                break

            elif opcion == 6:
                print("Cerrando el programa...")
                exit()

        except ValueError:
            print("No se ingresó un número válido.")
            continue
