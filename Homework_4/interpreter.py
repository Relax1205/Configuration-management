import argparse
import struct

def execute_command(opcode, args, memory, registers):
    if opcode == 6:  # LOAD_CONST
        B, C = args
        print(f"LOAD_CONST: Регистр {B} = {C}")
        if B < len(registers):  # Проверка, что индекс регистра в допустимом диапазоне
            registers[B] = C
        else:
            print(f"Ошибка: индекс регистра {B} выходит за пределы.")
    
    elif opcode == 10:  # READ_MEM
        B, C = args
        print(f"READ_MEM: Регистр {B} = Память[{C}] = {memory[C]}")
        if B < len(registers) and C < len(memory):  # Проверка индексов
            registers[B] = memory[C]
        else:
            print(f"Ошибка: индекс памяти {C} или регистра {B} выходит за пределы.")
    
    elif opcode == 12:  # WRITE_MEM
        B, C, D = args
        print(f"WRITE_MEM: Память[{B + registers[C]}] = Регистр[{D}] = {registers[D]}")
        if B + registers[C] < len(memory) and D < len(registers):  # Проверка индексов
            memory[B + registers[C]] = registers[D]
        else:
            print(f"Ошибка: индексы памяти или регистров {B}, {C}, {D} выходят за пределы.")
    
    elif opcode == 14:  # MODULO
        B, C, D, E = args
        print(f"MODULO: Память[{B + registers[C]}] = Память[{C + registers[D]}] % Регистр[{E}]")
        if B + registers[C] < len(memory) and D < len(registers) and E < len(registers):
            result = memory[C + registers[D]] % registers[E]
            memory[B + registers[C]] = result
        else:
            print(f"Ошибка: индексы памяти или регистров {B}, {C}, {D}, {E} выходят за пределы.")
    else:
        print(f"Ошибка: неизвестный opcode {opcode} с аргументами {args}")

def interpret(input_file, result_file, memory_range):
    memory = [0] * 1024  # Память, размер 1024 ячейки
    registers = [0] * 64  # Регистр, размер 64 регистра
    
    with open(input_file, 'rb') as infile:
        while True:
            byte = infile.read(1)
            if not byte:
                break
            opcode = ord(byte)
            print(f"Чтение opcode: {opcode}")
            
            # Инициализируем args в зависимости от opcode
            if opcode == 6:  # LOAD_CONST
                args = struct.unpack(">B I", infile.read(5))
            elif opcode == 10:  # READ_MEM
                args = struct.unpack(">B H", infile.read(3))
            elif opcode == 12:  # WRITE_MEM
                args = struct.unpack(">H B B", infile.read(4))
            elif opcode == 14:  # MODULO
                args = struct.unpack(">H B B B", infile.read(5))
            else:
                print(f"Ошибка: неизвестный opcode {opcode}. Пропускаем...")
                continue  # Пропускаем неизвестный opcode
            
            # Выполняем команду
            execute_command(opcode, args, memory, registers)
    
    # Сохраняем память в файл
    with open(result_file, 'w') as outfile:
        outfile.write("Address,Value\n")
        for i in range(memory_range[0], memory_range[1] + 1):
            if i < len(memory):  # Проверка, что индекс памяти в допустимом диапазоне
                outfile.write(f"{i},{memory[i]}\n")
            else:
                print(f"Ошибка: индекс памяти {i} выходит за пределы.")

# Главная функция для запуска интерпретатора
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interpreter for UVM (Virtual Machine).")
    parser.add_argument("input_file", help="Path to the input binary file")
    parser.add_argument("result_file", help="Path to the result CSV file")
    parser.add_argument("start_address", type=int, help="Start address of the memory range")
    parser.add_argument("end_address", type=int, help="End address of the memory range")
    args = parser.parse_args()
    
    interpret(args.input_file, args.result_file, (args.start_address, args.end_address))
