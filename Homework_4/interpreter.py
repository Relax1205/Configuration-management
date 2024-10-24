import struct
import argparse
import os

def load_binary(file_path):
    with open(file_path, 'rb') as file:
        return file.read()  # Чтение в байтах

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
    # Заполняем вектор 1 (адрес 0)
    memory[0:6] = [10, 20, 30, 40, 50, 60]
    # Заполняем вектор 2 (адрес 6)
    memory[6:12] = [3, 7, 4, 8, 6, 5]

    execute_instructions(binary_data, memory)

    print("Resulting memory (should contain the remainders):", memory[12:18])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Interpreter for UVM')
    parser.add_argument('binary_file', help='Path to the binary file')
    parser.add_argument('memory_size', type=int, help='Size of the memory')
    args = parser.parse_args()

    try:
        main(args.binary_file, args.memory_size)
    except Exception as e:
        print(f"Error: {e}")
