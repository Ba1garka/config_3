# Конфигурационное управление

### Домашнее задание 3

#### Условие задания

Разработать инструмент командной строки для учебного конфигурационного
языка, синтаксис которого приведен далее. Этот инструмент преобразует текст из
входного формата в выходной. Синтаксические ошибки выявляются с выдачей
сообщений.
Входной текст на языке json принимается из файла, путь к которому задан
ключом командной строки. Выходной текст на учебном конфигурационном
языке попадает в стандартный вывод.

Словари:
{
 имя = значение,
 имя = значение,
 имя = значение,
 ...
}

Имена:
[a-z][a-z0-9_]*

Значения:
• Числа.
• Строки.
• Словари.

Строки:
q(Это строка)

Объявление константы на этапе трансляции:
(define имя значение);

Вычисление константы на этапе трансляции:
@[имя]

Результатом вычисления константного выражения является значение.

Дополнения: 

Объявление переменной в которой будет записано текущее время
(define имя значение);

Вычисление переменной в которой будет записано текущее время
q(имя)

Все конструкции учебного конфигурационного языка (с учетом их
возможной вложенности) должны быть покрыты тестами. Необходимо показать 3
примера описания конфигураций из разных предметных областей.

### Функции

1. `format_constants(constants, indent_level=1)`:
   - принимает словарь constants и преобразует его в строку в формате для  конфигурационного языка.

2. `format_value(value, indent_level=1)`:
   - Преобразует заданное значение в строку, которая соответствует формату.
   - Если тип данных не поддерживается, выбрасывает ошибку.

3. `format_dict(d, indent_level=1)`:
   - Обрабатывает словарь d, формируя строки с его содержимым.
   - Проверяет, что имена ключей являются валидными. Если ключ равен constants, то обрабатывает его отдельно, чтобы правильно выставить запятые между константами.

4. `is_valid_name(name)`:
   - Проверяет, является ли имя (строка) валидным: должно начинаться с буквы и может содержать буквы, цифры или символ подчеркивания.
   - Возвращает True, если имя валидно, иначе — False.

5. `json_to_custom_config(json_data)`:
   - Принимает JSON-данные в виде словаря, извлекает из них constants, обрабатывает их через format_constants, а затем формирует остальную часть конфигурации через format_dict.
   - Возвращает итоговую строку, которая содержит как константы, так и остальные данные.

6. `main()`:
   - Проверяет, передан ли путь к JSON-файлу как аргумент командной строки.
   - Открывает файл, загружает JSON данные, обрабатывает их через json_to_custom_config, и выводит результат на экран.
  
### Файл json

![Снимок экрана (177)](https://github.com/user-attachments/assets/c5115c02-706c-44bb-aaf5-15bfaf6b4a09)

### Тестирование

![Снимок экрана (179)](https://github.com/user-attachments/assets/5db82b13-c897-4bfe-bbf2-d4781dffec8a)

![Снимок экрана (187)](https://github.com/user-attachments/assets/ce1be563-7c4c-4720-8c27-c0eaa5c394ea)

