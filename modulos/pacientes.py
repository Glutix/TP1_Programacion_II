from utils.constantes import PACIENTES_PATH
from utils.utilidades import validar_archivo, escribir_json, leer_json
import os


def registrar_paciente():
    nombre = input("Ingrese su nombre: ")
    apellido = input("Ingrese su apellido: ")
    dni = input("Ingrese su DNI: ")
    fecha_nacimiento = input("Ingrese su fecha de nacimiento (DD/MM/AAAA): ")
    nacionalidad = input("Ingrese su nacionalidad: ")

    paciente = {
        "nombre": nombre,
        "apellido": apellido,
        "dni": dni,
        "fecha_nacimiento": fecha_nacimiento,
        "nacionalidad": nacionalidad,
    }

    # Obtener los datos existentes del archivo
    datos_existentes = leer_json(PACIENTES_PATH)

    # Verificar si ya existe el paciente
    for elemento in datos_existentes:
        if elemento["dni"] == paciente["dni"]:
            print("El paciente ya existe.")
            return

    # Si no existe lo agregamos a los datos existentes
    datos_existentes.append(paciente)

    # Sobre-escribir el archivo json con los datos actualizados
    escribir_json(datos_existentes)


def editar_paciente(dni):
    # Obtener los datos existentes del archivo
    datos_existentes = leer_json(PACIENTES_PATH)

    # Verificar si ya existe el paciente
    paciente_encontrado = None
    indice = 0
    for i, elemento in enumerate(datos_existentes):
        if elemento["dni"] == dni:
            paciente_encontrado = elemento
            indice = i
            break

    if paciente_encontrado is None:
        print(f"No se encontro el paciente con DNI: {dni}")

    os.system("cls")
    print("Paciente encontrado...")
    for clave, valor in paciente_encontrado.items():
        print(f"{clave} - {valor}")

    print("A continuación modifique los campos que crea necesario.")
    print("Si no desea modificar, simplemente apriete enter.")

    # Solicitar los nuevos valores
    nombre_edit = input("Ingrese su nombre: ")
    apellido_edit = input("Ingrese su apellido: ")
    dni_edit = input("Ingrese su DNI: ")
    fecha_edit = input("Ingrese su fecha de nacimiento (DD/MM/AAAA): ")
    nacionalidad_edit = input("Ingrese su nacionalidad: ")

    # Crear el diccionario para el paciente editado
    paciente_edit = {
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

    # Mostrar el paciente editado
    print("\nPaciente editado:")
    for clave, valor in paciente_edit.items():
        print(f"{clave}: {valor}")

    # Confirmar si desea guardar los cambios
    confirmacion = input("\n¿Desea guardar los cambios? (s/n): ").lower()
    if confirmacion != "s":
        print("Los cambios no fueron guardados.")
        return

    # Modificar el archivo con los datos actualizados
    datos_existentes[indice] = paciente_edit
    escribir_json(PACIENTES_PATH, datos_existentes)
    print("Paciente actualizado correctamente.")


def menu_pacientes():
    # Verificar si el archivo existe, si no, crearlo
    validar_archivo(PACIENTES_PATH)

    while True:
        print("Eliga una opcion:")
        print("1. Registrar un paciente.")
        print("2. Modificar un paciente.")
        print("3. Eliminar un paciente.")
        print("4. Buscar un paciente.")
        print("5. Volver al menu anterior.")
        print("6. Salir del programa (directamente).")

        try:
            opcion = int(input("Ingrese una opción: "))

            if opcion == 1:
                registrar_paciente()

            elif opcion == 2:
                dni = input("Ingresar DNI: ")
                editar_paciente(dni)

            elif opcion == 3:
                pass

            elif opcion == 4:
                pass

            elif opcion == 5:
                break

            elif opcion == 6:
                print("Cerrando el programa...")
                exit()

        except ValueError:
            print("No se ingresó un número válido.")
            continue
