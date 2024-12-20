# Конвертер конфигурации

## Общее описание
Этот проект реализует конвертер, который преобразует XML-файлы в учебный конфигурационный язык. Он позволяет пользователям определять переменные, константы и массивы в формате XML, который затем преобразуется в удобочитаемый формат, используемый для учебных целей.

## Структура файлов
Проект состоит из следующих файлов:
- `config_language.py`: Содержит реализацию конвертера, включая классы и функции для обработки XML.
- `input.xml`: Пример входного XML-файла для тестирования конвертера.
- `output.txt`: Файл для записи результата преобразования.
- `test_config_language.py`: Содержит тесты для проверки функциональности конвертера.
- `README.md`: Документация проекта.

## Функциональность
Конвертер поддерживает следующие элементы XML:
- `variable`: Определяет переменную, которая будет преобразована в строку формата `var NAME := VALUE;`.
- `constant`: Определяет константу, которая будет преобразована в строку формата `(define NAME VALUE)`.
- `array`: Определяет массив значений, который будет преобразован в строку формата `<< VALUE1, VALUE2, ... >>`.

### Пример XML
```xml
<root>
    <constant name="PI">3.14</constant>
    <variable name="MY_VAR">42</variable>
    <array>
        <value>1</value>
        <value>2</value>
        <value>3</value>
    </array>
</root>
```

### Запуск конвертера
Чтобы запустить эмулятор оболочки, выполните следующую команду:
```bash
python config_language.py input.xml output.txt
```

### Результаты тестирования
![Скриншот результата](photo/Снимок%20экрана%202024-10-24%20201726.png)