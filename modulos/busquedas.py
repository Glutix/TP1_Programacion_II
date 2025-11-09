from utils.constantes import PACIENTES_PATH, HISTORIAS_PATH, MEDICOS_PATH
from utils.utilidades import (
    leer_json,
    calcular_edad,
    fecha_actual,
    limpiar_consola,
    existe_dni,
    obtener_por_dni,
    obtener_por_id,
    existe_matricula,
    obtener_por_matricula,
)
from datetime import datetime


def buscar_apellido_nombre():
    """Busca pacientes por apellido y/o nombre (búsqueda parcial)."""
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
        print("No se encontraron pacientes con esos datos.\n")
        return

    limpiar_consola()
    print(f"\n=== PACIENTES ENCONTRADOS ({len(pacientes_filtrados)}) ===\n")

    for paciente in pacientes_filtrados:
        edad = calcular_edad(paciente["fecha_nacimiento"])
        print(f"ID: {paciente['id']}")
        print(f"Nombre: {paciente['nombre']} {paciente['apellido']}")
        print(f"DNI: {paciente['dni']}")
        print(f"Fecha Nacimiento: {paciente['fecha_nacimiento']}")
        print(f"Edad: {edad} años")
        print(f"Nacionalidad: {paciente['nacionalidad']}")
        print("-" * 50)
        print()


def buscar_rango_fecha():
    """Busca historias clínicas de un paciente dentro de un rango de fechas."""
    # Revisar si hay pacientes cargados
    datos_pacientes = leer_json(PACIENTES_PATH)

    if not datos_pacientes:
        limpiar_consola()
        print("No hay pacientes registrados.\n")
        return

    # Solicitar un dato identificativo del paciente
    dni_paciente = input("Ingresar DNI del paciente: ").strip()

    # FIX: Agregar datos_pacientes como primer parámetro
    if not existe_dni(datos_pacientes, dni_paciente):
        limpiar_consola()
        print(f"No se encontró ningún paciente con DNI '{dni_paciente}'.\n")
        return

    # Recuperar paciente (FIX: Agregar datos_pacientes)
    paciente = obtener_por_dni(datos_pacientes, dni_paciente)

    # Recuperar id del paciente
    id_paciente = paciente["id"]

    # Recuperar datos de las historias clínicas
    datos_historias = leer_json(HISTORIAS_PATH)

    # Primer filtro: solo historias del paciente
    historias_paciente = list(
        filter(lambda e: e["id_paciente"] == id_paciente, datos_historias)
    )

    if not historias_paciente:
        limpiar_consola()
        print("El paciente no tiene ninguna historia clínica registrada.\n")
        return

    # Solicitar rango de fecha
    fecha_inicio_str = input("Ingrese fecha de inicio (DD/MM/YYYY): ").strip()
    fecha_final_str = input(
        "Ingrese fecha final (DD/MM/YYYY) - Enter para usar fecha actual: "
    ).strip()

    if not fecha_final_str:
        fecha_final_str = datetime.today().strftime("%d/%m/%Y")

    try:
        fecha_inicio = datetime.strptime(fecha_inicio_str, "%d/%m/%Y")
        fecha_final = datetime.strptime(fecha_final_str, "%d/%m/%Y")

        if fecha_final < fecha_inicio:
            limpiar_consola()
            print("Error: La fecha final no puede ser anterior a la fecha de inicio.\n")
            return

    except ValueError:
        limpiar_consola()
        print("Error: Formato de fecha inválido. Use DD/MM/YYYY.\n")
        return

    # Segundo filtro: historias dentro del rango de fechas
    # Convertir fechas del JSON (YYYY-MM-DD) a objetos datetime para comparar
    historias_en_rango = []
    for h in historias_paciente:
        try:
            # Intentar formato YYYY-MM-DD primero
            fecha_historia = datetime.strptime(h["fecha"], "%Y-%m-%d")
        except ValueError:
            # Si falla, intentar DD/MM/YYYY
            try:
                fecha_historia = datetime.strptime(h["fecha"], "%d/%m/%Y")
            except ValueError:
                continue  # Saltar si no se puede parsear

        if fecha_inicio <= fecha_historia <= fecha_final:
            historias_en_rango.append(h)

    if not historias_en_rango:
        limpiar_consola()
        print(
            "No se encontró ninguna historia clínica dentro del rango especificado.\n"
        )
        return

    # Cargar datos de médicos para mostrar información completa
    datos_medicos = leer_json(MEDICOS_PATH)

    # Mostrar información del paciente
    edad = calcular_edad(paciente["fecha_nacimiento"])
    limpiar_consola()
    print("\n" + "=" * 50)
    print("INFORMACIÓN DEL PACIENTE".center(50))
    print("=" * 50)
    print(f"ID:               {paciente['id']}")
    print(f"Nombre:           {paciente['nombre']} {paciente['apellido']}")
    print(f"DNI:              {paciente['dni']}")
    print(f"Fecha Nacimiento: {paciente['fecha_nacimiento']}")
    print(f"Edad:             {edad} años")
    print(f"Nacionalidad:     {paciente['nacionalidad']}")
    print("=" * 50 + "\n")

    print(f"=== HISTORIAS CLÍNICAS EN EL RANGO ({len(historias_en_rango)}) ===")
    print(f"Desde: {fecha_inicio_str} | Hasta: {fecha_final_str}\n")

    for indice, h in enumerate(historias_en_rango, 1):
        medico = obtener_por_id(datos_medicos, h["id_medico"])

        # Formatear fecha para mostrar
        try:
            fecha_obj = datetime.strptime(h["fecha"], "%Y-%m-%d")
            fecha_mostrar = fecha_obj.strftime("%d/%m/%Y")
        except ValueError:
            fecha_mostrar = h["fecha"]  # Usar tal cual si ya está en DD/MM/YYYY

        print(f"{indice}. Fecha: {fecha_mostrar}")
        if medico:
            print(
                f"   Médico: Dr/a. {medico['nombre']} {medico['apellido']} ({medico['especialidad']})"
            )
        print(f"   Afección: {h['enfermedad_afeccion']}")
        print(f"   Observaciones: {h['observaciones']}")
        print("-" * 50)
        print()


def buscar_nacionalidad():
    """Busca pacientes por nacionalidad (búsqueda parcial, case-insensitive)."""
    # Revisar si hay pacientes cargados
    pacientes = leer_json(PACIENTES_PATH)

    if not pacientes:
        limpiar_consola()
        print("No hay pacientes registrados.\n")
        return

    # Solicitar datos del paciente a buscar
    nacionalidad_busqueda = input(
        "Ingrese la nacionalidad del paciente (búsqueda parcial): "
    ).strip()

    if not nacionalidad_busqueda:
        limpiar_consola()
        print("Debe ingresar una nacionalidad.\n")
        return

    # Convertir a minúsculas para búsqueda case-insensitive
    nacionalidad_busqueda_lower = nacionalidad_busqueda.lower()

    # FIX: Búsqueda parcial y case-insensitive usando 'in'
    pacientes_filtrados = [
        p for p in pacientes if nacionalidad_busqueda_lower in p["nacionalidad"].lower()
    ]

    if not pacientes_filtrados:
        limpiar_consola()
        print(
            f"No se encontraron pacientes con nacionalidad que contenga '{nacionalidad_busqueda}'.\n"
        )
        return

    limpiar_consola()
    print(f"\n=== PACIENTES ENCONTRADOS ({len(pacientes_filtrados)}) ===")
    print(f"Criterio de búsqueda: '{nacionalidad_busqueda}'\n")

    for paciente in pacientes_filtrados:
        edad = calcular_edad(paciente["fecha_nacimiento"])
        print(f"ID: {paciente['id']}")
        print(f"Nombre: {paciente['nombre']} {paciente['apellido']}")
        print(f"DNI: {paciente['dni']}")
        print(f"Fecha Nacimiento: {paciente['fecha_nacimiento']}")
        print(f"Edad: {edad} años")
        print(f"Nacionalidad: {paciente['nacionalidad']}")
        print("-" * 50)
        print()


def buscar_enfermedad_afeccion():
    """Busca historias clínicas de un paciente por enfermedad/afección."""
    # Revisar si hay pacientes cargados
    datos_pacientes = leer_json(PACIENTES_PATH)

    if not datos_pacientes:
        limpiar_consola()
        print("No hay pacientes registrados.\n")
        return

    # Solicitar un dato identificativo del paciente
    dni_paciente = input("Ingresar DNI del paciente: ").strip()

    # FIX: Agregar datos_pacientes como primer parámetro
    if not existe_dni(datos_pacientes, dni_paciente):
        limpiar_consola()
        print(f"No se encontró ningún paciente con DNI '{dni_paciente}'.\n")
        return

    # Recuperar paciente (FIX: Agregar datos_pacientes)
    paciente = obtener_por_dni(datos_pacientes, dni_paciente)

    # Recuperar id del paciente
    id_paciente = paciente["id"]

    # Recuperar datos de las historias clínicas
    datos_historias = leer_json(HISTORIAS_PATH)

    # Primer filtro: solo historias del paciente
    historias_paciente = list(
        filter(lambda e: e["id_paciente"] == id_paciente, datos_historias)
    )

    if not historias_paciente:
        limpiar_consola()
        print("El paciente no tiene ninguna historia clínica registrada.\n")
        return

    # Solicitar enfermedad/afección
    enfermedad_afeccion = (
        input("Ingrese enfermedad/afección a buscar: ").strip().lower()
    )

    if not enfermedad_afeccion:
        limpiar_consola()
        print("No se ingresó ninguna enfermedad o afección.\n")
        return

    # Filtro por enfermedad/afección (búsqueda parcial)
    historias_enfermedad_afeccion = list(
        filter(
            lambda h: enfermedad_afeccion in h["enfermedad_afeccion"].lower(),
            historias_paciente,
        )
    )

    if not historias_enfermedad_afeccion:
        limpiar_consola()
        print(
            f"No se encontró ninguna historia clínica con '{enfermedad_afeccion}' para este paciente.\n"
        )
        return

    # Cargar datos de médicos
    datos_medicos = leer_json(MEDICOS_PATH)

    # Mostrar información del paciente
    edad = calcular_edad(paciente["fecha_nacimiento"])
    limpiar_consola()
    print("\n" + "=" * 50)
    print("INFORMACIÓN DEL PACIENTE".center(50))
    print("=" * 50)
    print(f"ID:               {paciente['id']}")
    print(f"Nombre:           {paciente['nombre']} {paciente['apellido']}")
    print(f"DNI:              {paciente['dni']}")
    print(f"Fecha Nacimiento: {paciente['fecha_nacimiento']}")
    print(f"Edad:             {edad} años")
    print(f"Nacionalidad:     {paciente['nacionalidad']}")
    print("=" * 50 + "\n")

    print(
        f"=== HISTORIAS CLÍNICAS POR ENFERMEDAD/AFECCIÓN ({len(historias_enfermedad_afeccion)}) ==="
    )
    print(f"Criterio de búsqueda: '{enfermedad_afeccion}'\n")

    for indice, h in enumerate(historias_enfermedad_afeccion, 1):
        medico = obtener_por_id(datos_medicos, h["id_medico"])

        # Formatear fecha para mostrar
        try:
            fecha_obj = datetime.strptime(h["fecha"], "%Y-%m-%d")
            fecha_mostrar = fecha_obj.strftime("%d/%m/%Y")
        except ValueError:
            fecha_mostrar = h["fecha"]

        print(f"{indice}. Fecha: {fecha_mostrar}")
        if medico:
            print(
                f"   Médico: Dr/a. {medico['nombre']} {medico['apellido']} ({medico['especialidad']})"
            )
        print(f"   Afección: {h['enfermedad_afeccion']}")
        print(f"   Observaciones: {h['observaciones']}")
        print("-" * 50)
        print()


def buscar_medico_trato():
    """Busca las atenciones que realizó un médico a un paciente específico."""
    datos_pacientes = leer_json(PACIENTES_PATH)
    datos_historias = leer_json(HISTORIAS_PATH)
    datos_medicos = leer_json(MEDICOS_PATH)

    if not datos_pacientes or not datos_historias or not datos_medicos:
        limpiar_consola()
        print(
            "Error: Faltan datos. Asegúrese de tener pacientes, médicos e historias clínicas registradas.\n"
        )
        return

    dni = input("Ingrese el DNI del paciente: ").strip()

    if not existe_dni(datos_pacientes, dni):
        limpiar_consola()
        print(f"No se encontró ningún paciente con DNI '{dni}'.\n")
        return

    # FIX: Agregar datos_pacientes como parámetro
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
        f"\n=== ATENCIONES MÉDICAS DE {paciente['nombre'].upper()} {paciente['apellido'].upper()} ===\n"
    )
    print(f"DNI: {dni}")
    print(f"Total de atenciones: {len(historias_paciente)}\n")
    print("-" * 60 + "\n")

    for i, h in enumerate(historias_paciente, 1):
        medico = obtener_por_id(datos_medicos, h["id_medico"])

        # Formatear fecha para mostrar
        try:
            fecha_obj = datetime.strptime(h["fecha"], "%Y-%m-%d")
            fecha_mostrar = fecha_obj.strftime("%d/%m/%Y")
        except ValueError:
            fecha_mostrar = h["fecha"]

        if medico:
            print(f"{i}. Fecha: {fecha_mostrar}")
            print(f"   Médico: Dr/a. {medico['nombre']} {medico['apellido']}")
            print(f"   Matrícula: {medico['matricula']}")
            print(f"   Especialidad: {medico['especialidad']}")
            print(f"   Enfermedad/Afección: {h['enfermedad_afeccion']}")
            print(f"   Observaciones: {h['observaciones']}")
            print("-" * 60)
            print()
        else:
            print(f"{i}. Fecha: {fecha_mostrar}")
            print(f"   [ERROR] Médico no encontrado (ID: {h['id_medico']})")
            print(f"   Enfermedad/Afección: {h['enfermedad_afeccion']}")
            print("-" * 60)
            print()


def buscar_pacientes_por_medico():
    """NUEVA FUNCIÓN: Busca todos los pacientes atendidos por un médico específico."""
    datos_pacientes = leer_json(PACIENTES_PATH)
    datos_historias = leer_json(HISTORIAS_PATH)
    datos_medicos = leer_json(MEDICOS_PATH)

    if not datos_pacientes or not datos_historias or not datos_medicos:
        limpiar_consola()
        print(
            "Error: Faltan datos. Asegúrese de tener pacientes, médicos e historias clínicas registradas.\n"
        )
        return

    matricula = input("Ingrese la matrícula del médico: ").strip()

    if not existe_matricula(datos_medicos, matricula):
        limpiar_consola()
        print(f"No se encontró ningún médico con matrícula '{matricula}'.\n")
        return

    medico = obtener_por_matricula(datos_medicos, matricula)
    id_medico = medico["id"]

    # Filtrar historias del médico
    historias_medico = list(
        filter(lambda h: h["id_medico"] == id_medico, datos_historias)
    )

    if not historias_medico:
        limpiar_consola()
        print(
            f"El médico {medico['nombre']} {medico['apellido']} no tiene atenciones registradas.\n"
        )
        return

    # Obtener pacientes únicos
    ids_pacientes = list(set([h["id_paciente"] for h in historias_medico]))

    limpiar_consola()
    print(
        f"\n=== PACIENTES ATENDIDOS POR DR/A. {medico['nombre'].upper()} {medico['apellido'].upper()} ===\n"
    )
    print(f"Matrícula: {medico['matricula']}")
    print(f"Especialidad: {medico['especialidad']}")
    print(f"Total de pacientes atendidos: {len(ids_pacientes)}")
    print(f"Total de atenciones: {len(historias_medico)}\n")
    print("-" * 60 + "\n")

    for id_pac in ids_pacientes:
        paciente = obtener_por_id(datos_pacientes, id_pac)
        if not paciente:
            continue

        # Contar atenciones a este paciente
        atenciones_paciente = [
            h for h in historias_medico if h["id_paciente"] == id_pac
        ]

        # Formatear última fecha
        try:
            fecha_obj = datetime.strptime(atenciones_paciente[-1]["fecha"], "%Y-%m-%d")
            ultima_fecha = fecha_obj.strftime("%d/%m/%Y")
        except ValueError:
            ultima_fecha = atenciones_paciente[-1]["fecha"]

        print(f"• Paciente: {paciente['nombre']} {paciente['apellido']}")
        print(f"  DNI: {paciente['dni']}")
        print(f"  Atenciones: {len(atenciones_paciente)}")
        print(f"  Última atención: {ultima_fecha}")
        print()


def menu_busquedas():
    """Menú principal del módulo de búsquedas."""
    while True:
        print("=== MÓDULO DE BÚSQUEDAS ===")
        print("Buscar Pacientes por:")
        print("1. Apellido y/o Nombre")
        print("2. Rango de fechas (historias clínicas)")
        print("3. Enfermedad/Afección")
        print("4. Atenciones de un paciente (por médico)")
        print("5. Nacionalidad")
        print("6. Pacientes atendidos por un médico")
        print("7. Volver al menú anterior")
        print("8. Salir del programa\n")

        try:
            opcion = int(input("Ingrese una opción: "))

            if opcion == 1:
                limpiar_consola()
                buscar_apellido_nombre()

            elif opcion == 2:
                limpiar_consola()
                buscar_rango_fecha()

            elif opcion == 3:
                limpiar_consola()
                buscar_enfermedad_afeccion()

            elif opcion == 4:
                limpiar_consola()
                buscar_medico_trato()

            elif opcion == 5:
                limpiar_consola()
                buscar_nacionalidad()

            elif opcion == 6:
                limpiar_consola()
                buscar_pacientes_por_medico()

            elif opcion == 7:
                limpiar_consola()
                break

            elif opcion == 8:
                print("Cerrando el programa...")
                exit()

            else:
                limpiar_consola()
                print(
                    "Opción no válida. Por favor, seleccione una opción entre 1 y 8.\n"
                )

        except ValueError:
            limpiar_consola()
            print("Error: No se ingresó un número válido.\n")
            continue
