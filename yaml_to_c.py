import yaml
import os
import sys

def clean_macro_name(name):
    return ''.join(c if c.isalnum() else '_' for c in name.upper())

def clean_c_string(value):
    lines = value.splitlines(keepends=True)
    escaped_lines = [line.replace("\\", "\\\\").replace('"', '\\"').replace('\n', '\\n') for line in lines]
    return '"{}"'.format(''.join(escaped_lines))

def write_yaml_to_c(macros_prefix, data, cf):
    if isinstance(data, dict):
        for key, val in data.items():
            macro_name = clean_macro_name(f"{macros_prefix}_{key}" if macros_prefix else key)
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
    if isinstance(value, str):
        return clean_c_string(value)
    elif isinstance(value, bool):
        return "1" if value else "0"
    elif value is None:
        return 'NULL'
    else:
        return str(value)

def yaml_to_c_header(yaml_file_path, c_header_path):
    with open(yaml_file_path, "r") as yf:
        data = yaml.safe_load(yf)

    with open(c_header_path, "w") as cf:
        cf.write("#ifndef YAML_CONTENT_H\n")
        write_yaml_to_c("", data, cf)
        cf.write("\n#endif \n")

def process_folder(input_folder, output_folder):
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