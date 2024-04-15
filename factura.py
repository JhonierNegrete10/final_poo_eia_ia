import os
import random
from datetime import datetime

from cliente import Cliente, CustomABC
from medicamentos import Medicamento, MedicamentoFacturado
from utils import add_box


class Factura(CustomABC):
    def __init__(self, cliente: Cliente):
        self.cliente = cliente
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.medicamentos_facturados: list[MedicamentoFacturado] = list()
        self.total = 0

    def agregar_medicamento(
        self, medicamento: Medicamento, cantidad
    ) -> tuple[bool, None | MedicamentoFacturado]:
        if medicamento.cantidad == 0:
            print(
                f"No hay inventario para el medicamento {medicamento.nombre_comercial}"
            )
            return (False, None)
        if medicamento.cantidad < cantidad:
            print(
                f"No hay suficiente inventario para el medicamento: \n {medicamento.nombre_comercial} hay solo {medicamento.cantidad} en vez {cantidad}"
            )
            cantidad = medicamento.cantidad
        precio_con_impuesto = medicamento.calcular_precio_con_impuesto()
        medicamento_facturado = MedicamentoFacturado(
            medicamento, cantidad, precio_con_impuesto
        )
        self.medicamentos_facturados.append(medicamento_facturado)
        self.total += medicamento_facturado.total
        medicamento.cantidad -= cantidad
        return (True, medicamento_facturado)

    @staticmethod
    def crear_factura_ficticia(cliente: Cliente, inventario: list[Medicamento]):
        factura = Factura(cliente)
        for _ in range(random.randint(3, 7)):
            medicamento = random.choice(inventario)
            cantidad = random.randint(1, 100)
            done, medicamento_facturado = factura.agregar_medicamento(
                medicamento, cantidad
            )
            if done:
                print()
                print(f"Medicamento agregado: {medicamento_facturado.imprimir()}")
        return factura

    def imprimir_factura(self):
        result = f"    Factura: {self.fecha} \
            \n- Cliente: {self.cliente.nombre} \
            \n- Cédula: {self.cliente.cedula} \n\n"

        for medicamento_facturado in self.medicamentos_facturados:
            result += f"{medicamento_facturado.medicamento.nombre_comercial} \
                    \n - SKU: {medicamento_facturado.medicamento.sku} \
                    \n - Cantidad: {medicamento_facturado.cantidad} \
                    \n - Precio unitario: {medicamento_facturado.precio_unitario:.2f} \
                    \n - Total: {medicamento_facturado.total:.2f} \n"

        result += f"\n Total a pagar: {self.total:.2f}"
        result += "\n\n"
        return result

    def guardar_factura(self, facturas_dir="./facturas"):
        if not os.path.exists(facturas_dir):
            os.makedirs(facturas_dir)

        factura_filename = f"factura_{self.cliente.cedula}_{self.fecha.replace(':', '').replace('-', '').replace(' ', '_')}_{random.randint(100, 999)}.txt"
        factura_path = os.path.join(facturas_dir, factura_filename)

        with open(factura_path, "w", encoding="UTF-8") as file:
            file.write(add_box(self.imprimir_factura()))
