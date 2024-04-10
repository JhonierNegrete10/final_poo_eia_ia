import csv
import json
import os
import random

from cliente import Cliente, Medico
from factura import Factura
from medicamentos import Medicamento, Restringido, VentaLibre
from utils import add_box


class Inventario:
    def __init__(self) -> None:
        self.medicamentos: list[Medicamento] = []

    def guardar_inventario(self):
        with open("inventario.csv", mode="w", newline="") as file:
            fieldnames = [
                "tipo",
                "sku",
                "nombre_comercial",
                "nombre_generico",
                "precio",
                "impuesto",
                "peso",
                "cantidad",
                "contraindicaciones",
                "dosis_maxima",
                "medico_autoriza",
            ]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for medicamento in self.medicamentos:
                writer.writerow(medicamento.to_dict())

    # Método para cargar inventario desde un archivo
    def cargar_inventario_desde_archivo(self, archivo="./inventario.txt"):
        # Validaciones que el archivo exista
        if not os.path.exists(archivo):
            print(
                add_box(
                    "\n  Error: El archivo especificado no existe."
                    + f"\n {archivo=} \n no existe en la carpeta:  {os.getcwd()}"
                    + "\n\n"
                )
            )
            return

        extension = os.path.splitext(archivo)[1]
        if extension == ".csv":
            self.cargar_inventario_csv(archivo)
        elif extension == ".json":
            self.cargar_inventario_json(archivo)
        elif extension == ".txt":
            self.cargar_inventario_txt(archivo)
        else:
            print(add_box("\n Error: Formato de archivo no soportado. \n\n"))

    def cargar_inventario_csv(self, archivo):
        venta_libre_ficticio: VentaLibre = VentaLibre.medicamento_ficticio("fake", 123)
        restringido_ficticio: Restringido = Restringido.medicamento_ficticio(
            "fake", 123
        )
        with open(archivo, mode="r", newline="", encoding="UTF-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                tipo = row.pop("tipo")
                if tipo == "VentaLibre":
                    # eliminar variables que no corresponden
                    row.pop("dosis_maxima")
                    row.pop("medico_autoriza")
                    #
                    if VentaLibre.validate_attr(
                        row, venta_libre_ficticio.export_schema_types()
                    ):
                        medicamento = VentaLibre(**row)
                    else:
                        print(
                            add_box("Error intentar crear VentaLibre cargado por csv")
                        )
                elif tipo == "Restringido":
                    row.pop("contraindicaciones")
                    schema = restringido_ficticio.export_schema_types()
                    schema.pop("medico_autoriza")
                    if Restringido.validate_attr(row, schema):
                        medicamento = Restringido(**row)
                self.medicamentos.append(medicamento)

    def cargar_inventario_json(self, archivo):
        with open(archivo, "r", encoding="UTF-8") as file:
            data: list[dict] = json.load(file)
            for entry in data:
                tipo = entry.pop("tipo")
                if tipo == "VentaLibre":
                    medicamento = VentaLibre(**entry)
                elif tipo == "Restringido":
                    medicamento = Restringido(**entry)
                self.medicamentos.append(medicamento)

    def cargar_inventario_txt(self, archivo):
        with open(archivo, "r", encoding="UTF-8") as file:
            for line in file:
                data = line.strip().split(";")
                if data[0] == "VentaLibre":
                    medicamento = VentaLibre(
                        **{
                            "sku": data[1],
                            "nombre_comercial": data[2],
                            "nombre_generico": data[3],
                            "precio": float(data[4]),
                            "impuesto": float(data[5]),
                            "peso": float(data[6]),
                            "cantidad": int(data[7]),
                            "contraindicaciones": data[8],
                        }
                    )
                elif data[0] == "Restringido":
                    medicamento = Restringido(
                        **{
                            "sku": data[1],
                            "nombre_comercial": data[2],
                            "nombre_generico": data[3],
                            "precio": float(data[4]),
                            "impuesto": float(data[5]),
                            "peso": float(data[6]),
                            "cantidad": int(data[7]),
                            "dosis_maxima": data[8],
                            "medico_autoriza": data[9],
                        }
                    )
                self.medicamentos.append(medicamento)

    def crear_inventario_ficticio(self):
        # Crear datos ficticios para medicamentos, clientes y médicos
        # Esta es una implementación simple y los datos deben ser más realistas
        nombres_medicamentos = ["Medicamento A", "Medicamento B", "Medicamento C"]
        for i in range(10):
            nombre_medicamento = random.choice(nombres_medicamentos)
            if random.choice([True, False]):
                medicamento = VentaLibre.medicamento_ficticio(nombre_medicamento, i)
            else:
                medicamento = Restringido.medicamento_ficticio(nombre_medicamento, i)
            self.medicamentos.append(medicamento)

    def mostrar_inventario(self):
        # Encabezados de la tabla
        headers = [
            "SKU",
            "Nombre Comercial",
            "Nombre Genérico",
            "Precio",
            "Impuesto",
            "Peso",
            "Cantidad",
            "Tipo",
        ]
        # Ancho de las columnas
        column_widths = [10, 20, 20, 10, 10, 10, 10, 15]

        # Imprimir los encabezados de la tabla
        header_row = "".join(
            f"{header:<{column_widths[i]}}" for i, header in enumerate(headers)
        )
        print(header_row)
        print("-" * sum(column_widths))  # Línea divisoria

        # Imprimir las filas de la tabla
        for medicamento in self.medicamentos:
            tipo_medicamento = (
                "VentaLibre" if isinstance(medicamento, VentaLibre) else "Restringido"
            )
            row = [
                f"{medicamento.sku:<{column_widths[0]}}",
                f"{medicamento.nombre_comercial[:column_widths[1] - 4]:<{column_widths[1] - 4}}... "
                if len(medicamento.nombre_comercial) > column_widths[1]
                else f"{medicamento.nombre_comercial:<{column_widths[1]}}",
                f"{medicamento.nombre_generico[:column_widths[2] - 4]:<{column_widths[2] - 4}}... "
                if len(medicamento.nombre_generico) > column_widths[2]
                else f"{medicamento.nombre_generico:<{column_widths[2]}}",
                f"{medicamento.precio:<{column_widths[3]}.2f}",
                f"{medicamento.impuesto:<{column_widths[4]}.2f}",
                f"{medicamento.peso:<{column_widths[5]}.2f}",
                f"{medicamento.cantidad:<{column_widths[6]}}",
                f"{tipo_medicamento:<{column_widths[7]}}",
            ]
            print("".join(row))
        print("\n")


class Drogueria:
    def __init__(self):
        self.inventario = Inventario()
        self.clientes: list[Cliente] = []
        self.medicos: list[Medico] = []
        self.facturas: list[Factura] = []

    def _isinstance(self, objeto, tipo):
        if isinstance(objeto, tipo):
            return True
        print(add_box(f"\n Error: No es del tipo {tipo.__name__} \n"))
        return False

    def agregar_cliente(self, cliente: Cliente):
        if self._isinstance(cliente, Cliente):
            self.clientes.append(cliente)

    def agregar_medico(self, medico: Medico):
        if self._isinstance(medico, Medico):
            self.medicos.append(medico)

    def agregar_factura(self, factura: Factura):
        if self._isinstance(factura, Factura):
            self.facturas.append(factura)

    def crear_factura_ficticia(self) -> None | Factura:
        # para crear una factura ficticia, debe haber clientes y medicamentos
        # todo: validaciones que haya clientes
        if not self.clientes:
            print(add_box("\n Error: No hay clientes en la lista clientes \n"))
            return None
        # todo: validaciones que haya inventario
        if not self.inventario.medicamentos:
            print(
                add_box("\n Error: Actualmente no hay medicamentos en el inventario \n")
            )
            return None

        cliente = random.choice(self.clientes)
        # cliente = Cliente.cliente_ficticio()
        factura = Factura.crear_factura_ficticia(cliente, self.inventario.medicamentos)
        self.agregar_factura(factura)

        return factura

    def cargar_inventario_desde_archivo(self, archivo):
        self.inventario.cargar_inventario_desde_archivo(archivo)

    def mostrar_inventario(self):
        # todo: validaciones de errores
        print("\n")
        if self.inventario.medicamentos:
            self.inventario.mostrar_inventario()
        else:
            print(
                add_box("\n Error: Actualmente no hay medicamentos en el inventario \n")
            )

    def crear_inventario_ficticio(self):
        self.inventario.crear_inventario_ficticio()

    def mostrar_facturas(self):
        # todo: mostrar facturas like a table
        for factura in self.facturas:
            print(factura)

    def crear_personas_ficticia(self):
        for _ in range(3):
            self.agregar_cliente(Cliente.cliente_ficticio())
            self.agregar_medico(Medico.medico_ficticio())

    def mostrar_personas(self):
        # todo: change presentation like a table
        print("\n --- Clientes ---")
        for cliente in self.clientes:
            print(cliente)

        print("\n\n --- Medicos ---")
        for medico in self.medicos:
            print(medico)
        print("\n\n")

    def guardar_inventario(self):
        self.inventario.guardar_inventario()
