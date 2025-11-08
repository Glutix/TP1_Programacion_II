from utils.constantes import (
    HISTORIAS_PATH,
    PACIENTES_PATH,
    MEDICOS_PATH,
    HISTORIAS_CAMPOS,
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
    obtener_por_id,
    eliminar_registro,
)


def agregar_historial_clinico():
    """Agrega una nueva historia clínica a un paciente."""
    # Solicitamos dni del paciente
    dni_paciente = input("Ingresar DNI del paciente: ").strip()

    # Cargamos los pacientes
    datos_pacientes = leer_json(PACIENTES_PATH)

    # Verificar si existe el registro
    if not existe_dni(datos_pacientes, dni_paciente):
        limpiar_consola()
        print(f"El paciente con DNI '{dni_paciente}' no está registrado...\n")
        return

    # Recuperamos el paciente (FIX: faltaba pasar datos_pacientes)
    paciente_encontrado = obtener_por_dni(datos_pacientes, dni_paciente)
    id_paciente = paciente_encontrado["id"]

    limpiar_consola()
    print("Paciente encontrado...\n")
    for clave, valor in paciente_encontrado.items():
        print(f"{clave}: {valor}")

    # Solicitamos matrícula del médico
    print()
    matricula_medico = input("Ingrese la matrícula del médico que lo trató: ").strip()

    # Obtener los datos existentes del archivo (médicos)
    datos_medicos = leer_json(MEDICOS_PATH)

    # Verificar si existe el registro
    if not existe_matricula(datos_medicos, matricula_medico):
        limpiar_consola()
        print(f"El médico con matrícula '{matricula_medico}' no está registrado...\n")
        return

    # Recuperamos el médico
    medico_encontrado = obtener_por_matricula(datos_medicos, matricula_medico)
    id_medico = medico_encontrado["id"]

    limpiar_consola()
    print("Médico encontrado...\n")
    print(f"Nombre: {medico_encontrado['nombre']} {medico_encontrado['apellido']}")
    print(f"Especialidad: {medico_encontrado['especialidad']}\n")

    # Datos de la historia clínica
    enfermedad_afeccion = input("Ingresar enfermedad o afección que padece: ").strip()
    observaciones = input("Ingresar observaciones: ").strip()
    fecha = input(
        "Ingresar fecha (DD/MM/YYYY), presione Enter para usar fecha actual: "
    ).strip()

    # Recuperamos las historias existentes
    datos_historias = leer_json(HISTORIAS_PATH)

    # Creamos la estructura de datos para la nueva historia clínica
    nueva_historia = {
        "id_medico": id_medico,
        "id_paciente": id_paciente,
        "enfermedad_afeccion": enfermedad_afeccion,
        "observaciones": observaciones,
        "fecha": fecha if fecha else fecha_actual(),
    }

    # Creamos el nuevo registro
    datos_actualizados = crear_registro(
        datos_historias, nueva_historia, HISTORIAS_CAMPOS
    )

    # Actualizamos la información en el archivo
    escribir_json(HISTORIAS_PATH, datos_actualizados)
    limpiar_consola()
    print("Historia clínica agregada correctamente.\n")


def listar_historial_clinico():
    """Lista todos los historiales clínicos registrados."""
    datos_existentes = leer_json(HISTORIAS_PATH)
    datos_pacientes = leer_json(PACIENTES_PATH)
    datos_medicos = leer_json(MEDICOS_PATH)

    if not datos_existentes:
        limpiar_consola()
        print("No hay historiales clínicos registrados.\n")
        return

    limpiar_consola()
    print("\n=== LISTA DE HISTORIALES CLÍNICOS ===\n")

    for historia in datos_existentes:
        paciente = obtener_por_id(datos_pacientes, historia["id_paciente"])
        medico = obtener_por_id(datos_medicos, historia["id_medico"])

        # Verificar que el paciente y médico existan
        if not paciente or not medico:
            print(f"[ERROR] Historia ID {historia['id']}: Datos incompletos\n")
            continue

        print(f"ID Historia: {historia['id']}")
        print(f"Fecha: {historia['fecha']}")
        print(
            f"Paciente: {paciente['nombre']} {paciente['apellido']} (DNI: {paciente['dni']})"
        )
        print(
            f"Médico: {medico['nombre']} {medico['apellido']} (Matrícula: {medico['matricula']})"
        )
        print(f"Especialidad: {medico['especialidad']}")
        print(f"Enfermedad/Afección: {historia['enfermedad_afeccion']}")
        print(f"Observaciones: {historia['observaciones']}")
        print("-" * 60)
        print()


def buscar_historial_por_paciente():
    """Busca y muestra el historial clínico de un paciente específico."""
    dni_paciente = input("Ingresar DNI del paciente: ").strip()

    # Cargamos los datos
    datos_pacientes = leer_json(PACIENTES_PATH)
    datos_historias = leer_json(HISTORIAS_PATH)
    datos_medicos = leer_json(MEDICOS_PATH)

    # Verificar si existe el paciente
    if not existe_dni(datos_pacientes, dni_paciente):
        limpiar_consola()
        print(f"El paciente con DNI '{dni_paciente}' no está registrado...\n")
        return

    paciente = obtener_por_dni(datos_pacientes, dni_paciente)

    # Filtrar historiales del paciente
    historiales_paciente = [
        h for h in datos_historias if h["id_paciente"] == paciente["id"]
    ]

    if not historiales_paciente:
        limpiar_consola()
        print(
            f"El paciente {paciente['nombre']} {paciente['apellido']} no tiene historiales clínicos registrados.\n"
        )
        return

    limpiar_consola()
    print(
        f"\n=== HISTORIAL CLÍNICO DE {paciente['nombre'].upper()} {paciente['apellido'].upper()} ==="
    )
    print(f"DNI: {paciente['dni']}")
    print(f"Total de consultas: {len(historiales_paciente)}\n")

    for historia in historiales_paciente:
        medico = obtener_por_id(datos_medicos, historia["id_medico"])

        if not medico:
            continue

        print(f"ID: {historia['id']} | Fecha: {historia['fecha']}")
        print(
            f"Médico: Dr/a. {medico['nombre']} {medico['apellido']} ({medico['especialidad']})"
        )
        print(f"Diagnóstico: {historia['enfermedad_afeccion']}")
        print(f"Observaciones: {historia['observaciones']}")
        print("-" * 60)
        print()


def eliminar_historial_clinico():
    """Elimina una historia clínica específica."""
    # Listar historiales primero
    datos_existentes = leer_json(HISTORIAS_PATH)
    datos_pacientes = leer_json(PACIENTES_PATH)
    datos_medicos = leer_json(MEDICOS_PATH)

    if not datos_existentes:
        limpiar_consola()
        print("No hay historiales clínicos registrados para eliminar.\n")
        return

    limpiar_consola()
    print("\n=== HISTORIALES CLÍNICOS DISPONIBLES ===\n")

    for historia in datos_existentes:
        paciente = obtener_por_id(datos_pacientes, historia["id_paciente"])
        medico = obtener_por_id(datos_medicos, historia["id_medico"])

        if not paciente or not medico:
            continue

        print(f"ID: {historia['id']} | Fecha: {historia['fecha']}")
        print(
            f"Paciente: {paciente['nombre']} {paciente['apellido']} (DNI: {paciente['dni']})"
        )
        print(f"Médico: {medico['nombre']} {medico['apellido']}")
        print(f"Diagnóstico: {historia['enfermedad_afeccion']}")
        print("-" * 40)

    # Solicitar ID del historial a eliminar
    try:
        id_historia = int(
            input("\nIngrese el ID del historial a eliminar (0 para cancelar): ")
        )

        if id_historia == 0:
            limpiar_consola()
            print("Operación cancelada.\n")
            return

        # Buscar el historial
        historia_encontrada = obtener_por_id(datos_existentes, id_historia)

        if not historia_encontrada:
            limpiar_consola()
            print(f"No se encontró ningún historial con ID: {id_historia}\n")
            return

        # Mostrar detalles y confirmar
        paciente = obtener_por_id(datos_pacientes, historia_encontrada["id_paciente"])
        medico = obtener_por_id(datos_medicos, historia_encontrada["id_medico"])

        limpiar_consola()
        print("Historial encontrado:\n")
        print(f"Fecha: {historia_encontrada['fecha']}")
        print(f"Paciente: {paciente['nombre']} {paciente['apellido']}")
        print(f"Médico: {medico['nombre']} {medico['apellido']}")
        print(f"Diagnóstico: {historia_encontrada['enfermedad_afeccion']}")

        confirmacion = input(
            "\n¿Está seguro que desea eliminar este historial? (s/n): "
        ).lower()

        if confirmacion == "s":
            datos_actualizados = eliminar_registro(
                datos_existentes, historia_encontrada
            )
            escribir_json(HISTORIAS_PATH, datos_actualizados)
            limpiar_consola()
            print("Historial clínico eliminado correctamente.\n")
        else:
            limpiar_consola()
            print("Operación cancelada por el usuario.\n")

    except ValueError:
        limpiar_consola()
        print("Error: Debe ingresar un número válido.\n")


def menu_historial_clinico():
    """Menú principal del módulo de historias clínicas."""
    while True:
        print("=== GESTIÓN DE HISTORIALES CLÍNICOS ===")
        print("1. Agregar una historia clínica a un paciente")
        print("2. Listar todos los historiales clínicos")
        print("3. Buscar historial de un paciente específico")
        print("4. Eliminar un historial clínico")
        print("5. Volver al menú anterior")
        print("6. Salir del programa\n")

        try:
            opcion = int(input("Ingrese una opción: "))

            if opcion == 1:
                limpiar_consola()
                agregar_historial_clinico()

            elif opcion == 2:
                listar_historial_clinico()

            elif opcion == 3:
                limpiar_consola()
                buscar_historial_por_paciente()

            elif opcion == 4:
                eliminar_historial_clinico()

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
            print("Error: No se ingresó un número válido.\n")
            continue
