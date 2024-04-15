import csv
import json
import os
import random
from abc import ABC, abstractmethod

from medicamentos import Medicamento, Restringido, VentaLibre
from utils import add_box, mostrar_tabla


# Abstract classes
class WriterInventario(ABC):
    @abstractmethod
    def guardar_inventario(self, file_name: str, medicamentos: list[Medicamento]):
        pass


class ReaderInventario(ABC):
    @abstractmethod
    def cargar_inventario(self, file_name: str) -> list[Medicamento]:
        pass


# Writers Implemtation classes
class WriterInventarioCSV(WriterInventario):
    def guardar_inventario(
        self, medicamentos: list[Medicamento], file_name: str = "inventario_.csv"
    ):
        with open(file_name, mode="w", newline="", encoding="UTF-8") as file:
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
            for medicamento in medicamentos:
                data = medicamento.to_dict()
                data["tipo"] = medicamento.__class__.__name__
                writer.writerow(data)


class WriterInventarioJSON(WriterInventario):
    def guardar_inventario(
        self, medicamentos: list[Medicamento], file_name: str = "inventario_.json"
    ):
        data = []
        for medicamento in medicamentos:
            med_dict = medicamento.to_dict()
            med_dict["tipo"] = medicamento.__class__.__name__
            data.append(med_dict)
        with open(file_name, "w", encoding="UTF-8") as file:
            json.dump(data, file, indent=4)


class WriterInventarioTXT(WriterInventario):
    def guardar_inventario(
        self, medicamentos: list[Medicamento], file_name: str = "inventario_.txt"
    ):
        with open(file_name, "w", encoding="UTF-8") as file:
            for medicamento in medicamentos:
                datos = medicamento.to_txt()
                datos = medicamento.__class__.__name__ + ";" + datos
                file.write(datos + "\n")


# %% Readers Implemtation classes
class ReaderInventarioCSV(ReaderInventario):
    def cargar_inventario(self, file_name: str) -> list[Medicamento]:
        # dummys para acceder a -> export_schema_types()
        vl_dummy = VentaLibre.medicamento_ficticio("fake", 123)
        r_dummy = Restringido.medicamento_ficticio("fake", 123)

        medicamentos = []
        with open(file_name, mode="r", newline="", encoding="UTF-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                tipo = row.pop("tipo")
                if tipo == "VentaLibre":
                    # eliminar variables que no corresponden
                    row.pop("dosis_maxima")
                    row.pop("medico_autoriza")
                    #
                    if VentaLibre.validate_attr(row, vl_dummy.export_schema_types()):
                        medicamento = VentaLibre(**row)
                    else:
                        print(
                            add_box("Error: intentar crear VentaLibre cargado por csv")
                        )
                elif tipo == "Restringido":
                    row.pop("contraindicaciones")
                    schema = r_dummy.export_schema_types()
                    schema.pop("medico_autoriza")
                    if Restringido.validate_attr(row, schema):
                        medicamento = Restringido(**row)
                    else:
                        print(
                            add_box("Error: intentar crear Restringido cargado por csv")
                        )
                medicamentos.append(medicamento)
        return medicamentos


class ReaderInventarioJSON(ReaderInventario):
    def cargar_inventario(self, file_name: str) -> list[Medicamento]:
        medicamentos = []
        with open(file_name, "r", encoding="UTF-8") as file:
            data: list[dict] = json.load(file)
            for entry in data:
                tipo = entry.pop("tipo")
                if tipo == "VentaLibre":
                    medicamento = VentaLibre(**entry)
                elif tipo == "Restringido":
                    medicamento = Restringido(**entry)
                medicamentos.append(medicamento)
        return medicamentos


class ReaderInventarioTXT(ReaderInventario):
    def cargar_inventario(self, file_name: str) -> list[Medicamento]:
        medicamentos = []
        with open(file_name, "r", encoding="UTF-8") as file:
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
                            "cantidad": int(float(data[7])),
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
                            "cantidad": int(float(data[7])),
                            "dosis_maxima": data[8],
                            "medico_autoriza": data[9],
                        }
                    )
                if medicamento:
                    medicamentos.append(medicamento)
        return medicamentos


# %% Inventario
class Inventario:
    def __init__(self) -> None:
        self.medicamentos: list[Medicamento] = []
        self.writer_inventario: WriterInventario
        self.reader_inventario: ReaderInventario

    def guardar_inventario(self, formato):
        # dict the readers
        if formato == "csv":
            self.writer_inventario = WriterInventarioCSV()
        elif formato == "json":
            self.writer_inventario = WriterInventarioJSON()
        elif formato == "txt":
            self.writer_inventario = WriterInventarioTXT()
        else:
            print(add_box("\n Error: Formato de archivo no soportado. \n\n"))
        self.writer_inventario.guardar_inventario(self.medicamentos)

    # Método para cargar inventario desde un archivo
    def cargar_inventario_desde_archivo(self, archivo="./inventario.txt"):
        # Validaciones que el archivo exista
        if not os.path.exists(archivo):
            print(
                add_box(
                    "\n  Error: El archivo especificado no existe."
                    + f"\n {archivo=} \n no existe en la carpeta:  {os.getcwd()}"
                )
            )
            return

        extension = os.path.splitext(archivo)[1]
        if extension == ".csv":
            self.reader_inventario = ReaderInventarioCSV()
        elif extension == ".json":
            self.reader_inventario = ReaderInventarioJSON()
        elif extension == ".txt":
            self.reader_inventario = ReaderInventarioTXT()
        else:
            print(add_box("\n Error: Formato de archivo no soportado. \n\n"))
            return
        self.medicamentos.extend(self.reader_inventario.cargar_inventario(archivo))

    def crear_inventario_ficticio(self):
        nombres_medicamentos = [
            "Paracetamol",
            "Ibuprofeno",
            "Aspirina",
            "Omeprazol",
            "Amoxicilina",
            "Loratadina",
            "Simvastatina",
            "Metformina",
            "Atorvastatina",
            "Ciprofloxacino",
            "Metronidazol",
            "Fluoxetina",
            "Losartán",
            "Amlodipino",
            "Levotiroxina",
            "Insulina",
            "Prednisona",
            "Diazepam",
            "Tramadol",
            "Warfarina",
        ]
        for i in range(10):
            nombre_medicamento = random.choice(nombres_medicamentos)
            sku = random.randint(100, 999)
            if random.choice([True, False]):
                medicamento = VentaLibre.medicamento_ficticio(nombre_medicamento, sku)
            else:
                medicamento = Restringido.medicamento_ficticio(nombre_medicamento, sku)
            self.medicamentos.append(medicamento)

    def mostrar_inventario(self, headers: dict):
        print(add_box("Inventario de Medicamentos"))
        mostrar_tabla(headers, self.medicamentos)
