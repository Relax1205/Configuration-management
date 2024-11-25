import csv
import struct
import sys

class VirtualMachine:
    def __init__(self, memory_size=1024):
        self.memory = [0] * memory_size
        self.registers = [0] * 64

    def execute(self, opcode, args):
        if opcode == 6:  # LOAD_CONST
            b, c = args
            if not (0 <= b < len(self.registers)):
                print(f"Error: Register {b} out of range.")
                return
            self.registers[b] = c
            print(f"LOAD_CONST: Register[{b}] = {c}")
        elif opcode == 10:  # READ_MEM
            b, c = args
            if not (0 <= b < len(self.registers)):
                print(f"Error: Register {b} out of range.")
                return
            if not (0 <= c < len(self.memory)):
                print(f"Error: Memory address {c} out of range.")
                return
            self.registers[b] = self.memory[c]
            print(f"READ_MEM: Register[{b}] = Memory[{c}] = {self.memory[c]}")
        elif opcode == 12:  # WRITE_MEM
            b, c, d = args
            if not (0 <= c < len(self.registers)) or not (0 <= d < len(self.registers)):
                print(f"Error: Register {c} or {d} out of range.")
                return
            addr = self.registers[c] + b
            if not (0 <= addr < len(self.memory)):
                print(f"Error: Memory address {addr} out of range.")
                return
            self.memory[addr] = self.registers[d]
            print(f"WRITE_MEM: Memory[{addr}] = Register[{d}] = {self.registers[d]}")
        elif opcode == 14:  # MODULO
            b, c, d, e = args
            if not (0 <= c < len(self.registers)) or not (0 <= d < len(self.registers)) or not (0 <= e < len(self.registers)):
                print(f"Error: Register {c}, {d} или {e} out of range.")
                return
            addr = self.registers[c] + b
            if not (0 <= addr < len(self.memory)):
                print(f"Error: Memory address {addr} out of range.")
                return
            if self.registers[e] == 0:
                print("Error: Division by zero in MODULO operation.")
                return
            result = self.memory[self.registers[d]] % self.registers[e]
            self.memory[addr] = result
            print(f"MODULO: Memory[{addr}] = {result} (result of {self.memory[self.registers[d]]} % {self.registers[e]})")
        else:
            print(f"Unknown opcode: {opcode}")

    def save_memory(self, start, end, output_file):
        with open(output_file, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(["Address", "Value"])
            for i in range(start, end + 1):
                writer.writerow([i, self.memory[i]])

def interpret(input_file, output_file, memory_range):
    vm = VirtualMachine()
    with open(input_file, 'rb') as binfile:
        chunk_number = 1
        while True:
            opcode_byte = binfile.read(1)
            if not opcode_byte:
                break  # Конец файла

            opcode = opcode_byte[0]
            print(f"Executing opcode: {opcode} (Chunk {chunk_number})")

            if opcode == 6:  # LOAD_CONST
                args_bytes = binfile.read(6)  # 2 байта для b, 4 байта для c
                if len(args_bytes) < 6:
                    raise ValueError(f"Incomplete LOAD_CONST command at chunk {chunk_number}")
                b, c = struct.unpack(">HI", args_bytes)
                vm.execute(opcode, (b, c))
            elif opcode == 10:  # READ_MEM
                args_bytes = binfile.read(4)  # 2 байта для b, 2 байта для c
                if len(args_bytes) < 4:
                    raise ValueError(f"Incomplete READ_MEM command at chunk {chunk_number}")
                b, c = struct.unpack(">HH", args_bytes)
                vm.execute(opcode, (b, c))
            elif opcode == 12:  # WRITE_MEM
                args_bytes = binfile.read(4)  # 2 байта для b, 1 байт для c, 1 байт для d
                if len(args_bytes) < 4:
                    raise ValueError(f"Incomplete WRITE_MEM command at chunk {chunk_number}")
                b, c, d = struct.unpack(">HBB", args_bytes)
                vm.execute(opcode, (b, c, d))
            elif opcode == 14:  # MODULO
                args_bytes = binfile.read(5)  # 2 байта для b, 1 байт для c, 1 байт для d, 1 байт для e
                if len(args_bytes) < 5:
                    raise ValueError(f"Incomplete MODULO command at chunk {chunk_number}")
                b, c, d, e = struct.unpack(">HBBB", args_bytes)
                vm.execute(opcode, (b, c, d, e))
            else:
                raise ValueError(f"Unknown opcode {opcode} at chunk {chunk_number}")

            chunk_number += 1

    start, end = map(int, memory_range.split("-"))
    vm.save_memory(start, end, output_file)
    print(f"Memory from {start} to {end} saved to {output_file}.")

def main():
    if len(sys.argv) != 4:
        print("Usage:")
        print("  python vm.py <input_bin> <output_csv> <memory_range>")
        print("Example:")
        print("  python vm.py output.bin memory_dump.csv 0-50")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    memory_range = sys.argv[3]

    # Диагностический вывод всего бинарного файла
    with open(input_file, 'rb') as f:
        content = f.read()
        print(f"Full binary file content: {content.hex()}")

    interpret(input_file, output_file, memory_range)

if __name__ == "__main__":
    main()