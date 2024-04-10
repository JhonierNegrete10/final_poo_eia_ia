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
