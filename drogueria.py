import random

from cliente import Cliente, Medico
from factura import Factura
from inventario import Inventario
from utils import add_box, mostrar_tabla


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
        if not self.clientes:
            print(add_box("\n Error: No hay clientes en la lista clientes \n"))
            return None
        if not self.inventario.medicamentos:
            print(
                add_box("\n Error: Actualmente no hay medicamentos en el inventario \n")
            )
            return None

        cliente = random.choice(self.clientes)
        factura = Factura.crear_factura_ficticia(cliente, self.inventario.medicamentos)
        self.agregar_factura(factura)

        return factura

    def cargar_inventario_desde_archivo(self, archivo):
        self.inventario.cargar_inventario_desde_archivo(archivo)

    def mostrar_inventario(self):
        print("\n")
        if self.inventario.medicamentos:
            headers = {
                "SKU   ": "sku",
                "Nombre Comercial": "nombre_comercial",
                "Nombre Genérico": "nombre_generico",
                "Precio": "precio",
                "Impuesto": "impuesto",
                "Peso     ": "peso",
                "Cantidad": "cantidad",
                "Tipo     ": "tipo",
            }
            self.inventario.mostrar_inventario(headers)
        else:
            print(
                add_box("\n Error: Actualmente no hay medicamentos en el inventario \n")
            )

    def crear_inventario_ficticio(self):
        self.inventario.crear_inventario_ficticio()

    def crear_personas_ficticia(self):
        for _ in range(3):
            self.agregar_cliente(Cliente.cliente_ficticio())
            self.agregar_medico(Medico.medico_ficticio())

    def mostrar_personas(self):
        print(add_box("Lista de Clientes"))
        headers = {
            "Nombre": "nombre",
            "Teléfono": "telefono",
            "Dirección": "direccion",
            "Cédula": "cedula",
        }
        mostrar_tabla(headers, self.clientes)

        print(add_box("Lista de Médicos"))
        headers = {
            "Nombre": "nombre",
            "Teléfono": "telefono",
            "Especialidad": "especialidad",
        }

        mostrar_tabla(headers, self.medicos)

    def mostrar_facturas(self):
        print(add_box("Lista de Facturas"))
        headers = {"    Fecha           ": "fecha", "Total    ": "total"}
        mostrar_tabla(headers, self.facturas)

    def guardar_inventario(self, formato):
        self.inventario.guardar_inventario(formato)
