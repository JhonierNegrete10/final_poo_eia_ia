import os
import random
from datetime import datetime

from cliente import Cliente, CustomABC
from medicamentos import Medicamento, MedicamentoFacturado


# Clase Factura
class Factura(CustomABC):
    def __init__(self, cliente: Cliente):
        self.cliente = cliente
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.medicamentos_facturados: dict[str, MedicamentoFacturado] = dict()
        self.total = 0

    def agregar_medicamento(self, medicamento: Medicamento, cantidad):
        if medicamento.cantidad < cantidad:
            print(
                f"No hay suficiente inventario para el medicamento: \
                {medicamento.nombre_comercial}\
                hay solo {medicamento.cantidad} en vez {cantidad}\
                "
            )
            return None
        precio_con_impuesto = medicamento.calcular_precio_con_impuesto()
        medicamento_facturado = MedicamentoFacturado(
            medicamento, cantidad, precio_con_impuesto
        )
        self.medicamentos_facturados[medicamento_facturado.medicamento.sku] = (
            medicamento_facturado
        )
        self.total += medicamento_facturado.total
        medicamento.cantidad -= cantidad
        return True

    @staticmethod
    def crear_factura_ficticia(cliente: Cliente, inventario: list[Medicamento]):
        factura = Factura(cliente)
        for _ in range(random.randint(1, 5)):  # Añadir entre 1 y 5 medicamentos
            medicamento = random.choice(inventario)
            cantidad = random.randint(1, 3)  # Cantidad aleatoria entre 1 y 3
            done = factura.agregar_medicamento(medicamento, cantidad)
            if done:
                # todo: change presentation => be simple 
                print(f"Medicamento agregado: {medicamento}")
        print("\n\n")
        return factura

    def imprimir_factura(self):
        result = ""
        result += f"Factura: {self.fecha} \
            \n- Cliente: {self.cliente.nombre} \
            \n- Cédula: {self.cliente.cedula} \n\n"

        for medicamento_facturado in self.medicamentos_facturados.values():
            result += f"{medicamento_facturado.medicamento.nombre_comercial} \
                    \n - Cantidad: {medicamento_facturado.cantidad} \
                    \n - Precio unitario: {medicamento_facturado.precio_unitario} \
                    \n - Total: {medicamento_facturado.total} \n"

        result += f"\n Total a pagar: {self.total}"
        result += "\n\n"
        return result

    def __repr__(self):
        resultado = super().__repr__()
        return resultado

    # todo: Guardar factura en Factura
    # Esta factura iterará sobre medicamento facturado

    def guardar_factura(self, facturas_dir="./facturas"):
        # Todo: añadir validación de tipo
        if not os.path.exists(facturas_dir):
            os.makedirs(facturas_dir)

        factura_filename = f"factura_{self.cliente.cedula}_{self.fecha.replace(':', '').replace('-', '').replace(' ', '_')}.txt"
        factura_path = os.path.join(facturas_dir, factura_filename)

        with open(factura_path, "w") as file:
            file.write(self.imprimir_factura())
