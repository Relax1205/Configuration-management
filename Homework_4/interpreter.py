import argparse

def popcnt(value):
    """Подсчет количества установленных битов (единиц) в числе."""
    return bin(value).count('1')

def interpreter(binary_path, result_path, memory_range):
    memory = [0] * 1024  # Размер памяти
    registers = [0] * 64  # Количество регистров

    with open(binary_path, "rb") as binary_file:
        byte_code = binary_file.read()

    i = 0
    while i < len(byte_code):
        command = byte_code[i] & 0x0F  # Биты 0-3 для команды
        i += 1  # Переход к следующему байту после команды
        
        if command == 6:  # LOAD_CONST
            B = (byte_code[i] << 2) | (byte_code[i+1] >> 6)  # Биты 4-9
            C = ((byte_code[i+1] & 0x3F) << 24) | (byte_code[i+2] << 16) | (byte_code[i+3] << 8) | byte_code[i+4]  # Биты 10-41
            registers[B] = C
            i += 5
        elif command == 10:  # READ_MEM
            B = (byte_code[i] >> 2) & 0x1F  # Биты 4-9
            C = ((byte_code[i] & 0x03) << 20) | (byte_code[i+1] << 12) | (byte_code[i+2] << 4) | (byte_code[i+3] >> 4)  # Биты 10-25
            registers[B] = memory[C]
            i += 5
        elif command == 12:  # WRITE_MEM
            B = ((byte_code[i] << 8) | byte_code[i+1])  # Биты 4-33
            C = (byte_code[i+2] << 8) | byte_code[i+3]  # Биты 34-38
            D = byte_code[i+4]  # Регистр
            memory[B] = registers[D]
            i += 5
        elif command == 14:  # MODULO
            B = byte_code[i]  # Смещение
            C = byte_code[i+1]  # Адрес
            D = byte_code[i+2]  # Адрес регистра
            E = byte_code[i+3]  # Операнд
            memory[C + B] = memory[D] % registers[E]
            i += 5
        else:
            print(f"Неизвестная команда: {command}. Пропускаем...")
            i += 5

    with open(result_path, "w", encoding="utf-8") as result_file:
        result_file.write("Address,Value\n")
        for address in range(memory_range[0], memory_range[1] + 1):
            result_file.write(f"{address},{memory[address]}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Интерпретатор бинарных инструкций для УВМ.")
    parser.add_argument("binary_path", help="Путь к бинарному файлу")
    parser.add_argument("result_path", help="Путь к результатам в CSV файл")
    parser.add_argument("first_index", type=int, help="Первый индекс для отображения памяти")
    parser.add_argument("last_index", type=int, help="Последний индекс для отображения памяти")
    args = parser.parse_args()

    interpreter(args.binary_path, args.result_path, (args.first_index, args.last_index))
