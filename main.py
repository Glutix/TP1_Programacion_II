from modulos.pacientes import menu_pacientes
# from modulos.medicos import menu_medicos
# from modulos.historias import menu_historial_clinico
# from modulos.busquedas import menu_busquedas
from utils.utilidades import limpiar_consola

# Interfaz de usuario:
while True:
    limpiar_consola()
    print("\n Sistema de Gestión - 'Instituto Médico Las Luciérnagas'")
    print(" 1. Gestionar Pacientes.")
    print(" 2. Gestionar Historias Clinícas.")
    print(" 3. Gestionar Médicos.")
    print(" 4. Gestionar Busquedas.")
    print(" 5. Salir.\n")

    try:
        opcion = int(input(" Seleccione una opcion: "))

        # Menu de opciones
        if opcion == 1:
            limpiar_consola()
            menu_pacientes()

        elif opcion == 2:
            pass
            limpiar_consola()
            # menu_historial_clinico()

        elif opcion == 3:
            pass
            limpiar_consola()
            # menu_medicos()

        elif opcion == 4:
            pass
            limpiar_consola()
            # menu_busquedas()

        elif opcion == 5:
            limpiar_consola()
            break

        else:
            print("Opción no válida. Por favor, seleccione una opción del 1 al 4.")
            continue
    except ValueError:
        print("Opción no válida. Por favor, ingrese un número.")
        continue
