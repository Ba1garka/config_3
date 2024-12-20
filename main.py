import json
import re
import sys
from collections import OrderedDict
from datetime import datetime


def format_constants(constants, indent_level=1):
    indent = "    " * indent_level
    constant_definitions = []
    for key, value in constants.items():
        if not is_valid_name(key):
            raise ValueError(f"Invalid constant name '{key}'")
        constant_definition = f"(define {key} {format_value(value, indent_level)});\n"
        constant_definitions.append(constant_definition)
    return ''.join(constant_definitions)


def format_value(value, indent_level=1):
    indent = "    " * indent_level
    if isinstance(value, str):
        return f'q({value})'
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, list):
        items = [format_value(item, indent_level + 1) for item in value]
        return f"[\n{indent}    {',\n' + indent + '    '.join(items)}\n{indent}    ]"  # Handle lists
    elif isinstance(value, dict):
        return format_dict(value, indent_level + 1)
    else:
        raise ValueError("Unsupported type")


def format_dict(d, indent_level=1):
    indent = "    " * indent_level
    items = []
    total_keys = len(d)
    current_key_index = 0

    for key, value in d.items():
        if not is_valid_name(key):
            raise ValueError(f"Invalid name '{key}'")

        if key == 'constants':
            items.append(f"{indent}{key} = {{\n")
            for const_key in value:
                items.append(f"{indent}    {const_key} = @[ {const_key} ]")
                if const_key != list(value)[-1]:
                    items.append(',\n')
            items.append(f"\n{indent}}}")
            if current_key_index < total_keys - 1:
                items.append(',\n')
            current_key_index += 1
            continue

        item = f"{indent}{key} = {format_value(value, indent_level)}"
        items.append(item)
        if current_key_index < total_keys - 1:
            items.append(',\n')
        current_key_index += 1

    output = f"{{\n" + "".join(items).rstrip(',\n') + f"\n{indent[:-4]}}}"
    return output


def is_valid_name(name):
    return bool(re.match(r'[a-z][a-z0-9_]*', name))


def find_time_key(data, time_key='time'):
    """Ищет ключ time в любом месте JSON."""
    if isinstance(data, dict):
        if time_key in data:
            return data[time_key]
        for value in data.values():
            found = find_time_key(value, time_key)
            if found is not None:
                return found
    elif isinstance(data, list):
        for item in data:
            found = find_time_key(item, time_key)
            if found is not None:
                return found
    return None


def json_to_custom_config(json_data):
    constants = json_data.get('constants', {})

    time_value = find_time_key(json_data)

    iso_time = datetime.now().isoformat()

    time_definition = f"(define {time_value} {iso_time});\n" if time_value else ""

    constant_definitions = format_constants(constants)
    formatted_dict = format_dict(json_data)
    return time_definition + constant_definitions + formatted_dict
def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json_file>")
        sys.exit(1)
    json_file_path = sys.argv[1]
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file, object_pairs_hook=OrderedDict)
            result = json_to_custom_config(json_data)
            print(result)
    except FileNotFoundError:
        print(f"Error: File not found: {json_file_path}")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
