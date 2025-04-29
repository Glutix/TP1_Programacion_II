from modulos.pacientes import menu_pacientes
from modulos.medicos import menu_medicos
from modulos.historias import menu_historial_clinico
from modulos.busquedas import menu_busquedas
import os

# Interfaz de usuario:
while True:
    os.system("cls")
    print("\n Sistema de Gestión - 'Instituto Médico Las Luciérnagas'")
    print(" 1. Gestionar Pacientes.")
    print(" 2. Gestionar Historias Clinícas.")
    print(" 3. Gestionar Médicos.")
    print(" 4. Buscar a un cliente.")
    print(" 5. Salir.\n")

    try:
        opcion = int(input(" Seleccione una opcion: "))

        # Menu de opciones
        if opcion == 1:
            # limpiar consola
            os.system("cls")
            menu_pacientes()

        elif opcion == 2:
            os.system("cls")
            menu_historial_clinico()

        elif opcion == 3:
            os.system("cls")
            menu_medicos()

        elif opcion == 4:
            os.system("cls")
            menu_busquedas()

        elif opcion == 5:
            os.system("cls")
            break

        else:
            print("Opción no válida. Por favor, seleccione una opción del 1 al 4.")
            continue
    except ValueError:
        print("Opción no válida. Por favor, ingrese un número.")
        continue
