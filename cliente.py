import json
from abc import ABC #, abstractmethod


# Clase abstracta Usuario
class CustomABC(ABC):
    def __repr__(self):
        attributes = ", ".join(f"{key}={value}" for key, value in vars(self).items())
        return f"{self.__class__.__name__}({attributes})"

    # todo: do the same as __repr__ to export csv, txt, and json
    # todo: do the same as __repr__ to export export schema dict
    def to_csv(self, headers=True):
        """Export object attributes to CSV format."""
        values = ",".join(str(value) for value in vars(self).values())
        if headers:
            header = ",".join(vars(self).keys())
            return f"{header}\n{values}"
        return values

    def to_txt(self):
        """Export object attributes to TXT format."""
        # lines = [f"{key}: {value}" for key, value in vars(self).items()]
        # return "\n".join(lines)
        lines = [f"{value}" for _, value in vars(self).items()]
        return ";".join(lines)

    def to_json(self):
        """Export object attributes to JSON format."""
        return json.dumps(vars(self), indent=4)

    def export_schema(self):
        """Export the schema of the object as a dictionary."""
        return {key: type(value).__name__ for key, value in vars(self).items()}


class Usuario(CustomABC):
    def __init__(self, nombre, telefono):
        self.nombre = nombre
        self.telefono = telefono


# Clase Cliente hereda de Usuario
class Cliente(Usuario):
    def __init__(self, nombre, telefono, direccion, cedula):
        super().__init__(nombre, telefono)
        self.direccion = direccion
        self.cedula = cedula

    @staticmethod
    def cliente_ficticio():
        return Cliente("ficticio", 311456987, "Aqui", "12345666")


# Clase Medico hereda de Usuario
class Medico(Usuario):
    def __init__(self, nombre, telefono, especialidad):
        super().__init__(nombre, telefono)
        self.especialidad = especialidad


if __name__ == "__main__":
    # Create a User instance
    user = Medico("Alice", 300123987, "ginecologo")

    # Export to CSV
    print("csv: ", user.to_csv())
    print("csv: ", user.to_csv(headers=False))

    # Export to TXT
    print("txt: ", user.to_txt())

    # Export to JSON
    print("json: ", user.to_json())

    # Export schema
    print("schema: ", user.export_schema())

    print("__repr__: ", user)
