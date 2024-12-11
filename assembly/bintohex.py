import argparse
from pathlib import Path

def bin_to_hex(binary_line):
    if len(binary_line) != 16 or not all(c in "01" for c in binary_line):
        raise ValueError(f"Invalid binary line: {binary_line}")
    return f"{int(binary_line, 2):04x}"

def convert_file(input_file):
    hex_lines = []
    with open(input_file, "r") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                hex_line = bin_to_hex(line)
                hex_lines.append(hex_line)
            except ValueError as e:
                print(f"Error on line {line_number}: {e}")
                return None
    return hex_lines

def write_hex_file(hex_lines, output_file):
    with open(output_file, "w") as f:
        f.write("\n".join(hex_lines))

def toHex(input_file, output_file):
    hex_lines = convert_file(input_file)
    if hex_lines is not None:
        write_hex_file(hex_lines, output_file)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    input_file = args.filename
    output_file = str(Path(input_file).parent.parent.absolute()) + "\\hex\\" + str(Path(input_file).stem) + ".hex"
    toHex(input_file, output_file)

if __name__ == "__main__":
    main()