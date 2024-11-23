from assembler import assemble_csv
from interpreter import interpret
import csv
import os

def generate_csv_for_modulo(vector1, vector2, input_csv):
    """
    Генерирует CSV-файл с командами для выполнения операции взятия остатка над двумя векторами.
    """
    if len(vector1) != 6 or len(vector2) != 6:
        raise ValueError("Оба вектора должны быть длиной 6.")
    
    with open(input_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Command", "Arg1", "Arg2", "Arg3", "Arg4"])
        
        # Генерация команд для загрузки значений в регистры
        for i in range(6):
            writer.writerow(["LOAD_CONST", i, vector1[i], "", ""])  # vector1 -> Register[i]
            writer.writerow(["LOAD_CONST", i + 6, vector2[i], "", ""])  # vector2 -> Register[i+6]
        
        # Генерация команд для выполнения MODULO
        for i in range(6):
            writer.writerow(["MODULO", i + 12, i, i + 6, i + 6])  # MODULO result -> Memory[i+12]

def read_memory_output(output_csv, memory_range):
    """
    Считывает результаты из файла памяти и возвращает список значений.
    """
    memory_start, memory_end = map(int, memory_range.split("-"))
    results = []
    with open(output_csv, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            address = int(row["Address"])
            if memory_start <= address <= memory_end:
                results.append(int(row["Value"]))
    return results

def main():
    # Входные данные: два вектора
    vector1 = [15, 25, 35, 45, 55, 65]
    vector2 = [5, 10, 7, 6, 4, 8]

    # Файлы
    input_csv = "input_vectors.csv"
    output_bin = "output.bin"
    log_csv = "log.csv"
    memory_dump = "memory_dump.csv"
    memory_range = "12-17"  # Используем адреса 12-17 для записи результатов

    # Генерация CSV для ассемблера
    print("Generating CSV for modulo operation...")
    generate_csv_for_modulo(vector1, vector2, input_csv)

    # Ассемблирование
    print("Assembling commands...")
    assemble_csv(input_csv, output_bin, log_csv)

    # Интерпретация
    print("Interpreting binary file...")
    interpret(output_bin, memory_dump, memory_range)

    # Чтение результата
    print("Reading results from memory...")
    result_vector = read_memory_output(memory_dump, memory_range)

    print("Vector 1:", vector1)
    print("Vector 2:", vector2)
    print("Result Vector:", result_vector)

    # Удаление временных файлов (опционально)
    for file in [input_csv, output_bin, log_csv, memory_dump]:
        if os.path.exists(file):
            os.remove(file)

if __name__ == "__main__":
    main()
