from drogueria import Drogueria


# Función para mostrar el menú interactivo
def mostrar_menu():
    print("Bienvenido al sistema de gestión de la Droguería")
    print("1. Cargar inventario desde archivo")
    print("2. Crear inventario ficticio")
    print("3. Mostrar inventario actual")
    print("4. Crear factura ficticia")
    # todo
    print("5. Crear personas ficticias (Clientes y Medicos)")
    print("6. Mostrar personas")
    print("7. Guardar inventario actual")

    print("0. Salir")
    opcion = input("Seleccione una opción: ")
    return opcion


# Función principal que ejecuta el menú interactivo
def main():
    drogueria = Drogueria()
    while True:
        opcion = mostrar_menu()
        if opcion == "1":
            print("\n NOTA: El archivo debe estar en la misma carpeta. \n")
            archivo = input("Ingrese el nombre del archivo con el inventario: ")
            drogueria.cargar_inventario_desde_archivo(archivo)
        elif opcion == "2":
            drogueria.crear_inventario_ficticio()
            # Todo: Mostrar que elementos se agregaron
            # finalizar mostrando el inventario.
        elif opcion == "3":
            drogueria.mostrar_inventario()
        elif opcion == "4":
            factura = drogueria.crear_factura_ficticia()
            print(factura.imprimir_factura())
        elif opcion == "5":
            drogueria.crear_personas_ficticia()
        elif opcion == "6":
            drogueria.mostrar_personas()
        elif opcion == "":
            drogueria.guardar_inventario()
            # drogueria.guardar_factura(factura)
        elif opcion == "0":
            print("Gracias por usar el sistema.")
            break
        else:
            print("Opción no válida, intente de nuevo.")


if __name__ == "__main__":
    main()
