import struct
import argparse
import os

def assemble(input_file, output_file, log_file):
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"Input file '{input_file}' not found.")

    binary_instructions = []
    log_entries = []

    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    for line in lines:
        parts = line.strip().split()
        command = parts[0]
        operands = list(map(int, parts[1:]))

        if command == 'LOAD_CONSTANT':
            A, B, C = operands
            instruction = (0x86 << 24) | (A << 16) | (B << 8) | C
            binary_instructions.append(instruction)
            log_entries.append(f"LOAD_CONSTANT A={A}, B={B}, C={C}")
        elif command == 'READ_MEMORY':
            A, B, C = operands
            instruction = (0xCA << 24) | (A << 16) | (B << 8) | C
            binary_instructions.append(instruction)
            log_entries.append(f"READ_MEMORY A={A}, B={B}, C={C}")
        elif command == 'WRITE_MEMORY':
            A, B, C, D = operands
            instruction = (0xEC << 24) | (A << 16) | (B << 8) | C | (D << 32)
            binary_instructions.append(instruction)
            log_entries.append(f"WRITE_MEMORY A={A}, B={B}, C={C}, D={D}")
        elif command == 'VECTOR_REMAINDER':
            A, B, C = operands
            instruction = (0xCE << 24) | (A << 16) | (B << 8) | C
            binary_instructions.append(instruction)
            log_entries.append(f"VECTOR_REMAINDER A={A}, B={B}, C={C}")

    with open(output_file, 'wb') as outfile:
        for instruction in binary_instructions:
            outfile.write(struct.pack('>I', instruction))

    with open(log_file, 'w') as logfile:
        logfile.write("\n".join(log_entries))

def load_binary(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

def execute_instructions(binary_data, memory):
    instruction_pointer = 0

    while instruction_pointer < len(binary_data):
        instruction = struct.unpack('>I', binary_data[instruction_pointer:instruction_pointer + 4])[0]
        op_code = (instruction >> 24) & 0xFF
        A = (instruction >> 16) & 0xFF
        B = (instruction >> 8) & 0xFF
        C = instruction & 0xFF
        
        if op_code == 0xCE:  # VECTOR_REMAINDER
            for i in range(6):
                memory[C + i] = memory[A + i] % memory[B + i]
        
        instruction_pointer += 4

def main(binary_file, memory_size):
    binary_data = load_binary(binary_file)
    memory = [0] * memory_size

    # Пример: заполнение памяти значениями векторов
    memory[0:6] = [10, 20, 30, 40, 50, 60]  # Первый вектор
    memory[6:12] = [3, 7, 4, 8, 6, 5]      # Второй вектор

    execute_instructions(binary_data, memory)

    # Запись результата в CSV
    with open('result.csv', 'w') as result_file:
        result_file.write('Index,Remainder\n')
        for i in range(6):
            result_file.write(f'{i},{memory[12 + i]}\n')  # Запись остатков

    print("Resulting memory (should contain the remainders):", memory[12:18])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Assembler and Interpreter for UVM')
    subparsers = parser.add_subparsers(dest='command')

    # Ассемблер
    assembler_parser = subparsers.add_parser('assemble')
    assembler_parser.add_argument('input_file', help='Path to the input source file')
    assembler_parser.add_argument('output_file', help='Path to the output binary file')
    assembler_parser.add_argument('log_file', help='Path to the log file')

    # Интерпретатор
    interpreter_parser = subparsers.add_parser('execute')
    interpreter_parser.add_argument('binary_file', help='Path to the binary file')
    interpreter_parser.add_argument('memory_size', type=int, help='Size of the memory')

    args = parser.parse_args()

    try:
        if args.command == 'assemble':
            assemble(args.input_file, args.output_file, args.log_file)
            print(f"Assembling completed: {args.output_file} and {args.log_file} created.")
        elif args.command == 'execute':
            main(args.binary_file, args.memory_size)
    except Exception as e:
        print(f"Error: {e}")
