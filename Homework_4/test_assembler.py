import struct
from assembler import COMMANDS

def run_tests():
    tests = [
        {
            "command": "LOAD_CONST",
            "args": (6, 40, 803),
            "expected": b"\x86\x8E\x0C\x00\x00\x00"
        },
        {
            "command": "READ_MEM",
            "args": (10, 28, 934),
            "expected": b"\xCA\x99\x0E\x00\x00\x00"
        },
        {
            "command": "WRITE_MEM",
            "args": (12, 46, 31, 60),
            "expected": b"\xEC\xFA\x78\x00\x00\x00"
        },
        {
            "command": "MODULO",
            "args": (14, 92, 42, 57, 33),
            "expected": b"\xCE\x55\xF3\x10\x00\x00"
        }
    ]
    
    for i, test in enumerate(tests, 1):
        command = test["command"]
        args = test["args"]
        expected = test["expected"]

        opcode = COMMANDS[command]
        
        if command == "LOAD_CONST":
            # A + B + C -> Specific byte encoding logic
            data = struct.pack(">BBBHI", opcode, args[0], args[1], args[2], 0)
        elif command == "READ_MEM":
            # A + B + C -> Specific byte encoding logic
            data = struct.pack(">BBBHH", opcode, args[0], args[1], args[2], 0)
        elif command == "WRITE_MEM":
            # A + B + C + D -> Specific byte encoding logic
            data = struct.pack(">BBBHHB", opcode, args[0], args[1], args[2], args[3], 0)
        elif command == "MODULO":
            # A + B + C + D + E -> Specific byte encoding logic
            data = struct.pack(">BBBHHBB", opcode, args[0], args[1], args[2], args[3], args[4], 0)
        else:
            raise ValueError(f"Unknown command: {command}")
        
        assert data == expected, (
            f"Test {i} failed for {command}. "
            f"Expected: {expected.hex()}, Got: {data.hex()}"
        )
        print(f"Test {i} passed for {command}. Output: {data.hex()}")

if __name__ == "__main__":
    print("Running tests for assembler...")
    try:
        run_tests()
        print("All tests passed!")
    except AssertionError as e:
        print(e)
