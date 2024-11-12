import struct
import argparse
import csv
import os

def load_binary(file_path):
    """Загрузка бинарного файла с командами."""
    with open(file_path, 'rb') as file:
        return file.read()

def execute_instructions(binary_data, memory, log_file):
    """Выполнение инструкций из бинарных данных."""
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

            # Обработка команд
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

                    # Логирование каждой отдельной операции
                    log_writer.writerow(["VECTOR_REMAINDER", 
                                         f"A[{i}]={memory[A + i]}, B[{i}]={memory[B + i]}, "
                                         f"Result memory[C + {i}]={memory[C + i]}"])

            # Переход к следующей команде (шаг на 6 байт)
            instruction_pointer += 6

def main(binary_file, memory_size, output_file, log_file, memory_range_start, memory_range_end):
    """Основная функция для загрузки и выполнения инструкций."""
    binary_data = load_binary(binary_file)
    memory = [0] * memory_size

    # Инициализация памяти для тестов
    memory[0:6] = [10, 20, 30, 40, 50, 60]  # Инициализируем первый вектор
    memory[6:12] = [3, 7, 4, 8, 6, 5]       # Инициализируем второй вектор

    # Выполняем команды и записываем логи
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
    parser.add_argument('binary_file', help='Path to the binary file (e.g., output.bin)')
    parser.add_argument('memory_size', type=int, help='Size of the memory')
    parser.add_argument('output_file', help='Path to the result file (e.g., result_interpreter.csv)')
    parser.add_argument('log_file', help='Path to the log file for execution (e.g., execution_log.csv)')
    parser.add_argument('memory_range_start', type=int, help='Start of memory range to save')
    parser.add_argument('memory_range_end', type=int, help='End of memory range to save')
    args = parser.parse_args()

    try:
        main(args.binary_file, args.memory_size, args.output_file, args.log_file, args.memory_range_start, args.memory_range_end)
    except Exception as e:
        print(f"Error: {e}")
