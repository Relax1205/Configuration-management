import csv
import struct
import sys

# Команды виртуальной машины
COMMANDS = {
    "LOAD_CONST": 6,
    "READ_MEM": 10,
    "WRITE_MEM": 12,
    "MODULO": 14
}

def assemble_csv(input_csv, output_file, log_file):
    with open(input_csv, 'r') as infile, open(output_file, 'wb') as binfile, open(log_file, 'w', newline='') as logfile:
        reader = csv.DictReader(infile)
        log_writer = csv.writer(logfile)
        log_writer.writerow(["Command", "Opcode", "Bytes"])

        for row in reader:
            command = row["Command"]
            if command not in COMMANDS:
                raise ValueError(f"Unknown command: {command}")
            
            opcode = COMMANDS[command]

            # Собираем байты команды
            if command == "LOAD_CONST":
                b, c = int(row["Arg1"]), int(row["Arg2"])
                data = struct.pack(">BHI", opcode, b, c)
            elif command == "READ_MEM":
                b, c = int(row["Arg1"]), int(row["Arg2"])
                data = struct.pack(">BHH", opcode, b, c)
            elif command == "WRITE_MEM":
                b, c, d = int(row["Arg1"]), int(row["Arg2"]), int(row["Arg3"])
                data = struct.pack(">BHBB", opcode, b, c, d)
            elif command == "MODULO":
                b, c, d, e = int(row["Arg1"]), int(row["Arg2"]), int(row["Arg3"]), int(row["Arg4"])
                data = struct.pack(">BHBBB", opcode, b, c, d, e)
            else:
                raise ValueError(f"Unknown command: {command}")

            binfile.write(data)
            log_writer.writerow([command, opcode, " ".join(f"{byte:02X}" for byte in data)])

def run_tests():
    tests = [
        {
            "command": "LOAD_CONST",
            "args": (6, 40, 803),
            "expected": b"\x06\x00\x28\x00\x00\x03\x23"
        },
        {
            "command": "READ_MEM",
            "args": (10, 28, 934),
            "expected": b"\x0A\x00\x1C\x03\xA6"
        },
        {
            "command": "WRITE_MEM",
            "args": (12, 46, 31, 60),
            "expected": b"\x0C\x00\x2E\x1F\x3C"
        },
        {
            "command": "MODULO",
            "args": (14, 92, 42, 57, 33),
            "expected": b"\x0E\x00\x5C\x2A\x39\x21"
        }
    ]

    
    for i, test in enumerate(tests, 1):
        command = test["command"]
        args = test["args"]
        expected = test["expected"]

        opcode = COMMANDS[command]
        
        if command == "LOAD_CONST":
            data = struct.pack(">BHI", opcode, args[1], args[2])
        elif command == "READ_MEM":
            data = struct.pack(">BHH", opcode, args[1], args[2])
        elif command == "WRITE_MEM":
            data = struct.pack(">BHBB", opcode, args[1], args[2], args[3])
        elif command == "MODULO":
            data = struct.pack(">BHBBB", opcode, args[1], args[2], args[3], args[4])
        else:
            raise ValueError(f"Unknown command: {command}")
        
        assert data == expected, (
            f"Test {i} failed for {command}. "
            f"Expected: {expected.hex()}, Got: {data.hex()}"
        )
        print(f"Test {i} passed for {command}. Output: {data.hex()}")

if __name__ == "__main__":
    print("Running tests...")
    try:
        run_tests()
        print("All tests passed!")
    except AssertionError as e:
        print(e)
        sys.exit(1)  # Завершаем выполнение, если тесты не проходят
    
    # Если тесты пройдены, выполняем основную функцию
    if len(sys.argv) == 4:
        assemble_csv(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Usage:")
        print("  python assembler.py <input_csv> <output_bin> <log_csv>")
