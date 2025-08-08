import yaml
import os
import sys


def clean_macro_name(name):
    """
    Clean and format a string to be used as a C macro name.

    Converts the input string to uppercase and replaces any non-alphanumeric
    characters with underscores to ensure it's a valid C macro identifier.

    Args:
        name (str): The input string to be converted to a macro name

    Returns:
        str: A cleaned string suitable for use as a C macro name
    """
    return ''.join(c if c.isalnum() else '_' for c in name.upper())


def clean_c_string(value):
    """
    Convert a Python string to C string literal.

    Args:
        value (str): The Python string to be converted

    Returns:
        str: A C string literal enclosed in double quotes
    """
    lines = value.splitlines(keepends=True)
    escaped_lines = [line.replace("\\", "\\\\").replace(
        '"', '\\"').replace('\n', '\\n') for line in lines]
    return '"{}"'.format(''.join(escaped_lines))


def write_yaml_to_c(macros_prefix, data, cf):
    """
    Recursively convert YAML data structure to C

    This function iterates through nested dictionaries and lists in the YAML data,
    convert each value to a C macro definition. 

    Args:
        macros_prefix (str): The prefix to use for macro names
        data: The YAML data to convert
        cf: File object to write the C macros to
    """
    if isinstance(data, dict):
        for key, val in data.items():
            macro_name = clean_macro_name(
                f"{macros_prefix}_{key}" if macros_prefix else key)
            if isinstance(val, (dict, list)):
                write_yaml_to_c(macro_name, val, cf)
            else:
                val_str = convert_value_to_c(val)
                cf.write(f"#define {macro_name} {val_str}\n")
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            macro_name = clean_macro_name(f"{macros_prefix}_{idx}")
            if isinstance(item, (dict, list)):
                write_yaml_to_c(macro_name, item, cf)
            else:
                val_str = convert_value_to_c(item)
                cf.write(f"#define {macro_name} {val_str}\n")
    else:
        macro_name = clean_macro_name(macros_prefix)
        val_str = convert_value_to_c(data)
        cf.write(f"#define {macro_name} {val_str}\n")


def convert_value_to_c(value):
    """
    Convert a Python value to its C representation.

    Handles different data types:
    - Strings: Converted to C string using clean_c_string()
    - Booleans: Converted to 1 or 0
    - None: Converted to NULL
    - Numbers: Converted to string

    Args:
        value: The Python value to convert

    Returns:
        str: The C representation of the value
    """
    if isinstance(value, str):
        return clean_c_string(value)
    elif isinstance(value, bool):
        return "1" if value else "0"
    elif value is None:
        return 'NULL'
    else:
        return str(value)


def yaml_to_c_header(yaml_file_path, c_header_path):
    """
    Convert a YAML file to a C header file with preprocessor macros.

    Reads the YAML file, parses its content, and generates a C header file
    containing #define statements for all the data in the YAML file.

    Args:
        yaml_file_path (str): Path to the input YAML file
        c_header_path (str): Path where the output C header file will be written
    """
    with open(yaml_file_path, "r") as yf:
        data = yaml.safe_load(yf)

    with open(c_header_path, "w") as cf:
        cf.write("#ifndef YAML_CONTENT_H\n")
        write_yaml_to_c("", data, cf)
        cf.write("\n#endif \n")


def process_folder(input_folder, output_folder):
    """
    Process all YAML files in a folder and convert them to C header files.

    Scans the input folder for files with .yaml or .yml extensions and converts
    each one to a corresponding .h file in the output folder. Creates the output
    folder if it doesn't exist. Prints progress messages and error handling.

    Args:
        input_folder (str): Path to the folder containing YAML files
        output_folder (str): Path to the folder where C header files will be written
    """
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith(".yaml") or filename.endswith(".yml"):
            yaml_path = os.path.join(input_folder, filename)
            header_filename = os.path.splitext(filename)[0] + ".h"
            header_path = os.path.join(output_folder, header_filename)
            print(f"Processing {yaml_path} -> {header_path}")
            try:
                yaml_to_c_header(yaml_path, header_path)
            except Exception as e:
                print(f"Failed to process {yaml_path}: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input_folder> <header_folder>")
        sys.exit(1)
    input_folder = sys.argv[1]
    output_folder = sys.argv[2]

    if not os.path.isdir(input_folder):
        print(f"Error: {input_folder} is not a directory.")
        sys.exit(1)

    process_folder(input_folder, output_folder)
