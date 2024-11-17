def execute_remainder(memory, vector1_start, vector2_start, result_start, length):
    """
    Выполняет элементарную операцию `REMAINDER` для двух векторов,
    записывая результат в память.

    memory: Список, представляющий память.
    vector1_start: Начальный адрес первого вектора.
    vector2_start: Начальный адрес второго вектора.
    result_start: Начальный адрес результата.
    length: Длина векторов.
    """
    for i in range(length):
        # Эмулируем работу команды REMAINDER
        addr_v1 = vector1_start + i
        addr_v2 = vector2_start + i
        addr_res = result_start + i

        operand1 = memory[addr_v1]  # Первый операнд
        operand2 = memory[addr_v2]  # Второй операнд

        if operand2 != 0:
            memory[addr_res] = operand1 % operand2
        else:
            memory[addr_res] = 0  # Если делитель 0, результат 0

        # Логируем операцию
        print(f"REMAINDER: memory[{addr_v1}]={operand1} % memory[{addr_v2}]={operand2} -> memory[{addr_res}]={memory[addr_res]}")


# Инициализация памяти и векторов
memory = [0] * 256  # Эмулируем память размером 256
vector1 = [10, 20, 30, 40, 50, 60]
vector2 = [3, 7, 4, 8, 6, 5]

# Загружаем вектора в память
vector1_start = 0  # Адрес первого вектора
vector2_start = 6  # Адрес второго вектора
result_start = 12  # Адрес результата
length = len(vector1)

# Копируем данные в память
memory[vector1_start:vector1_start + length] = vector1
memory[vector2_start:vector2_start + length] = vector2

# Выполняем поэлементное взятие остатка
execute_remainder(memory, vector1_start, vector2_start, result_start, length)

# Выводим результаты
result_vector = memory[result_start:result_start + length]
print("Vector 1:", vector1)
print("Vector 2:", vector2)
print("Result Vector (Remainders):", result_vector)

# Сохраняем результат в файл
with open("vector_remainder_result.csv", "w") as file:
    file.write("Index, Remainder\n")
    for index, value in enumerate(result_vector):
        file.write(f"{index}, {value}\n")
