from drogueria import Drogueria
from utils import add_box


# Función para mostrar el menú interactivo
def mostrar_menu():
    print(add_box("Bienvenido al sistema de gestión de la Droguería"))
    print("Acciones relacionadas con el inventario:")
    print("1. Cargar inventario desde archivo (csv, json, txt)")
    print("2. Crear inventario ficticio")
    print("3. Mostrar inventario actual")
    print("4. Guardar inventario actual")
    print("\nAcciones relacionadas con personas:")
    print("5. Crear personas ficticias (Clientes y Medicos)")
    print("6. Mostrar personas")
    print("\nAcciones relacionadas con facturas:")
    print("7. Crear factura ficticia y guardarla en .txt")
    print("8. Mostrar facturas")
    print("\n10. Crear todo")
    print("0. Salir")
    opcion = input("Seleccione una opción: ")
    return opcion


# Función principal que ejecuta el menú interactivo
def main():
    drogueria = Drogueria()
    while True:
        opcion = mostrar_menu()
        if opcion == "1":
            print(add_box("\n NOTA: El archivo debe estar en la misma carpeta. \n"))
            archivo = input("Ingrese el nombre del archivo con el inventario: ")
            drogueria.cargar_inventario_desde_archivo(archivo)
            drogueria.mostrar_inventario()
        elif opcion == "2":
            drogueria.crear_inventario_ficticio()
            drogueria.mostrar_inventario()
        elif opcion == "3":
            drogueria.mostrar_inventario()
        elif opcion == "7":
            print(
                add_box(
                    "Nota: crear una factura ficticia, debe haber clientes y medicamentos subidos al sistema."
                )
            )
            factura = drogueria.crear_factura_ficticia()
            if factura:
                print(add_box(factura.imprimir_factura()))
                factura.guardar_factura()

        elif opcion == "5":
            drogueria.crear_personas_ficticia()
            drogueria.mostrar_personas()
        elif opcion == "6":
            drogueria.mostrar_personas()
        elif opcion == "8":
            drogueria.mostrar_facturas()
        elif opcion == "4":
            print()
            formato = input(
                "Ingrese el formato para guardar el inventario (csv, json, txt): "
            )
            drogueria.guardar_inventario(formato)

        elif opcion == "10":
            drogueria.crear_personas_ficticia()
            drogueria.mostrar_personas()
            drogueria.crear_inventario_ficticio()
            drogueria.mostrar_inventario()
            factura = drogueria.crear_factura_ficticia()
            if factura:
                print(add_box(factura.imprimir_factura()))

        elif opcion == "0":
            print(add_box("Gracias por usar el sistema."))
            break
        else:
            print("Opción no válida, intente de nuevo.")


if __name__ == "__main__":
    main()
