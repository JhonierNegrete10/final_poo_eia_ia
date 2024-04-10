from cliente import CustomABC


def add_box(text: str):
    lines = text.split("\n")
    max_length = max(len(line) for line in lines)
    box_width = max_length + 4  # Add padding on both sides
    horizontal_border = "+" + "-" * box_width + "+"
    result = [horizontal_border]

    for line in lines:
        result.append(f"|  {line.ljust(max_length)}  |")  # Left align text
    result.append(horizontal_border)

    return "\n".join(result)


def mostrar_tabla(headers_mapping: dict, data: list[CustomABC]):
    # Ancho de las columnas
    column_widths = [len(header) + 3 for header in headers_mapping.keys()]

    # Imprimir los encabezados de la tabla
    header_row = "".join(
        f"{header:<{column_widths[i]}}"
        for i, header in enumerate(headers_mapping.keys())
    )
    print(header_row)
    print("-" * sum(column_widths))  # Línea divisoria

    # Imprimir las filas de la tabla
    for item in data:
        row = ""
        for i, header in enumerate(headers_mapping.keys()):
            if header == "Tipo     ":
                value = item.__class__.__name__
            else:
                attr = headers_mapping[header]
                value = str(getattr(item, attr))
            if len(value) > column_widths[i]:
                truncated_value = (
                    f"{value[:column_widths[i] - 4]:<{column_widths[i] - 4}}... "
                )
                row += truncated_value
            else:
                row += f"{value:<{column_widths[i]}}"
        print(row)
    print
