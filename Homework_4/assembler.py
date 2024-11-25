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

            print(f"Command: {command}, Opcode: {opcode}, Data: {data}")  # Debug print
            binfile.write(data)
            log_writer.writerow([command, opcode, " ".join(f"{byte:02X}" for byte in data)])

if __name__ == "__main__":
    assemble_csv(sys.argv[1], sys.argv[2], sys.argv[3])
    print("Assembler save data")
