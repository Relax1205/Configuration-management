import struct
from assembler import COMMANDS

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
    print("Running tests for assembler...")
    try:
        run_tests()
        print("All tests passed!")
    except AssertionError as e:
        print(e)
