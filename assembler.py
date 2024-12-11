from argparse import ArgumentParser
from pathlib import Path

opcodes = {
    "NOP": "0000",
    "HLT": "0001",
    "ADD": "0010",
    "SUB": "0011",
    "NOR": "0100",
    "AND": "0101",
    "XOR": "0110",
    "RSH": "0111",
    "LDI": "1000",
    "ADI": "1001",
    "JMP": "1010",
    "JMC": "1011"
}
conditions = {"Z": "00", "NZ": "01", "C": "10", "NC": "11"}

def parse_number(num_str):
    num_str = num_str.strip().lower()
    try:
        if num_str.endswith('b'): return int(num_str[:-1], 2)
        if num_str.endswith('h'): return int(num_str[:-1], 16)
        if num_str.endswith('d'): return int(num_str[:-1], 10)
        return int(num_str)
    except ValueError:
        raise ValueError(f"Invalid number: {num_str}")

def parse_line(line):
    parts = line.strip().split()
    mnemonic = parts[0]
    
    if mnemonic == "HLT":
        if len(parts) != 1: raise ValueError(f"{mnemonic} requires no operands")
        return f"{opcodes[mnemonic]}{0:012b}"
    
    if mnemonic in ["ADD", "SUB", "NOR", "AND", "XOR"]:
        if len(parts) != 4: raise ValueError(f"{mnemonic} requires 3 registers")
        rA, rB, rC = map(lambda x: int(x[1:]), parts[1:])
        return f"{opcodes[mnemonic]}{rA:04b}{rB:04b}{rC:04b}"
    
    if mnemonic == "RSH":
        if len(parts) != 3: raise ValueError(f"{mnemonic} requires 2 registers")
        rA, rC = map(lambda x: int(x[1:]), parts[1:])
        return f"{opcodes[mnemonic]}{0:04b}{rA:04b}{rC:04b}"
    
    if mnemonic in ["LDI", "ADI"]:
        if len(parts) != 3: raise ValueError(f"{mnemonic} requires an address and an immediate value")
        rA = int(parts[1][1:])
        imm = parse_number(parts[2])
        if not (0 < imm < 255): raise ValueError(f"Immediate value must be between 1 and 255")
        return f"{opcodes[mnemonic]}{rA:04b}{imm:08b}"
    
    if mnemonic == "JMP":
        if len(parts) != 2: raise ValueError(f"{mnemonic} requires an address")
        addr = parse_number(parts[1])
        if not (0 < addr < 1023): raise ValueError(f"Address must be from 0 to 1023")
        return f"{opcodes[mnemonic]}{0:02b}{addr:010b}"
    
    if mnemonic == "JMC":
        if len(parts) != 3: raise ValueError(f"{mnemonic} requires a condition and an address")
        condition = parts[1]
        if condition not in conditions: raise ValueError(f"Invalid condition: {condition}; Valid conditions: Z, NZ, C, NC")
        addr = parse_number(parts[2])
        if not (0 < addr < 1023): raise ValueError(f"Address must be from 0 to 1023")
        return f"{opcodes[mnemonic]}{conditions[condition]}{addr:010b}"
    
    raise ValueError(f"Mnemonic {mnemonic} is not supported")

def assemble(input_file, output_file):
    instructions = []
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()
        for i, line in enumerate(lines):
            line = line.split('#', 1)[0].strip()
            if not line: continue
            try:
                binary_word = parse_line(line)
                instructions.append(binary_word)
            except ValueError as e:
                print(f"Error on line {i}: {e}")
    with open(output_file, 'w') as f:
        f.write('\n'.join(instructions))

def main():
    parser = ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    input_file = args.filename
    output_file = str(Path(input_file).parent.absolute()) + "\\bins\\" + str(Path(input_file).stem) + ".bin"
    assemble(input_file, output_file)

if __name__ == "__main__":
    main()
