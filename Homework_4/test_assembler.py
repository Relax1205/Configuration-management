from assembler import serializer

def test_load_const():
    """
    Загрузка константы
    Тест (A=6, B=40, C=803): 
    0x86, 0x8E, 0x0C, 0x00, 0x00, 0x00
    """
    cmd = 6
    fields = ((40, 4), (803, 10))
    size = 6
    bytes = serializer(cmd, fields, size)
    expected = b'\x86\x8E\x0C\x00\x00\x00'
    assert bytes == expected, f"Expected {expected.hex()}, got {bytes.hex()}"
    print("Test LOAD_CONST passed!")


def test_read_mem():
    """
    Чтение значения из памяти
    Тест (A=10, B=28, C=934): 
    0xCA, 0x99, 0x0E, 0x00, 0x00, 0x00
    """
    cmd = 10
    fields = ((28, 4), (934, 10))
    size = 6
    bytes = serializer(cmd, fields, size)
    expected = b'\xCA\x99\x0E\x00\x00\x00'
    assert bytes == expected, f"Expected {expected.hex()}, got {bytes.hex()}"
    print("Test READ_MEM passed!")


def test_write_mem():
    """
    Запись значения в память
    Тест (A=12, B=46, C=31, D=60): 
    0xEC, 0xFA, 0x78, 0x00, 0x00, 0x00
    """
    cmd = 12
    fields = ((46, 4), (31, 11), (60, 17))
    size = 6
    bytes = serializer(cmd, fields, size)
    expected = b'\xEC\xFA\x78\x00\x00\x00'
    assert bytes == expected, f"Expected {expected.hex()}, got {bytes.hex()}"
    print("Test WRITE_MEM passed!")


def test_modulo():
    """
    Бинарная операция: взятие остатка
    Тест (A=14, B=92, C=42, D=57, E=33): 
    0xCE, 0x55, 0xF3, 0x10, 0x00, 0x00
    """
    cmd = 14
    fields = ((92, 4), (42, 11), (57, 17), (33, 23))
    size = 6
    bytes = serializer(cmd, fields, size)
    expected = b'\xCE\x55\xF3\x10\x00\x00'
    assert bytes == expected, f"Expected {expected.hex()}, got {bytes.hex()}"
    print("Test MODULO passed!")


if __name__ == "__main__":
    print("Running tests for UVM assembler...")
    try:
        test_load_const()
        test_read_mem()
        test_write_mem()
        test_modulo()
        print("All tests passed!")
    except AssertionError as e:
        print(e)
