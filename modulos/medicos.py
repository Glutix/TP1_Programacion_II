from utils.constantes import MEDICOS_PATH, MEDICOS_CAMPOS
from utils.utilidades import (
    escribir_json,
    leer_json,
    solicitar_datos,
    actualizar_registro,
    crear_registro,
    obtener_por_matricula,
    existe_matricula,
    eliminar_registro,
    limpiar_consola,
)


def registrar_medico():
    """Registra un nuevo médico en el sistema."""
    # Obtener los datos existentes del archivo
    datos_existentes = leer_json(MEDICOS_PATH)
    datos_formulario = solicitar_datos(MEDICOS_CAMPOS)

    # Verificamos si la matrícula no está registrada
    if existe_matricula(datos_existentes, datos_formulario["matricula"]):
        limpiar_consola()
        print(
            f"El médico con matrícula '{datos_formulario['matricula']}' ya está registrado...\n"
        )
        return

    # Creamos el nuevo registro
    datos_actualizados = crear_registro(
        datos_existentes, datos_formulario, MEDICOS_CAMPOS
    )

    # Sobre-escribir el archivo json con los datos actualizados
    escribir_json(MEDICOS_PATH, datos_actualizados)
    limpiar_consola()
    print("Médico registrado correctamente.\n")


def editar_medico():
    """Edita los datos de un médico existente."""
    # Solicitar matrícula al usuario
    matricula = input("Ingresar matrícula: ")

    # Obtener los datos existentes del archivo
    datos_existentes = leer_json(MEDICOS_PATH)

    # Verificar si existe el registro
    if not existe_matricula(datos_existentes, matricula):
        limpiar_consola()
        print(f"El médico con matrícula '{matricula}' no está registrado...\n")
        return

    # Recuperar el médico
    medico = obtener_por_matricula(datos_existentes, matricula)

    limpiar_consola()
    print("Médico encontrado...\n")
    for clave, valor in medico.items():
        print(f"{clave} - {valor}")

    print("\nA continuación modifique los campos que crea necesario.")
    print("Si no desea modificar, No ingrese nada.\n")

    # Solicitar los nuevos valores
    medico_editado = solicitar_datos(MEDICOS_CAMPOS)

    # Crear un diccionario para el registro modificado
    medico_modificado = actualizar_registro(medico, medico_editado)

    # Mostrar la modificación del registro
    limpiar_consola()
    print("Médico modificado...\n")
    for clave, valor in medico_modificado.items():
        print(f"{clave}: {valor}")

    while True:
        opcion = input("\n¿Desea modificar al médico (s/n)? ").lower()

        if opcion == "n":
            limpiar_consola()
            print("Operación cancelada por el usuario.\n")
            break
        elif opcion == "s":
            # Modificar el archivo con los datos actualizados
            indice = datos_existentes.index(medico)
            datos_existentes[indice] = medico_modificado
            escribir_json(MEDICOS_PATH, datos_existentes)
            limpiar_consola()
            print("Médico actualizado correctamente.\n")
            return
        else:
            print("Opción no válida. Por favor ingrese una opción correcta.")
            continue


def eliminar_medico():
    """Elimina un médico del sistema."""
    # Solicitar matrícula al usuario
    matricula = input("Ingresar matrícula: ")

    # Obtener los datos existentes del archivo
    datos_existentes = leer_json(MEDICOS_PATH)

    # Verificar si existe el registro
    if not existe_matricula(datos_existentes, matricula):
        limpiar_consola()
        print(f"El médico con matrícula '{matricula}' no está registrado...\n")
        return

    # Si existe traemos el registro
    medico = obtener_por_matricula(datos_existentes, matricula)

    limpiar_consola()
    print("Médico encontrado.\n")
    for clave, valor in medico.items():
        print(f"{clave} - {valor}")

    while True:
        opcion = input("\n¿Desea eliminar al médico (s/n)? ").lower()

        if opcion == "n":
            limpiar_consola()
            print("Operación cancelada por el usuario.\n")
            break
        elif opcion == "s":
            # Remover el médico de los datos existentes
            datos_actualizados = eliminar_registro(datos_existentes, medico)

            # Sobre escribir el archivo json
            escribir_json(MEDICOS_PATH, datos_actualizados)
            limpiar_consola()
            print("Se guardaron los cambios correctamente.\n")
            return
        else:
            print("Opción no válida. Por favor ingrese una opción correcta.")
            continue


def listar_medicos():
    """Lista todos los médicos registrados."""
    datos_existentes = leer_json(MEDICOS_PATH)

    if not datos_existentes:
        limpiar_consola()
        print("No hay médicos registrados.\n")
        return

    limpiar_consola()
    print("\nLista de médicos...\n")

    for medico in datos_existentes:
        # FIX: Usar comillas simples dentro del f-string
        print(
            f"Nombre y Apellido: {medico['nombre']} {medico['apellido']} | "
            f"Matrícula: {medico['matricula']} | "
            f"Especialidad: {medico['especialidad']}"
        )
    print()


def menu_medicos():
    """Menú principal del módulo de médicos."""
    while True:
        print("Seleccione una opción:")
        print("1. Registrar un médico.")
        print("2. Modificar un médico.")
        print("3. Eliminar un médico.")
        print("4. Listar médicos.")
        print("5. Volver al menú anterior.")
        print("6. Salir del programa (directamente).")

        try:
            opcion = int(input("Ingrese una opción: "))

            if opcion == 1:
                limpiar_consola()
                registrar_medico()

            elif opcion == 2:
                limpiar_consola()
                editar_medico()

            elif opcion == 3:
                limpiar_consola()
                eliminar_medico()

            elif opcion == 4:
                listar_medicos()

            elif opcion == 5:
                limpiar_consola()
                break

            elif opcion == 6:
                print("Cerrando el programa...")
                exit()

            else:
                limpiar_consola()
                print(
                    "Opción no válida. Por favor, seleccione una opción entre 1 y 6.\n"
                )

        except ValueError:
            limpiar_consola()
            print("No se ingresó un número válido.\n")
            continue
        except Exception as e:
            limpiar_consola()
            print(f"Error inesperado: {e}\n")
            continue
