import argparse
COMMANDS = {
    "load_const": 6,
    "read_mem": 10,
    "write_mem": 12,
    "modulo": 14
}

def log_operation(log_path, operation_code, *args):
    """Логирование операций в указанный файл"""
    if log_path:
        with open(log_path, "a", encoding="utf-8") as log_file:
            log_file.write(f"A={operation_code}, " + ", ".join(f"Arg{i}={arg}" for i, arg in enumerate(args, start=1)) + "\n")

def serializer(cmd, fields, size):
    """Собирает команду в битовую последовательность"""
    bits = 0
    bits |= cmd  # Вставляем команду в первые 4 бита
    for value, offset in fields:
        bits |= (value << offset)  # Вставляем значения в указанные биты
    return bits.to_bytes(size, "little")

def assembler(instructions, log_path=None):
    """Ассемблирует инструкции в байт-код"""
    byte_code = []
    for operation, *args in instructions:
        if operation == "load_const":
            B, C = args
            # A: биты 0–3, B: 4–9, C: 10–41
            byte_code += serializer(6, ((B, 4), (C, 10)), 6)
            log_operation(log_path, 6, B, C)
        elif operation == "read_mem":
            B, C = args
            # A: биты 0–3, B: 4–9, C: 10–25
            byte_code += serializer(10, ((B, 4), (C, 10)), 6)
            log_operation(log_path, 10, B, C)
        elif operation == "write_mem":
            B, C, D = args
            # A: биты 0–3, B: 4–10, C: 11–16, D: 17–22
            byte_code += serializer(12, ((B, 4), (C, 11), (D, 17)), 6)
            log_operation(log_path, 12, B, C, D)
        elif operation == "modulo":
            B, C, D, E = args
            # A: биты 0–3, B: 4–10, C: 11–16, D: 17–22, E: 23–28
            byte_code += serializer(14, ((B, 4), (C, 11), (D, 17), (E, 23)), 6)
            log_operation(log_path, 14, B, C, D, E)
        else:
            raise ValueError(f"Unknown operation: {operation}")
    return byte_code

def assemble(instructions_path: str, log_path=None):
    """Читает файл инструкций и запускает ассемблирование"""
    with open(instructions_path, "r", encoding="utf-8") as f:
        instructions = [[j if not j.isdigit() else int(j) for j in i.split()] for i in f.readlines()]
    return assembler(instructions, log_path)

def save_to_bin(assembled_instructions, binary_path):
    """Сохраняет скомпилированные инструкции в бинарный файл"""
    with open(binary_path, "wb") as binary_file:
        binary_file.write(bytes(assembled_instructions))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ассемблирование файла инструкций в байт-код.")
    parser.add_argument("instructions_path", help="Путь к файлу инструкций (txt)")
    parser.add_argument("binary_path", help="Путь к бинарному файлу (bin)")
    parser.add_argument("log_path", help="Путь к файлу лога (csv)")
    args = parser.parse_args()

    # Инициализация лога
    with open(args.log_path, "w", encoding="utf-8") as log_file:
        log_file.write("Operation code, Arg1, Arg2, Arg3, Arg4\n")
    
    # Ассемблирование
    result = assemble(args.instructions_path, args.log_path)
    save_to_bin(result, args.binary_path)
