import json
import random
from abc import abstractmethod

from cliente import CustomABC, Medico


# Clase abstracta Medicamento
class Medicamento(CustomABC):
    def __init__(
        self,
        sku: str,
        nombre_comercial: str,
        nombre_generico: str,
        precio: float,
        impuesto: float,
        peso: float,
        cantidad: float,
    ):
        self.sku = sku
        self.nombre_comercial = nombre_comercial
        self.nombre_generico = nombre_generico
        self.precio = float(precio)
        self.impuesto = float(impuesto)
        self.peso = float(peso)
        self.cantidad = float(cantidad)

    def calcular_precio_con_impuesto(self):
        return self.precio + (self.precio * self.impuesto)

    @staticmethod
    @abstractmethod
    def medicamento_ficticio():
        pass


# Clase VentaLibre hereda de Medicamento
class VentaLibre(Medicamento):
    def __init__(
        self,
        sku,
        nombre_comercial,
        nombre_generico,
        precio,
        impuesto,
        peso,
        cantidad,
        contraindicaciones,
    ):
        super().__init__(
            sku, nombre_comercial, nombre_generico, precio, impuesto, peso, cantidad
        )
        self.contraindicaciones = contraindicaciones
        # self.tipo = self.__class__.__name__

    @staticmethod
    def medicamento_ficticio(nombre_medicamento: str, sku):
        return VentaLibre(
            sku=f"VL_{sku}",
            nombre_comercial=nombre_medicamento,
            nombre_generico=nombre_medicamento,
            precio=round(random.uniform(10, 100), 2),
            impuesto=0.19,
            peso=round(random.uniform(100, 500), 2),
            cantidad=random.randint(50, 200),
            contraindicaciones="Ninguna",
        )


# Clase Restringido hereda de Medicamento
class Restringido(Medicamento):
    def __init__(
        self,
        sku,
        nombre_comercial,
        nombre_generico,
        precio,
        impuesto,
        peso,
        cantidad,
        dosis_maxima: str,
        medico_autoriza: Medico | dict,
    ):
        super().__init__(
            sku, nombre_comercial, nombre_generico, precio, impuesto, peso, cantidad
        )
        self.dosis_maxima = dosis_maxima

        if isinstance(medico_autoriza, Medico):
            self.medico_autoriza = medico_autoriza
        elif isinstance(medico_autoriza, str):
            medico_autoriza: str = medico_autoriza.replace(";", ",")
            medico_dict = json.loads(medico_autoriza.replace("'", '"'))
            self.medico_autoriza: Medico = Medico.from_dict(medico_dict)

    @staticmethod
    def medicamento_ficticio(nombre_medicamento: str, sku):
        return Restringido(
            sku=f"RE_{sku}",
            nombre_comercial=nombre_medicamento,
            nombre_generico=nombre_medicamento,
            precio=round(random.uniform(10, 100), 2),
            impuesto=0.19,
            peso=round(random.uniform(100, 500), 2),
            cantidad=random.randint(50, 200),
            dosis_maxima="2 al día",
            medico_autoriza=Medico.medico_ficticio(),
        )


class MedicamentoFacturado(CustomABC):
    def __init__(
        self, medicamento: Medicamento, cantidad: float, precio_unitario: float
    ):
        self.medicamento = medicamento.copy()
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.total = precio_unitario * cantidad

    def imprimir(self):
        return f"SKU:{self.medicamento.sku} - {self.medicamento.nombre_comercial} \
- {self.precio_unitario:.2f} x {self.cantidad} - Total: {self.total:.2f}"
