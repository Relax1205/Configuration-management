import struct

def test_load_constant():
    # Test for LOAD_CONSTANT: A=6, B=40, C=803, expected output: 0x86, 0x62, 0x28, 0x00, 0x03, 0x23
    A, B, C = 6, 40, 803
    byte1 = 0x86
    byte2 = (A << 4) | ((B >> 4) & 0xF)
    byte3 = B & 0xFF
    byte4 = (C >> 16) & 0xFF
    byte5 = (C >> 8) & 0xFF
    byte6 = C & 0xFF
    result = struct.pack('>BBBBBB', byte1, byte2, byte3, byte4, byte5, byte6)
    expected = bytes([0x86, 0x62, 0x28, 0x00, 0x03, 0x23])
    assert result == expected, f"LOAD_CONSTANT failed: got {result}, expected {expected}"
    print("Test LOAD_CONSTANT passed")

def test_read_memory():
    # Test for READ_MEMORY: A=10, B=28, C=934, expected output: 0xCA, 0xA1, 0x1C, 0x00, 0x03, 0xA6
    A, B, C = 10, 28, 934
    byte1 = 0xCA
    byte2 = (A << 4) | ((B >> 4) & 0xF)
    byte3 = B & 0xFF
    byte4 = (C >> 16) & 0xFF
    byte5 = (C >> 8) & 0xFF
    byte6 = C & 0xFF
    result = struct.pack('>BBBBBB', byte1, byte2, byte3, byte4, byte5, byte6)
    expected = bytes([0xCA, 0xA1, 0x1C, 0x00, 0x03, 0xA6])
    assert result == expected, f"READ_MEMORY failed: got {result}, expected {expected}"
    print("Test READ_MEMORY passed")

def test_write_memory():
    # Test for WRITE_MEMORY: A=12, B=46, C=31, D=60, expected output: 0xEC, 0xC2, 0x2E, 0x00, 0x00, 0xDF
    A, B, C, D = 12, 46, 31, 60
    byte1 = 0xEC
    byte2 = (A << 4) | ((B >> 4) & 0xF)
    byte3 = B & 0xFF
    byte4 = (C >> 16) & 0xFF
    byte5 = (C >> 8) & 0xFF
    byte6 = (C & 0xFF) | ((D & 0xF) << 4)
    result = struct.pack('>BBBBBB', byte1, byte2, byte3, byte4, byte5, byte6)
    expected = bytes([0xEC, 0xC2, 0x2E, 0x00, 0x00, 0xDF])
    assert result == expected, f"WRITE_MEMORY failed: got {result}, expected {expected}"
    print("Test WRITE_MEMORY passed")

def test_vector_remainder():
    # Test for VECTOR_REMAINDER: A=14, B=92, C=42, D=57, E=33, expected output: 0xCE, 0xE5, 0x5C, 0x00, 0x00, 0x2A
    A, B, C, D = 14, 92, 42, 57
    byte1 = 0xCE
    byte2 = (A << 4) | ((B >> 4) & 0xF)
    byte3 = B & 0xFF
    byte4 = (C >> 16) & 0xFF
    byte5 = (C >> 8) & 0xFF
    byte6 = C & 0xFF
    result = struct.pack('>BBBBBB', byte1, byte2, byte3, byte4, byte5, byte6)
    expected = bytes([0xCE, 0xE5, 0x5C, 0x00, 0x00, 0x2A])
    assert result == expected, f"VECTOR_REMAINDER failed: got {result}, expected {expected}"
    print("Test VECTOR_REMAINDER passed")
    
def run_tests():
    print("Running tests...")
    test_load_constant()
    test_read_memory()
    test_write_memory()
    test_vector_remainder()
    print("All tests passed successfully.")

if __name__ == "__main__":
    run_tests()
