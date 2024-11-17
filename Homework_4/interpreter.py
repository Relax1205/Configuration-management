import struct
import argparse
import csv
import os

def load_binary(file_path):
    """Загрузка бинарного файла с командами."""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Binary file '{file_path}' not found.")
    with open(file_path, 'rb') as file:
        return file.read()

def execute_instructions(binary_data, memory, log_file):
    """Выполнение инструкций из бинарных данных."""
    instruction_pointer = 0

    with open(log_file, 'w', newline='', encoding='utf-8') as log:
        log_writer = csv.writer(log)
        log_writer.writerow(['Operation', 'Details'])  # Заголовок для логов

        while instruction_pointer < len(binary_data):
            # Проверка, что осталось как минимум 6 байт для инструкции
            if instruction_pointer + 6 > len(binary_data):
                log_writer.writerow(["ERROR", "Incomplete instruction at the end of binary data."])
                break

            instruction = struct.unpack('>BBBBBB', binary_data[instruction_pointer:instruction_pointer + 6])
            op_code = instruction[0]

            # Извлечение полей команды
            A = (instruction[1] >> 4) & 0xF
            B = ((instruction[1] & 0xF) << 2) | ((instruction[2] >> 6) & 0x3)
            C = ((instruction[2] & 0x3F) << 16) | (instruction[3] << 8) | instruction[4]
            D = (instruction[5] >> 4) & 0xF
            E = instruction[5] & 0xF

            if op_code == 0x86:  # LOAD_CONSTANT
                if B >= len(memory):
                    log_writer.writerow(["LOAD_CONSTANT", f"Error: Address B={B} out of memory bounds."])
                else:
                    memory[B] = C
                    log_writer.writerow(["LOAD_CONSTANT", f"memory[{B}] = {C}"])

            elif op_code == 0xCA:  # READ_MEMORY
                if C >= len(memory) or B >= len(memory):
                    log_writer.writerow(["READ_MEMORY", f"Error: Address C={C} or B={B} out of memory bounds."])
                else:
                    memory[B] = memory[C]
                    log_writer.writerow(["READ_MEMORY", f"memory[{B}] = memory[{C}] ({memory[C]})"])

            elif op_code == 0xEC:  # WRITE_MEMORY
                target_address = C + B
                if target_address >= len(memory) or D >= len(memory):
                    log_writer.writerow(["WRITE_MEMORY", f"Error: Address C+B={target_address} or D={D} out of memory bounds."])
                else:
                    memory[target_address] = memory[D]
                    log_writer.writerow(["WRITE_MEMORY", f"memory[{target_address}] = memory[{D}] ({memory[D]})"])

            elif op_code == 0xCE:  # REMAINDER
                # Выполняем: memory[C + B] = memory[memory[D]] % memory[E]
                if C + B >= len(memory) or D >= len(memory) or E >= len(memory):
                    log_writer.writerow(["REMAINDER", f"Error: Address C+B={C+B}, D={D}, or E={E} out of memory bounds."])
                else:
                    addr_d = memory[D]
                    addr_e = memory[E]
                    result_address = C + B

                    if addr_d >= len(memory) or addr_e >= len(memory) or result_address >= len(memory):
                        log_writer.writerow(["REMAINDER", f"Error: Nested address memory[{D}]={addr_d}, memory[{E}]={addr_e} out of bounds."])
                    else:
                        operand1 = memory[addr_d]
                        operand2 = memory[addr_e]
                        if operand2 != 0:
                            result = operand1 % operand2
                        else:
                            result = 0  # Если делитель равен 0, результат 0
                        memory[result_address] = result
                        log_writer.writerow([
                            "REMAINDER",
                            f"memory[{addr_d}] ({operand1}) % memory[{addr_e}] ({operand2}) = memory[{result_address}] ({result})"
                        ])

            else:
                log_writer.writerow(["UNKNOWN_COMMAND", f"Op code {op_code} at address {instruction_pointer} is not recognized."])

            # Переход к следующей инструкции (шаг на 6 байт)
            instruction_pointer += 6

def save_memory_range(memory, start, end, output_file):
    """Сохранение диапазона памяти в CSV файл."""
    if start < 0 or end >= len(memory) or start > end:
        raise ValueError(f"Invalid memory range: start={start}, end={end}, memory size={len(memory)}.")

    with open(output_file, 'w', newline='', encoding='utf-8') as result_file:
        csv_writer = csv.writer(result_file)
        csv_writer.writerow(['Address', 'Value'])  # Заголовок
        for i in range(start, end + 1):
            csv_writer.writerow([i, memory[i]])

    print(f"Memory values from {start} to {end} have been saved to '{output_file}'.")

def main(binary_file, memory_size, output_file, log_file, memory_range_start, memory_range_end):
    """Основная функция для загрузки и выполнения инструкций."""
    binary_data = load_binary(binary_file)
    memory = [0] * memory_size

    execute_instructions(binary_data, memory, log_file)
    save_memory_range(memory, memory_range_start, memory_range_end, output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Interpreter for UVM')
    parser.add_argument('binary_file', help='Path to the binary file (e.g., output.bin)')
    parser.add_argument('memory_size', type=int, help='Size of the memory')
    parser.add_argument('output_file', help='Path to the result file (CSV)')
    parser.add_argument('log_file', help='Path to the execution log file (CSV)')
    parser.add_argument('memory_range_start', type=int, help='Start of memory range to save')
    parser.add_argument('memory_range_end', type=int, help='End of memory range to save')

    args = parser.parse_args()

    try:
        main(args.binary_file, args.memory_size, args.output_file, args.log_file, args.memory_range_start, args.memory_range_end)
    except Exception as e:
        print(f"Error: {e}")
