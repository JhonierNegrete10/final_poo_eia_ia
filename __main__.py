from drogueria import Drogueria
from utils import add_box


# Función para mostrar el menú interactivo
def mostrar_menu():
    print(add_box("Bienvenido al sistema de gestión de la Droguería"))
    print("1. Cargar inventario desde archivo")
    print("2. Crear inventario ficticio")
    print("3. Mostrar inventario actual")
    print("4. Crear personas ficticias (Clientes y Medicos)")
    print("5. Crear factura ficticia y guardarla en txt")
    print("6. Mostrar personas")
    print("7. Guardar inventario actual")
    print("8. Mostrar facturas")
    print("10. Crear todo")
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
            #
            drogueria.crear_inventario_ficticio()
            drogueria.mostrar_inventario()
        elif opcion == "3":
            drogueria.mostrar_inventario()
        elif opcion == "5":
            factura = drogueria.crear_factura_ficticia()
            if factura:
                # TODO: add box
                print(factura.imprimir_factura())
            # TODO : guardar factura en un txt with the box

        elif opcion == "4":
            drogueria.crear_personas_ficticia()
            drogueria.mostrar_personas()
        elif opcion == "6":
            drogueria.mostrar_personas()
        elif opcion == "8":
            drogueria.mostrar_facturas()
        elif opcion == "7":
            # TODO: input to save the file name
            # TODO: validations to extensions (only txt, json, csv)
            # TODO: validations dont be a path, only a filename avalible
            drogueria.guardar_inventario()

        elif opcion == "10":
            drogueria.crear_personas_ficticia()
            drogueria.crear_inventario_ficticio()
            factura = drogueria.crear_factura_ficticia()
            if factura:
                print(factura.imprimir_factura())

        elif opcion == "0":
            print("Gracias por usar el sistema.")
            break
        else:
            print("Opción no válida, intente de nuevo.")


if __name__ == "__main__":
    main()
