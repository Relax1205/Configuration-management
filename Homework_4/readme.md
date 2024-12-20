# Ассемблер и интерпретатор учебной виртуальной машины

## Общее описание
Этот проект реализует ассемблер и интерпретатор для учебной виртуальной машины (УВМ). Ассемблер принимает на вход текстовый файл с исходной программой и генерирует бинарный файл, который может быть выполнен интерпретатором. Интерпретатор выполняет команды УВМ и сохраняет результаты в указанном диапазоне памяти.

## Структура файлов
Проект состоит из следующих файлов:

- `assembler.py`: Содержит реализацию ассемблера.
- `interpreter.py`: Содержит реализацию интерпретатора УВМ.
- `input.txt`: Пример входного текстового файла с командами для ассемблера.
- `output.bin`: Бинарный файл, созданный ассемблером.
- `result_assembler.csv`: Лог-файл, содержащий ассемблированные инструкции в формате CSV.
- `test_result.csv`: Файл с результатами выполнения инструкций интерпретатором. Содержит память после выполнения команд.
- `test_program.csv`: Тестовый файл с программой, выполняющей поэлементное взятие остатка над двумя векторами длины 6. Результат записывается в новый вектор.
- `vector_modulo.py`: Python-скрипт для выполнения теста поэлементного взятия остатка без использования бинарного файла.
- `test_uvm_assembler.py`: Python-скрипт с тестами для инструкций `LOAD_CONSTANT`, `READ_MEMORY`, `WRITE_MEMORY`, и `REMAINDER`.

## Функциональность
Ассемблер поддерживает следующие команды:

- `LOAD_CONSTANT`: Загружает константу в указанный адрес памяти.
- `READ_MEMORY`: Читает значение из памяти.
- `WRITE_MEMORY`: Записывает значение в память.
- `REMAINDER`: Выполняет операцию взятия остатка для двух векторов и записывает результат в новый вектор.

Интерпретатор загружает бинарный файл и выполняет инструкции, сохраняя результаты в памяти.

## Запуск ассемблера и интерпретатора

### Предварительные требования
Убедитесь, что у вас установлен Python 3.x.

### Запуск ассемблера
Для сборки текстовой программы в бинарный файл выполните следующую команду:

```bash
python assembler.py input.csv output.bin result_assembler.csv
```
При успешном выполнении:

Бинарный файл будет сохранен в output.bin.
Лог инструкций сохранится в result_assembler.csv в формате CSV с колонками для каждой инструкции.
Запуск интерпретатора
Для выполнения скомпилированной программы и сохранения результатов в test_result.csv:

```bash
python interpreter.py output.bin <размер_памяти> test_result.csv <начало_диапазона> <конец_диапазона>
```
Например, чтобы выполнить файл output.bin с объемом памяти 18 и сохранить значения с 12 по 17:

```bash
python interpreter.py output.bin test_result.csv 100-150
```
При успешном выполнении:

Интерпретатор загрузит output.bin, выполнит инструкции и запишет лог выполнения в test_result.csv.
Результаты сохраняются в файле test_result.csv в указанном диапазоне.
Запуск тестовой программы vector_modulo.py
Тестовый файл vector_modulo.py предназначен для проверки поэлементного взятия остатка над двумя векторами длины 6 без использования ассемблера и интерпретатора. Чтобы запустить тест:

```bash
python vector_modulo.py
```
Скрипт выполнит операцию взятия остатка и сохранит результаты в remainder_result.csv с колонками Index и Remainder.

Запуск тестов команд в test_uvm_assembler.py
Скрипт test_uvm_assembler.py содержит тесты для команд LOAD_CONSTANT, READ_MEMORY, WRITE_MEMORY, и REMAINDER. Он проверяет правильность формата бинарных инструкций для этих команд.