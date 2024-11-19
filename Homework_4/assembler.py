import struct
import csv
import argparse
import os

def assemble(input_file, output_file, log_file):
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"Input file '{input_file}' not found.")

    binary_instructions = []
    log_entries = [["Command", "A", "B", "C", "D", "E"]]  # Заголовок для log.csv

    def parse_int(value):
        """Вспомогательная функция для безопасного преобразования строки в целое число."""
        try:
            return int(value) if value else 0
        except ValueError:
            return 0

    with open(input_file, 'r', newline='', encoding='utf-8') as infile:
        csv_reader = csv.DictReader(infile)
        for row_number, row in enumerate(csv_reader, start=2):  # Начинаем с 2 для учёта заголовка
            command_field = row.get('Command', '').strip()
            # Пропуск строк-комментариев или пустых строк
            if not command_field or command_field.startswith('#'):
                continue

            command = command_field.upper()
            A = parse_int(row.get('A'))
            B = parse_int(row.get('B'))
            C = parse_int(row.get('C'))
            D = parse_int(row.get('D'))
            E = parse_int(row.get('E'))

            try:
                if command == 'LOAD_CONSTANT':
                    # Команда LOAD_CONSTANT: A=4 бит, B=6 бит, C=32 бит
                    byte1 = 0x86
                    byte2 = ((A & 0xF) << 4) | ((B >> 2) & 0xF)
                    byte3 = ((B & 0x3) << 6) | ((C >> 24) & 0x3F)
                    byte4 = (C >> 16) & 0xFF
                    byte5 = (C >> 8) & 0xFF
                    byte6 = C & 0xFF
                    instruction = struct.pack('>BBBBBB', byte1, byte2, byte3, byte4, byte5, byte6)
                    log_entries.append([command, A, B, C, "", ""])

                elif command == 'READ_MEMORY':
                    # Команда READ_MEMORY: A=4 бит, B=6 бит, C=16 бит
                    byte1 = 0xCA
                    byte2 = ((A & 0xF) << 4) | ((B >> 2) & 0xF)
                    byte3 = ((B & 0x3) << 6) | ((C >> 8) & 0x3F)
                    byte4 = C & 0xFF
                    byte5 = 0x00  # Предполагаем, что поле D не используется
                    byte6 = 0x00
                    instruction = struct.pack('>BBBBBB', byte1, byte2, byte3, byte4, byte5, byte6)
                    log_entries.append([command, A, B, C, "", ""])

                elif command == 'WRITE_MEMORY':
                    # Команда WRITE_MEMORY: A=4 бит, B=6 бит, C=16 бит, D=4 бит
                    byte1 = 0xEC
                    byte2 = ((A & 0xF) << 4) | ((B >> 2) & 0xF)
                    byte3 = ((B & 0x3) << 6) | ((C >> 16) & 0x3F)
                    byte4 = (C >> 8) & 0xFF
                    byte5 = C & 0xFF
                    byte6 = (D & 0xF) << 4
                    instruction = struct.pack('>BBBBBB', byte1, byte2, byte3, byte4, byte5, byte6)
                    log_entries.append([command, A, B, C, D, ""])

                elif command == 'REMAINDER':
                    # Команда REMAINDER: A=4 бит, B=6 бит, C=16 бит, D=4 бит, E=4 бит
                    byte1 = 0xCE
                    byte2 = ((A & 0xF) << 4) | ((B >> 2) & 0xF)
                    byte3 = ((B & 0x3) << 6) | ((C >> 16) & 0x3F)
                    byte4 = (C >> 8) & 0xFF
                    byte5 = C & 0xFF
                    byte6 = ((D & 0xF) << 4) | (E & 0xF)
                    instruction = struct.pack('>BBBBBB', byte1, byte2, byte3, byte4, byte5, byte6)
                    log_entries.append([command, A, B, C, D, E])

                else:
                    raise ValueError(f"Unknown command '{command}' on line {row_number} in input file.")

                binary_instructions.append(instruction)

            except Exception as cmd_error:
                raise ValueError(f"Error processing command '{command}' on line {row_number}: {cmd_error}")

    # Запись бинарных инструкций в output.bin файл
    with open(output_file, 'wb') as outfile:
        for instruction in binary_instructions:
            outfile.write(instruction)

    # Запись log.csv без префиксов
    with open(log_file, 'w', newline='', encoding='utf-8') as logfile:
        csv_writer = csv.writer(logfile)
        csv_writer.writerows(log_entries)

    print(f"Assembling completed. Output binary saved to '{output_file}' and log saved to '{log_file}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Assembler for UVM')
    parser.add_argument('input_file', help='Path to the input source file (CSV)')
    parser.add_argument('output_file', help='Path to the output binary file')
    parser.add_argument('log_file', help='Path to the log file (CSV)')

    args = parser.parse_args()

    try:
        assemble(args.input_file, args.output_file, args.log_file)
    except Exception as e:
        print(f"An error occurred during assembly: {e}")