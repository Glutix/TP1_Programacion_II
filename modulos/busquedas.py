from utils.constantes import PACIENTES_PATH, HISTORIAS_PATH
from utils.utilidades import leer_json, calcular_edad, buscar_paciente_dni, fecha_actual
from datetime import datetime
import os


def buscar_apellido_nombre():
    # Revisar si hay pacientes cargados
    pacientes = leer_json(PACIENTES_PATH)

    if not pacientes:
        print("No hay pacientes registrados.")
        return

    # Solicitar datos del paciente a buscar
    nombre = input("Ingresa el nombre del paciente: ")
    apellido = input("ingresa el apellido del paciente: ")
    paciente_encontrado = None

    for paciente in pacientes:
        if (
            paciente["nombre"].lower() == nombre.lower()
            and paciente["apellido"].lower() == apellido.lower()
        ):
            paciente_encontrado = paciente
            break

    if paciente_encontrado is None:
        print("No se encontro el paciente.")
        return

    # Calcular edad
    edad_paciente = calcular_edad(paciente_encontrado["fecha_nacimiento"])

    # Mostrar al paciente
    print("\n====== Información del Paciente ======")
    print(f"ID:               {paciente_encontrado['id']}")
    print(f"Nombre:           {paciente_encontrado['nombre']}")
    print(f"Apellido:         {paciente_encontrado['apellido']}")
    print(f"DNI:              {paciente_encontrado['dni']}")
    print(f"Fecha Nacimiento: {paciente_encontrado['fecha_nacimiento']}")
    print(f"Edad:             {edad_paciente} años")
    print(f"Nacionalidad:     {paciente_encontrado['nacionalidad']}")
    print("=======================================\n")


def buscar_rango_fecha():
    # Revisar si hay pacientes cargados
    pacientes = leer_json(PACIENTES_PATH)

    if not pacientes:
        print("No hay pacientes registrados.")
        return

    # Solicitar un dato indificativo del cliente
    dni_paciente = input("Ingresar DNI: ")

    paciente_encontrado = buscar_paciente_dni(dni_paciente, pacientes)

    if isinstance(paciente_encontrado, str):
        print(paciente_encontrado)
        return

    # recuperar paciente
    paciente = paciente_encontrado[0]

    # recuperar id del paciente
    id_paciente = paciente["id"]

    # recuperar datos de las historias clinicas
    historias_clinicas = leer_json(HISTORIAS_PATH)

    # Primer filtro: solo historias del paciente
    historias_paciente = list(
        filter(
            lambda elemento: elemento["id_paciente"] == id_paciente, historias_clinicas
        )
    )

    if not historias_paciente:
        print("El paciente no tiene ninguna historia clinica.")
        return

    # Solicitar rango de fecha
    fecha_inicio_str = input("Ingrese fecha de inicio (DD/MM/AAAA): ")
    fecha_final_str = input(
        "Ingrese fecha final (DD/MM/AAAA) no ingresar nada si quiere usar le fecha actual: "
    )

    fecha_final_str = fecha_final_str if fecha_final_str else fecha_actual()

    try:
        fecha_inicio = datetime.strptime(fecha_inicio_str, "%d/%m/%Y")
        fecha_final = datetime.strptime(fecha_final_str, "%d/%m/%Y")
    except ValueError:
        print("Formato de fecha inválido. Use DD/MM/AAAA.")
        return

    # Segundo filtro: historias dentro del rango de fechas
    historias_en_rango = list(
        filter(
            lambda elemento: fecha_inicio
            <= datetime.strptime(elemento["fecha"], "%d/%m/%Y")
            <= fecha_final,
            historias_paciente,
        )
    )

    if not historias_en_rango:
        print("No se encontro ninguna historia clinica dentro del rango.")
        return

    for historia in historias_en_rango:
        print(
            f"- {historia['fecha']} | {historia['enfermedad_aficcion']} | {historia['observaciones']}"
        )


def buscar_nacionalidad():
    # Revisar si hay pacientes cargados
    pacientes = leer_json(PACIENTES_PATH)

    if not pacientes:
        print("No hay pacientes registrados.")
        return

    # Solicitar datos del paciente a buscar
    nacionalidad = input("Ingresa la nacionalidad del paciente: ")

    paciente_encontrado = None
    for paciente in pacientes:
        if paciente["nacionalidad"].lower() == nacionalidad:
            paciente_encontrado = paciente
            break

    if paciente_encontrado is None:
        print("No se encontro el paciente.")
        return

    # Calcular edad
    edad_paciente = calcular_edad(paciente_encontrado["fecha_nacimiento"])

    # Mostrar al paciente
    print("\n====== Información del Paciente ======")
    print(f"ID:               {paciente_encontrado['id']}")
    print(f"Nombre:           {paciente_encontrado['nombre']}")
    print(f"Apellido:         {paciente_encontrado['apellido']}")
    print(f"DNI:              {paciente_encontrado['dni']}")
    print(f"Fecha Nacimiento: {paciente_encontrado['fecha_nacimiento']}")
    print(f"Edad:             {edad_paciente} años")
    print(f"Nacionalidad:     {paciente_encontrado['nacionalidad']}")
    print("=======================================\n")


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
                pass

            elif opcion == 4:
                pass

            elif opcion == 5:
                buscar_nacionalidad()

            elif opcion == 6:
                os.system("cls")
                break

            elif opcion == 7:
                print("Cerrando el programa...")
                exit()

        except ValueError:
            print("No se ingresó un número válido.")
            continue
