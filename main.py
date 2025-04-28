from modulos.pacientes import menu_pacientes
import os

# Interfaz de usuario:
while True:
    os.system("cls")
    print("\n Sistema de Gestión - 'Instituto Médico Las Luciérnagas'")
    print(" 1. Gestionar Pacientes.")
    print(" 2. Gestionar Historias Clinícas.")
    print(" 3. Gestionar Médicos.")
    print(" 4. Salir.\n")

    try:
        opcion = int(input(" Seleccione una opcion: "))

        # Menu de opciones
        if opcion == 1:
            # limpiar consola
            os.system("cls")
            menu_pacientes()

        elif opcion == 2:
            os.system("cls")
            pass

        elif opcion == 3:
            os.system("cls")
            pass

        elif opcion == 4:
            os.system("cls")
            break

        else:
            print("Opción no válida. Por favor, seleccione una opción del 1 al 4.")
            continue
    except ValueError:
        print("Opción no válida. Por favor, ingrese un número.")
        continue


""" # Historial clinica
now = datetime.now()
fecha = f"{now.year}/{now.month}/{now.day} - {now.hour}:{now.minute}:{now.second}"
enfermedad_afeccion = "Corona virus"
medico = "Mauro Perez"
observaciones = "Mucha fiebre y mal de chaga"
historia_clinica = [
    {
        "fecha": fecha,
        "enfermedad_afeccion": enfermedad_afeccion,
        "medico": medico,
        "observaciones": observaciones,
    }
] """
