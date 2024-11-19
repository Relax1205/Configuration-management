import csv
import struct
import sys


class VirtualMachine:
    def __init__(self, memory_size=1024):
        self.memory = [0] * memory_size
        self.registers = [0] * 64

    def execute(self, opcode, args):
        print(f"Executing opcode: {opcode}, with args: {args}")
        if opcode == 6:  # LOAD_CONST
            b, c = args
            print(f"LOAD_CONST: Register {b} = {c}")
            self.registers[b] = c
        elif opcode == 10:  # READ_MEM
            b, c = args
            print(f"READ_MEM: Register {b} = Memory[{c}] = {self.memory[c]}")
            self.registers[b] = self.memory[c]
        elif opcode == 12:  # WRITE_MEM
            b, c, d = args
            addr = self.registers[c] + b
            print(f"WRITE_MEM: Memory[{addr}] = Register[{d}] = {self.registers[d]}")
            self.memory[addr] = self.registers[d]
        elif opcode == 14:  # MODULO
            b, c, d, e = args
            addr = self.registers[c] + b
            result = self.memory[self.registers[d]] % self.registers[e]
            print(f"MODULO: Memory[{addr}] = {result} (result of {self.memory[self.registers[d]]} % {self.registers[e]})")
            self.memory[addr] = result
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
        while chunk := binfile.read(6):  # Читаем 6 байт за раз
            print(f"Reading chunk {chunk_number}: {chunk.hex()}")  # Отладочный вывод
            if len(chunk) < 6:
                break  # Если байт меньше 6, останавливаем выполнение

            opcode = chunk[0] >> 4  # Извлекаем опкод (старшие 4 бита)
            print(f"Read opcode: {opcode}, Chunk: {chunk.hex()}")

            if opcode == 0:
                print("End of file marker encountered. Stopping execution.")
                break  # Если опкод равен 0, останавливаем выполнение
            elif opcode == 6 or opcode == 10:  # LOAD_CONST или READ_MEM
                b = ((chunk[0] & 0xF) << 2) | (chunk[1] >> 6)
                c = ((chunk[1] & 0x3F) << 16) | struct.unpack(">H", chunk[2:4])[0]
                print(f"LOAD_CONST/READ_MEM: b={b}, c={c}")
                vm.execute(opcode, (b, c))
            elif opcode == 12:  # WRITE_MEM
                b = ((chunk[0] & 0xF) << 2) | (chunk[1] >> 6)
                c = ((chunk[1] & 0x3F) << 16) | chunk[2]
                d = chunk[3]
                print(f"WRITE_MEM: b={b}, c={c}, d={d}")
                vm.execute(opcode, (b, c, d))
            elif opcode == 14:  # MODULO
                b = ((chunk[0] & 0xF) << 2) | (chunk[1] >> 6)
                c = ((chunk[1] & 0x3F) << 16) | chunk[2]
                d, e = chunk[3:5]
                print(f"MODULO: b={b}, c={c}, d={d}, e={e}")
                vm.execute(opcode, (b, c, d, e))
            else:
                raise ValueError(f"Unknown opcode in binary file: {opcode}")

            chunk_number += 1

    start, end = map(int, memory_range.split("-"))
    vm.save_memory(start, end, output_file)


if __name__ == "__main__":
    interpret(sys.argv[1], sys.argv[2], sys.argv[3])
