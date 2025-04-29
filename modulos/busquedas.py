from utils.constantes import PACIENTES_PATH
import os


def menu_busquedas():
    # Verificar si el archivo existe, si no, crearlo
    validar_archivo(PACIENTES_PATH)

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
                pass

            elif opcion == 2:
                pass

            elif opcion == 3:
                pass

            elif opcion == 4:
                pass

            elif opcion == 5:
                pass

            elif opcion == 6:
                os.system("cls")
                break

            elif opcion == 7:
                print("Cerrando el programa...")
                exit()

        except ValueError:
            print("No se ingresó un número válido.")
            continue
