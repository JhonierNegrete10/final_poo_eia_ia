import json
import random
from abc import ABC  # , abstractmethod
from copy import deepcopy


# Clase abstracta Usuario
class CustomABC(ABC):
    def __repr__(self):
        attributes = ", ".join(f"{key}={value}" for key, value in vars(self).items())
        return f"{self.__class__.__name__}({attributes})"

    def copy(self):
        """Return a deep copy of the instance."""
        return deepcopy(self)

    def to_csv(self, headers=True):
        """Export object attributes to CSV format."""
        values = ",".join(str(value) for value in vars(self).values())
        if headers:
            header = ",".join(vars(self).keys())
            return f"{header}\n{values}"
        return values

    def to_txt(self):
        """Export object attributes to TXT format."""
        lines = [
            f"{value}" if type(value) in [str, int, float] else f"{value.to_dict()}"
            for _, value in vars(self).items()
        ]
        return ";".join(lines)

    def to_json(self):
        """Export object attributes to JSON format."""
        return json.dumps(vars(self), indent=4)

    def export_schema(self):
        """Export the schema of the object as a dictionary."""
        return {key: type(value).__name__ for key, value in vars(self).items()}

    def export_schema_types(self):
        """Export the schema of the object as a dictionary."""
        return {key: type(value) for key, value in vars(self).items()}

    def to_dict(self, tipo=False):
        """Export object attributes of the object as a dictionary."""
        return {
            key: value if type(value) in [str, int, float] else value.to_dict()
            for key, value in vars(self).items()
        }

    @staticmethod
    def validate_attr(input_attr: dict, schema: dict):
        """Static method to validate the type of the input attributes

        Args:
            input_attr (dict): dict read from the files
            schema (dict): {cls}.export_schema_types()

        Returns:
            bool: confirmation if the input validation is correct
        """
        for attr, _type in schema.items():
            if attr not in input_attr.keys():
                print(f"Falta el atributo requerido: {attr}")
                return False
            try:
                converted_value = _type(input_attr[attr])

            except (ValueError, TypeError):
                print(
                    f"El valor del atributo {attr} no se puede convertir al tipo {_type} \n "
                    + f"{type(input_attr[attr])}"
                )
                return False

            if not isinstance(converted_value, _type):
                print(f"El atributo {attr} debe ser de tipo {_type}")
                return False
        return True


class Usuario(CustomABC):
    def __init__(self, nombre: str, telefono: int):
        self.nombre = nombre
        self.telefono = int(telefono)

    @staticmethod
    def random_name():
        names = [
            "Briana Choi",
            "Heather Walter",
            "Ashley Roman",
            "Jon Love",
            "Gregory Davis",
            "Lisa Williams",
            "Linda Marsh",
            "Erica Jackson",
            "Krista Adams",
            "Alexis Gordon",
        ]
        return random.choice(names)


class Cliente(Usuario):
    def __init__(self, nombre, telefono, direccion, cedula):
        super().__init__(nombre, telefono)
        self.direccion = direccion
        self.cedula = cedula

    @staticmethod
    def cliente_ficticio():
        telefono = random.randint(300000000, 3159999999)
        cedula = random.randint(100000000, 1239999999)
        return Cliente(Usuario.random_name(), telefono, "Medellin", str(cedula))


class Medico(Usuario):
    def __init__(self, nombre, telefono, especialidad):
        super().__init__(nombre, telefono)
        self.especialidad = especialidad

    @staticmethod
    def medico_ficticio():
        telefono = random.randint(300000000, 3159999999)
        especialidad = random.choice(
            [
                "Cardiología",
                "Dermatología",
                "Endocrinología",
                "Gastroenterología",
                "Geriatría",
                "Ginecología",
                "Hematología",
                "Medicina Interna",
                "Nefrología",
                "Neumología",
                "Neurología",
                "Obstetricia",
                "Oncología",
                "Oftalmología",
                "Ortopedia",
                "Otorrinolaringología",
                "Pediatría",
                "Psiquiatría",
                "Radiología",
                "Traumatología",
            ]
        )
        return Medico(Usuario.random_name(), telefono, especialidad)

    @staticmethod
    def from_dict(dict: dict):
        return Medico(**dict)
