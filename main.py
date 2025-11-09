from modulos.pacientes import menu_pacientes
from modulos.medicos import menu_medicos
from modulos.historias import menu_historial_clinico
from modulos.busquedas import menu_busquedas
from utils.utilidades import limpiar_consola

# Interfaz de usuario:
while True:
    print("=" * 60)
    print("Sistema de Gestión - 'Instituto Médico Las Luciérnagas'".center(60))
    print("=" * 60)
    print("1. Gestionar Pacientes")
    print("2. Gestionar Historias Clínicas")
    print("3. Gestionar Médicos")
    print("4. Gestionar Búsquedas")
    print("5. Salir\n")

    try:
        opcion = int(input("Seleccione una opción: "))

        # Menú de opciones
        if opcion == 1:
            limpiar_consola()
            menu_pacientes()

        elif opcion == 2:
            limpiar_consola()
            menu_historial_clinico()

        elif opcion == 3:
            limpiar_consola()
            menu_medicos()

        elif opcion == 4:
            limpiar_consola()
            menu_busquedas()

        elif opcion == 5:
            print("\nCerrando programa...")
            print("¡Hasta luego!")
            break

        else:
            limpiar_consola()
            print("Opción no válida. Por favor, seleccione una opción entre 1 y 5.\n")
            continue

    except ValueError:
        limpiar_consola()
        print("Error: Opción no válida. Por favor, ingrese un número entre 1 y 5.\n")
        continue
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario.")
        print("¡Hasta luego!")
        break
    except Exception as e:
        limpiar_consola()
        print(f"Error inesperado: {e}\n")
        continue
