from utils.constantes import (
    HISTORIAS_PATH,
    PACIENTES_PATH,
    MEDICOS_PATH,
    MEDICOS_CAMPOS,
)
from utils.utilidades import (
    existe_dni,
    obtener_por_dni,
    leer_json,
    limpiar_consola,
    obtener_por_matricula,
    existe_matricula,
    fecha_actual,
    crear_registro,
    escribir_json,
    solicitar_datos,
)


def agregar_historial_clinico():
    # Solicitamos dni del paciente
    dni_paciente = input("Ingresar DNI del paciente: ")

    # Cargamos los pacientes
    datos_pacientes = leer_json(PACIENTES_PATH)

    # Verificar si existe el registro
    if not existe_dni(datos_pacientes, dni_paciente):
        limpiar_consola()
        print(f"El paciente con dni '{dni_paciente}' no esta registado...\n")
        return

    # Recuperamos el id del paciente
    paciente_encontrado = obtener_por_dni(dni_paciente)
    id_paciente = paciente_encontrado["id"]

    limpiar_consola()
    print("Paciente encontrado...\n")
    for clave, valor in paciente_encontrado.items():
        print(f"{clave} - {valor}")

    # Solicitamos matricula del medico
    matricula_medico = input("Ingrese la matricula del medico que lo trato: ")

    # Obtener los datos existentes del archivo (medicos)
    datos_medicos = leer_json(MEDICOS_PATH)

    # Verificar si existe el registro
    if not existe_matricula(datos_medicos, matricula_medico):
        limpiar_consola()
        print(f"El paciente con matricula '{matricula_medico}' no esta registado...\n")
        return

    # recuperamos el id del medico
    medico_encontrado = obtener_por_matricula(datos_medicos, matricula_medico)
    id_medico = medico_encontrado["id"]

    # Datos de la historia clinica
    enfermedad_aficcion = input("Ingresar enfermedad o aficcion que padece: ")
    observaciones = input("ingresar obersvaciones: ")
    fecha = input("Ingresar fecha en que fue atendido, si es hoy ignorar este campo:")

    # Recuperamos las historias existentes
    datos_historias = leer_json(HISTORIAS_PATH)

    # Creamos la estructura de datos para la nueva historia clinica
    nueva_historia = {
        "id_medico": id_medico,
        "id_paciente": id_paciente,
        "enfermedad_aficcion": enfermedad_aficcion,
        "observaciones": observaciones,
        "fecha": fecha if fecha else fecha_actual(),
    }

    # Creamos el nuevo registro
    datos_actualizados = crear_registro(datos_historias, nueva_historia, MEDICOS_CAMPOS)

    # Actualizamos la informacion en el archivo
    escribir_json(HISTORIAS_PATH, datos_actualizados)
    limpiar_consola()
    print("Historia clinica agregada correctamente\n")


def listar_historial_clinico():
    datos_existentes = leer_json(HISTORIAS_PATH)

    if not datos_existentes:
        print("No hay historiales clinicos registrados.")
        return

    limpiar_consola()
    print("\nLista de historiales clinico...")
    for elemento in datos_existentes:
        print(elemento)
    print()


def menu_historial_clinico():
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
                limpiar_consola()
                break

            elif opcion == 4:
                print("Cerrando el programa...")
                exit()
            else:
                print("Opcion incorrecta, ingrese número entre 1 y 4.")
                continue

        except ValueError:
            print("Opcion incorrecta, ingrese número entre 1 y 4.")
            continue
