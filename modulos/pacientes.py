from utils.constantes import PACIENTES_PATH
from utils.utilidades import (
    validar_archivo,
    escribir_json,
    leer_json,
    buscar_paciente_dni,
    generar_id,
)
import os


def registrar_paciente():
    nombre = input("Ingrese su nombre: ")
    apellido = input("Ingrese su apellido: ")
    dni = input("Ingrese su DNI: ")
    fecha_nacimiento = input("Ingrese su fecha de nacimiento (DD/MM/AAAA): ")
    nacionalidad = input("Ingrese su nacionalidad: ")

    # Obtener los datos existentes del archivo
    datos_existentes = leer_json(PACIENTES_PATH)

    # Verificar si ya existe el paciente
    for elemento in datos_existentes:
        if elemento["dni"] == dni:
            print("El paciente ya existe.")
            return

    # Generar un ID
    nuevo_id = generar_id(datos_existentes)

    # Crear estructura de datos
    paciente = {
        "id": nuevo_id,
        "nombre": nombre,
        "apellido": apellido,
        "dni": dni,
        "fecha_nacimiento": fecha_nacimiento,
        "nacionalidad": nacionalidad,
    }

    # Agregamos al nuevo paciente
    datos_existentes.append(paciente)

    # Sobre-escribir el archivo json con los datos actualizados
    escribir_json(PACIENTES_PATH, datos_existentes)


def editar_paciente():
    # Solicitar DNI al usuario
    dni = input("Ingresar DNI: ")

    # Obtener los datos existentes del archivo
    datos_existentes = leer_json(PACIENTES_PATH)

    # Retorna un string si no se encontro, o una tupla si se encontro (paciente, indice).
    resultado_busqueda = buscar_paciente_dni(dni, datos_existentes)

    # Verificar si no se encontro el paciente
    if isinstance(resultado_busqueda, str):
        print(resultado_busqueda)
        return

    # separamos el paciente y el indice
    paciente_encontrado, indice = resultado_busqueda

    os.system("cls")
    print("Paciente encontrado...")
    for clave, valor in paciente_encontrado.items():
        print(f"{clave} - {valor}")

    print("A continuación modifique los campos que crea necesario.")
    print("Si no desea modificar, No ingrese nada.\n")

    # Solicitar los nuevos valores
    nombre_edit = input("Ingrese su nombre: ")
    apellido_edit = input("Ingrese su apellido: ")
    dni_edit = input("Ingrese su DNI: ")
    fecha_edit = input("Ingrese su fecha de nacimiento (DD/MM/AAAA): ")
    nacionalidad_edit = input("Ingrese su nacionalidad: ")

    # Crear el diccionario para el paciente modificado
    paciente_edit = {
        "id": paciente_encontrado["id"],
        "nombre": nombre_edit if nombre_edit else paciente_encontrado["nombre"],
        "apellido": apellido_edit if apellido_edit else paciente_encontrado["apellido"],
        "dni": dni_edit if dni_edit else paciente_encontrado["dni"],
        "fecha_nacimiento": (
            fecha_edit if fecha_edit else paciente_encontrado["fecha_nacimiento"]
        ),
        "nacionalidad": (
            nacionalidad_edit
            if nacionalidad_edit
            else paciente_encontrado["nacionalidad"]
        ),
    }

    # Mostrar el paciente modificado
    print("\nPaciente modificado...")
    for clave, valor in paciente_edit.items():
        print(f"{clave}: {valor}")

    while True:
        opcion = input("Desea elminar al paciente (s/n)? ").lower()

        if opcion == "n":
            print("No se realizo ninguna accion.")
            break
        elif opcion == "s":
            # Modificar el archivo con los datos actualizados
            datos_existentes[indice] = paciente_edit
            escribir_json(PACIENTES_PATH, datos_existentes)
            print("Paciente actualizado correctamente.")
            return

        else:
            print("Opcion no valida. Por favor ingrese una opcion correcta.")
            continue


def eliminar_paciente():
    # Solicitar DNI al usuario
    dni = input("Ingresar DNI: ")

    # Obtener los datos existentes del archivo
    datos_existentes = leer_json(PACIENTES_PATH)

    # Retorna un string si no se encontro, o una tupla si se encontro (paciente, indice).
    resultado_busqueda = buscar_paciente_dni(dni, datos_existentes)

    # Verificar si no se encontro el paciente
    if isinstance(resultado_busqueda, str):
        return resultado_busqueda

    # separamos el paciente y el indice
    paciente_encontrado, indice = resultado_busqueda

    os.system("cls")
    print("Paciente encontrado...")
    for clave, valor in paciente_encontrado.items():
        print(f"{clave} - {valor}")

    while True:
        opcion = input("Desea elminar al paciente (s/n)? ").lower()

        if opcion == "n":
            print("No se realizo ninguna accion.")
            break
        elif opcion == "s":
            # remover el paciente de los datos existentes
            datos_existentes.pop(indice)

            # sobre escribir el archivo json
            escribir_json(PACIENTES_PATH, datos_existentes)

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

    print("\nLista de pacientes...")

    for paciente in datos_existentes:
        print(
            f"Nombre y Apellido: {paciente["nombre"]} {paciente["apellido"]} | DNI: {paciente["dni"]} | Nacionalidad: {paciente["nacionalidad"]}"
        )
    print()


def menu_pacientes():
    # Verificar si el archivo existe, si no, crearlo
    validar_archivo(PACIENTES_PATH)

    while True:
        print("Eliga una opcion:")
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
                os.system("cls")
                break

            elif opcion == 6:
                print("Cerrando el programa...")
                exit()

        except ValueError:
            print("No se ingresó un número válido.")
            continue
