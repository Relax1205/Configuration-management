import struct
import argparse
import csv

def load_binary(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

def execute_instructions(binary_data, memory, log_file):
    instruction_pointer = 0

    # Открываем лог-файл для записи
    with open(log_file, 'w', newline='') as log:
        log_writer = csv.writer(log)
        log_writer.writerow(['Operation', 'Details'])  # Заголовок для логов

        while instruction_pointer < len(binary_data):
            instruction = struct.unpack('>BBBBBB', binary_data[instruction_pointer:instruction_pointer + 6])
            op_code = instruction[0]
            
            # Извлечение полей команды
            A = (instruction[1] >> 4) & 0xF
            B = ((instruction[1] & 0xF) << 8) | instruction[2]
            C = (instruction[3] << 16) | (instruction[4] << 8) | (instruction[5] & 0xFF)
            D = (instruction[5] >> 4) & 0xF  # Используется только в некоторых командах

            if op_code == 0x86:  # LOAD_CONSTANT
                memory[B] = C
                log_writer.writerow(["LOAD_CONSTANT", f"B={B}, C={C} -> memory[{B}] = {memory[B]}"])

            elif op_code == 0xCA:  # READ_MEMORY
                memory[B] = memory[C]
                log_writer.writerow(["READ_MEMORY", f"B={B}, C={C} -> memory[{B}] = {memory[C]}"])

            elif op_code == 0xEC:  # WRITE_MEMORY
                memory[C + B] = memory[D]
                log_writer.writerow(["WRITE_MEMORY", f"C+B={C + B}, D={D} -> memory[{C + B}] = {memory[D]}"])

            elif op_code == 0xCE:  # VECTOR_REMAINDER
                log_writer.writerow(["VECTOR_REMAINDER", 
                                     f"Before: A={A}, B={B}, C={C}, memory[A:A+6]={memory[A:A+6]}, memory[B:B+6]={memory[B:B+6]}"])
                
                for i in range(6):
                    if memory[B + i] != 0:
                        memory[C + i] = memory[A + i] % memory[B + i]
                    else:
                        memory[C + i] = 0  # Устанавливаем в 0, если делитель равен 0

                log_writer.writerow(["VECTOR_REMAINDER", f"After: memory[C:C+6]={memory[C:C+6]}"])

            # Переход к следующей команде (шаг на 6 байт)
            instruction_pointer += 6

def main(assembler_output, memory_size, output_file, memory_range_start, memory_range_end):
    # Загружаем бинарные данные из result_assembler.csv
    binary_data = load_binary(assembler_output)
    memory = [0] * memory_size
    log_file = 'result_interpreter.csv'

    # Инициализация значений для отладки
    memory[0:6] = [10, 15, 30, 55, 45, 100]  # Вектор делимых (увеличены значения)
    memory[6:12] = [3, 7, 4, 8, 6, 9]        # Вектор делителей (изменены значения)

    # Выполняем команды и записываем логи в result_interpreter.csv
    execute_instructions(binary_data, memory, log_file)

    # Запись диапазона значений памяти в CSV файл
    with open(output_file, 'w', newline='') as result_file:
        csv_writer = csv.writer(result_file)
        csv_writer.writerow(['Address', 'Value'])  # Заголовок
        for i in range(memory_range_start, memory_range_end + 1):
            csv_writer.writerow([i, memory[i]])

    print(f"Memory values from {memory_range_start} to {memory_range_end} have been saved to {output_file}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Interpreter for UVM')
    parser.add_argument('assembler_output', help='Path to the result_assembler.csv file')
    parser.add_argument('memory_size', type=int, help='Size of the memory')
    parser.add_argument('output_file', help='Path to the output CSV file')
    parser.add_argument('memory_range_start', type=int, help='Start of memory range to save')
    parser.add_argument('memory_range_end', type=int, help='End of memory range to save')
    args = parser.parse_args()

    try:
        main(args.assembler_output, args.memory_size, args.output_file, args.memory_range_start, args.memory_range_end)
    except Exception as e:
        print(f"Error: {e}")
