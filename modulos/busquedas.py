from utils.constantes import PACIENTES_PATH, HISTORIAS_PATH, MEDICOS_PATH
from utils.utilidades import (
    leer_json,
    calcular_edad,
    fecha_actual,
    limpiar_consola,
    existe_dni,
    obtener_por_dni,
    obtener_por_id,
)
from datetime import datetime


def buscar_apellido_nombre():
    datos_pacientes = leer_json(PACIENTES_PATH)

    if not datos_pacientes:
        limpiar_consola()
        print("No hay pacientes registrados.\n")
        return

    nombre = input("Ingrese el nombre del paciente (opcional): ").strip().lower()
    apellido = input("Ingrese el apellido del paciente (opcional): ").strip().lower()

    if not nombre and not apellido:
        limpiar_consola()
        print("Debe ingresar al menos un nombre o un apellido.\n")
        return

    def coincide(paciente):
        nombre_paciente = paciente["nombre"].strip().lower()
        apellido_paciente = paciente["apellido"].strip().lower()

        return (nombre and nombre in nombre_paciente) or (
            apellido and apellido in apellido_paciente
        )

    pacientes_filtrados = list(filter(coincide, datos_pacientes))

    if not pacientes_filtrados:
        limpiar_consola()
        print("No se encontraron pacientes con esos datos...\n")
        return

    limpiar_consola()
    print("Pacientes encontrados:\n")
    for paciente in pacientes_filtrados:
        edad = calcular_edad(paciente["fecha_nacimiento"])
        print(
            f"""
ID: {paciente['id']}
Nombre: {paciente['nombre']} {paciente['apellido']}
DNI: {paciente['dni']}
Fecha Nacimiento: {paciente['fecha_nacimiento']}
Edad: {edad} años
Nacionalidad: {paciente['nacionalidad']}
-------------------------------------\n"""
        )


def buscar_rango_fecha():
    # Revisar si hay pacientes cargados
    datos_pacientes = leer_json(PACIENTES_PATH)

    if not datos_pacientes:
        limpiar_consola()
        print("No hay pacientes registrados.\n")
        return

    # Solicitar un dato indificativo del cliente
    dni_paciente = input("Ingresar DNI: ").strip()

    if not existe_dni(datos_pacientes, dni_paciente):
        limpiar_consola()
        print(f"No se encontro a ningun paciente con dni '{dni_paciente}'\n")
        return

    # recuperar paciente
    paciente = obtener_por_dni(datos_pacientes, dni_paciente)

    # recuperar id del paciente
    id_paciente = paciente["id"]

    # recuperar datos de las historias clinicas
    datos_historias = leer_json(HISTORIAS_PATH)

    # Primer filtro: solo historias del paciente
    historias_paciente = list(
        filter(lambda e: e["id_paciente"] == id_paciente, datos_historias)
    )

    if not historias_paciente:
        limpiar_consola()
        print("El paciente no tiene ninguna historia clinica.\n")
        return

    # Solicitar rango de fecha
    fecha_inicio_str = input("Ingrese fecha de inicio (DD/MM/AAAA): ").strip()
    fecha_final_str = input(
        "Ingrese fecha final (DD/MM/AAAA) no ingresar nada si quiere usar le fecha actual: "
    ).strip()

    if not fecha_final_str:
        fecha_final_str = fecha_actual()

    try:
        fecha_inicio = datetime.strptime(fecha_inicio_str, "%d/%m/%Y")
        fecha_final = datetime.strptime(fecha_final_str, "%d/%m/%Y")

        if fecha_final < fecha_inicio:
            limpiar_consola()
            print("La fecha final no puede ser anterior a la fecha de inicio.")
            return

    except ValueError:
        limpiar_consola()
        print("Formato de fecha inválido. Use DD/MM/AAAA.")
        return

    # Segundo filtro: historias dentro del rango de fechas
    historias_en_rango = list(
        filter(
            lambda h: fecha_inicio
            <= datetime.strptime(h["fecha"], "%d/%m/%Y")
            <= fecha_final,
            historias_paciente,
        )
    )

    if not historias_en_rango:
        limpiar_consola()
        print("No se encontro ninguna historia clinica dentro del rango.\n")
        return

    # Mostrar información del paciente
    edad = calcular_edad(paciente["fecha_nacimiento"])
    limpiar_consola()
    print("\n====== Información del Paciente ======")
    print(f"ID:               {paciente['id']}")
    print(f"Nombre:           {paciente['nombre']} {paciente['apellido']}")
    print(f"DNI:              {paciente['dni']}")
    print(f"Fecha Nacimiento: {paciente['fecha_nacimiento']}")
    print(f"Edad:             {edad} años")
    print(f"Nacionalidad:     {paciente['nacionalidad']}")
    print("======================================\n")

    print("=== Historias Clínicas en el Rango ===")
    for indice, h in enumerate(historias_en_rango, 1):
        print(f"{indice}. Fecha: {h['fecha']}")
        print(f"   Afección: {h['enfermedad_afeccion']}")
        print(f"   Observaciones: {h['observaciones']}\n")


def buscar_nacionalidad():
    # Revisar si hay pacientes cargados
    pacientes = leer_json(PACIENTES_PATH)

    if not pacientes:
        print("No hay pacientes registrados.")
        return

    # Solicitar datos del paciente a buscar
    nacionalidad = input("Ingresa la nacionalidad del paciente: ").strip().lower()

    pacientes_filtrados = [
        p for p in pacientes if p["nacionalidad"].lower() == nacionalidad
    ]

    if not pacientes_filtrados:
        limpiar_consola()
        print("No se encontro el paciente.\n")
        return

    limpiar_consola()
    for paciente in pacientes_filtrados:
        edad = calcular_edad(paciente["fecha_nacimiento"])
        print(
            f"""
ID: {paciente['id']}
Nombre: {paciente['nombre']} {paciente['apellido']}
DNI: {paciente['dni']}
Fecha Nacimiento: {paciente['fecha_nacimiento']}
Edad: {edad} años
Nacionalidad: {paciente['nacionalidad']}
-------------------------"""
        )


def buscar_enfermedad_afeccion():
    # Revisar si hay pacientes cargados
    datos_pacientes = leer_json(PACIENTES_PATH)

    if not datos_pacientes:
        limpiar_consola()
        print("No hay pacientes registrados.\n")
        return

    # Solicitar un dato indificativo del cliente
    dni_paciente = input("Ingresar DNI: ").strip()

    if not existe_dni(datos_pacientes, dni_paciente):
        limpiar_consola()
        print(f"No se encontro a ningun paciente con dni '{dni_paciente}'\n")
        return

    # recuperar paciente
    paciente = obtener_por_dni(datos_pacientes, dni_paciente)

    # recuperar id del paciente
    id_paciente = paciente["id"]

    # recuperar datos de las historias clinicas
    datos_historias = leer_json(HISTORIAS_PATH)

    # Primer filtro: solo historias del paciente
    historias_paciente = list(
        filter(lambda e: e["id_paciente"] == id_paciente, datos_historias)
    )

    if not historias_paciente:
        limpiar_consola()
        print("El paciente no tiene ninguna historia clinica.\n")
        return

    # Solicitar rango de fecha
    enfermedad_afeccion = input("Ingrese enfermedad/afección: ").strip().lower()

    if not enfermedad_afeccion:
        limpiar_consola()
        print("No se ingreso ninguna enfermedad o afeccion.\n")
        return

    # filtro
    historias_enfermedad_afeccion = list(
        filter(
            lambda h: enfermedad_afeccion in h["enfermedad_afeccion"].lower(),
            historias_paciente,
        )
    )

    if not historias_enfermedad_afeccion:
        limpiar_consola()
        print(
            "No se encontro ninguna historia clinica con los criterios establecidos.\n"
        )
        return

    # Mostrar información del paciente
    edad = calcular_edad(paciente["fecha_nacimiento"])
    limpiar_consola()
    print("\n====== Información del Paciente ======")
    print(f"ID:               {paciente['id']}")
    print(f"Nombre:           {paciente['nombre']} {paciente['apellido']}")
    print(f"DNI:              {paciente['dni']}")
    print(f"Fecha Nacimiento: {paciente['fecha_nacimiento']}")
    print(f"Edad:             {edad} años")
    print(f"Nacionalidad:     {paciente['nacionalidad']}")
    print("======================================\n")

    print("=== Historias Clínicas segun su enfermedad/afeccion ===")
    for indice, h in enumerate(historias_enfermedad_afeccion, 1):
        print(f"{indice}. Fecha: {h['fecha']}")
        print(f"   Afección: {h['enfermedad_afeccion']}")
        print(f"   Observaciones: {h['observaciones']}\n")


def buscar_medico_trato():
    datos_pacientes = leer_json(PACIENTES_PATH)
    datos_historias = leer_json(HISTORIAS_PATH)
    datos_medicos = leer_json(MEDICOS_PATH)

    if not datos_pacientes or not datos_historias or not datos_medicos:
        limpiar_consola()
        print(
            "Faltan datos: no hay pacientes, médicos o historias clínicas registradas.\n"
        )
        return

    dni = input("Ingrese el DNI del paciente: ").strip()

    if not existe_dni(datos_pacientes, dni):
        limpiar_consola()
        print(f"No se encontró ningún paciente con DNI '{dni}'.\n")
        return

    paciente = obtener_por_dni(datos_pacientes, dni)
    id_paciente = paciente["id"]

    historias_paciente = list(
        filter(lambda h: h["id_paciente"] == id_paciente, datos_historias)
    )

    if not historias_paciente:
        limpiar_consola()
        print(
            f"No se encontraron historias clínicas para {paciente['nombre']} {paciente['apellido']}.\n"
        )
        return

    limpiar_consola()
    print(
        f"=== Atenciones para {paciente['nombre']} {paciente['apellido']} (DNI {dni}) ===\n"
    )

    for i, h in enumerate(historias_paciente, 1):
        medico = obtener_por_id(datos_medicos, h["id_medico"])
        if medico:
            print(f"{i}. Fecha: {h['fecha']}")
            print(
                f"   Médico: Dr. {medico['nombre']} {medico['apellido']} (Matrícula {medico['matricula']})"
            )
            print(f"   Especialidad: {medico['especialidad']}")
            print(f"   Enfermedad/Afección: {h['enfermedad_afeccion']}")
            print(f"   Observaciones: {h['observaciones']}\n")


def menu_busquedas():
    while True:
        print("Buscar Pacientes por:")
        print("1. Apellido y/o Nombre.")
        print("2. Rango de fechas en la que fueron atendidos.")
        print("3. Enfermedad/afección.")
        print("4. Por Médico que lo/la trató.")
        print("5. Nacionalidad")
        print("6. Volver al menu anterior.")
        print("7. Salir del programa (directamente).")

        try:
            opcion = int(input("Ingrese una opción: "))

            if opcion == 1:
                buscar_apellido_nombre()

            elif opcion == 2:
                buscar_rango_fecha()

            elif opcion == 3:
                buscar_enfermedad_afeccion()

            elif opcion == 4:
                buscar_medico_trato()

            elif opcion == 5:
                buscar_nacionalidad()

            elif opcion == 6:
                limpiar_consola()
                break

            elif opcion == 7:
                print("Cerrando el programa...")
                exit()

        except ValueError:
            print("No se ingresó un número válido.")
            continue
