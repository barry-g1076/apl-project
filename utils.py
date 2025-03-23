def check_type(variable):
    if isinstance(variable, int):
        return "Integer"
    elif isinstance(variable, str):
        return "String"
    elif isinstance(variable, float):
        return "Float"
    elif isinstance(variable, bool):
        return "Boolean"
    elif isinstance(variable, list):
        return "List"
    elif isinstance(variable, tuple):
        return "Tuple"
    elif isinstance(variable, set):
        return "Set"
    elif isinstance(variable, dict):
        return "Dictionary"
    elif isinstance(variable, complex):
        return "Complex"
    elif isinstance(variable, bytes):
        return "Bytes"
    elif isinstance(variable, bytearray):
        return "Bytearray"
    elif isinstance(variable, None):
        return "None"
    else:
        return "Unknown type"
