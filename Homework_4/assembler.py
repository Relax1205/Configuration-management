import struct
import csv
import argparse
import os

def assemble(input_file, output_file, log_file):
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"Input file '{input_file}' not found.")

    binary_instructions = []
    log_entries = [["Command", "A", "B", "C", "D"]]  # Заголовок для log.csv

    def parse_int(value):
        """Helper function to safely parse integers, defaulting to 0 if empty or invalid."""
        try:
            return int(value) if value else 0
        except ValueError:
            return 0

    with open(input_file, 'r') as infile:
        csv_reader = csv.DictReader(infile)
        for row in csv_reader:
            command = row['Command']
            A = parse_int(row['A'])
            B = parse_int(row['B'])
            C = parse_int(row['C'])
            D = parse_int(row['D'])

            if command == 'LOAD_CONSTANT':
                byte1 = 0x86
                byte2 = (A << 4) | ((B >> 4) & 0xF)
                byte3 = B & 0xFF
                byte4 = (C >> 16) & 0xFF
                byte5 = (C >> 8) & 0xFF
                byte6 = C & 0xFF
                instruction = struct.pack('>BBBBBB', byte1, byte2, byte3, byte4, byte5, byte6)
                log_entries.append(["Command=LOAD_CONSTANT", f"A={A}", f"B={B}", f"C={C}"])

            elif command == 'READ_MEMORY':
                byte1 = 0xCA
                byte2 = (A << 4) | ((B >> 4) & 0xF)
                byte3 = B & 0xFF
                byte4 = (C >> 16) & 0xFF
                byte5 = (C >> 8) & 0xFF
                byte6 = C & 0xFF
                instruction = struct.pack('>BBBBBB', byte1, byte2, byte3, byte4, byte5, byte6)
                log_entries.append(["Command=READ_MEMORY", f"A={A}", f"B={B}", f"C={C}"])

            elif command == 'WRITE_MEMORY':
                byte1 = 0xEC
                byte2 = (A << 4) | ((B >> 4) & 0xF)
                byte3 = B & 0xFF
                byte4 = (C >> 16) & 0xFF
                byte5 = (C >> 8) & 0xFF
                byte6 = (C & 0xFF) | ((D & 0xF) << 4)
                instruction = struct.pack('>BBBBBB', byte1, byte2, byte3, byte4, byte5, byte6)
                log_entries.append(["Command=WRITE_MEMORY", f"A={A}", f"B={B}", f"C={C}", f"D={D}"])

            elif command == 'VECTOR_REMAINDER':
                byte1 = 0xCE
                byte2 = (A << 4) | ((B >> 4) & 0xF)
                byte3 = B & 0xFF
                byte4 = (C >> 16) & 0xFF
                byte5 = (C >> 8) & 0xFF
                byte6 = C & 0xFF
                instruction = struct.pack('>BBBBBB', byte1, byte2, byte3, byte4, byte5, byte6)
                log_entries.append(["Command=VECTOR_REMAINDER", f"A={A}", f"B={B}", f"C={C}", f"D={D}"])

            binary_instructions.append(instruction)

    # Запись бинарных инструкций в output.bin файл
    with open(output_file, 'wb') as outfile:
        for instruction in binary_instructions:
            outfile.write(instruction)

    # Запись log.csv
    with open(log_file, 'w', newline='') as logfile:
        csv_writer = csv.writer(logfile)
        csv_writer.writerows(log_entries)

    print(f"Assembling completed. Output binary saved to {output_file} and log saved to {log_file}.")

def load_binary(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

def execute_instructions(binary_data, memory):
    instruction_pointer = 0

    while instruction_pointer < len(binary_data):
        instruction = struct.unpack('>BBBBBB', binary_data[instruction_pointer:instruction_pointer + 6])
        op_code = instruction[0]
        A = (instruction[1] >> 4) & 0xF
        B = ((instruction[1] & 0xF) << 8) | instruction[2]
        C = (instruction[3] << 16) | (instruction[4] << 8) | instruction[5]
        
        if op_code == 0x86:  # LOAD_CONSTANT
            memory[B] = C
            print(f"LOAD_CONSTANT: Loaded {C} to memory[{B}]")

        elif op_code == 0xCA:  # READ_MEMORY
            memory[B] = memory[C]
            print(f"READ_MEMORY: Read value {memory[B]} from memory[{C}] to memory[{B}]")

        elif op_code == 0xEC:  # WRITE_MEMORY
            memory[C + B] = memory[D]
            print(f"WRITE_MEMORY: Written value {memory[D]} to memory[{C + B}]")

        elif op_code == 0xCE:  # VECTOR_REMAINDER
            for i in range(6):
                memory[C + i] = memory[A + i] % memory[B + i] if memory[B + i] != 0 else 0
            print(f"VECTOR_REMAINDER: Remainder vector stored starting at memory[{C}]")

        instruction_pointer += 6

def main(binary_file, memory_size, output_file):
    binary_data = load_binary(binary_file)
    memory = [0] * memory_size

    memory[0:6] = [10, 20, 30, 40, 50, 60]  # Initialize first vector
    memory[6:12] = [3, 7, 4, 8, 6, 5]       # Initialize second vector

    execute_instructions(binary_data, memory)

    with open(output_file, 'w', newline='') as result_file:
        csv_writer = csv.writer(result_file)
        csv_writer.writerow(['Index', 'Remainder'])
        for i in range(6):
            csv_writer.writerow([i, memory[12 + i]])

    print(f"Execution completed. Result saved to {output_file}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Assembler and Interpreter for UVM')
    subparsers = parser.add_subparsers(dest='command')

    assembler_parser = subparsers.add_parser('assemble')
    assembler_parser.add_argument('input_file', help='Path to the input source file')
    assembler_parser.add_argument('output_file', help='Path to the output binary file')
    assembler_parser.add_argument('log_file', help='Path to the log file (e.g., result_assembler.csv)')

    interpreter_parser = subparsers.add_parser('execute')
    interpreter_parser.add_argument('binary_file', help='Path to the binary file (e.g., output.bin)')
    interpreter_parser.add_argument('memory_size', type=int, help='Size of the memory')
    interpreter_parser.add_argument('output_file', help='Path to the result file (e.g., result_interpreter.csv)')

    args = parser.parse_args()

    try:
        if args.command == 'assemble':
            assemble(args.input_file, args.output_file, args.log_file)
        elif args.command == 'execute':
            main(args.binary_file, args.memory_size, args.output_file)
    except Exception as e:
        print(f"Error: {e}")
