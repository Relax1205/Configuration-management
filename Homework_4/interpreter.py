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

def execute_instructions(binary_data, regs, log_file):
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
                if B >= len(regs):
                    log_writer.writerow(["LOAD_CONSTANT", f"Error: Address B={B} out of memory bounds."])
                else:
                    regs[B] = C
                    log_writer.writerow(["LOAD_CONSTANT", f"regs[{B}] = {C}"])

            elif op_code == 0xCA:  # READ_MEMORY
                if C >= len(regs) or B >= len(regs):
                    log_writer.writerow(["READ_MEMORY", f"Error: Address C={C} or B={B} out of memory bounds."])
                else:
                    regs[B] = regs[C]
                    log_writer.writerow(["READ_MEMORY", f"regs[{B}] = regs[{C}] ({regs[C]})"])

            elif op_code == 0xEC:  # WRITE_MEMORY
                target_address = C + B
                if target_address >= len(regs) or D >= len(regs):
                    log_writer.writerow(["WRITE_MEMORY", f"Error: Address C+B={target_address} or D={D} out of memory bounds."])
                else:
                    regs[target_address] = regs[D]
                    log_writer.writerow(["WRITE_MEMORY", f"regs[{target_address}] = regs[{D}] ({regs[D]})"])

            elif op_code == 0xCE:  # REMAINDER
                # Выполняем: regs[C + B] = regs[regs[D]] % regs[E]
                if C + B >= len(regs) or D >= len(regs) or E >= len(regs):
                    log_writer.writerow(["REMAINDER", f"Error: Address C+B={C+B}, D={D}, or E={E} out of memory bounds."])
                else:
                    addr_d = regs[D]
                    addr_e = regs[E]
                    result_address = C + B

                    if addr_d >= len(regs) or addr_e >= len(regs) or result_address >= len(regs):
                        log_writer.writerow(["REMAINDER", f"Error: Nested address regs[{D}]={addr_d}, regs[{E}]={addr_e} out of bounds."])
                    else:
                        operand1 = regs[addr_d]
                        operand2 = regs[addr_e]
                        if operand2 != 0:
                            result = operand1 % operand2
                        else:
                            result = 0  # Если делитель равен 0, результат 0
                        regs[result_address] = result
                        log_writer.writerow([
                            "REMAINDER",
                            f"regs[{addr_d}] ({operand1}) % regs[{addr_e}] ({operand2}) = regs[{result_address}] ({result})"
                        ])

            else:
                log_writer.writerow(["UNKNOWN_COMMAND", f"Op code {op_code} at address {instruction_pointer} is not recognized."])

            # Переход к следующей инструкции (шаг на 6 байт)
            instruction_pointer += 6

def save_regs_range(regs, start, end, output_file):
    """Сохранение диапазона регистров в CSV файл."""
    if start < 0 or end >= len(regs) or start > end:
        raise ValueError(f"Invalid register range: start={start}, end={end}, regs size={len(regs)}.")

    with open(output_file, 'w', newline='', encoding='utf-8') as result_file:
        csv_writer = csv.writer(result_file)
        csv_writer.writerow(['Address', 'Value'])  # Заголовок
        for i in range(start, end + 1):
            csv_writer.writerow([i, regs[i]])

    print(f"Regs values from {start} to {end} have been saved to '{output_file}'.")

def main(binary_file, regs_size, output_file, log_file, regs_range_start, regs_range_end):
    """Основная функция для загрузки и выполнения инструкций."""
    binary_data = load_binary(binary_file)
    regs = [0] * regs_size

    execute_instructions(binary_data, regs, log_file)
    save_regs_range(regs, regs_range_start, regs_range_end, output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Interpreter for UVM')
    parser.add_argument('binary_file', help='Path to the binary file (e.g., output.bin)')
    parser.add_argument('regs_size', type=int, help='Size of the regs')
    parser.add_argument('output_file', help='Path to the result file (CSV)')
    parser.add_argument('log_file', help='Path to the execution log file (CSV)')
    parser.add_argument('regs_range_start', type=int, help='Start of regs range to save')
    parser.add_argument('regs_range_end', type=int, help='End of regs range to save')

    args = parser.parse_args()

    try:
        main(args.binary_file, args.regs_size, args.output_file, args.log_file, args.regs_range_start, args.regs_range_end)
    except Exception as e:
        print(f"Error: {e}")
