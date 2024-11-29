import re

def parse_input(text):
    # Регулярное выражение для поиска массива
    array_pattern = r"\(\s*\{([^\}]+)\}\s*\)"
    array_matches = re.findall(array_pattern, text)

    # Регулярное выражение для словаря
    dictionary_pattern = r"begin\s*\n([\s\S]+?)\s*end"  # Захватываем все, включая пробелы и новые строки
    dict_matches = re.findall(dictionary_pattern, text)

    # Регулярное выражение для поиска объявления констант
    set_pattern = r"set\s+([A-Z]+)\s*=\s*(.+?);"
    set_matches = re.findall(set_pattern, text)

    # Отладочные сообщения для проверки, что правильно извлекаем массивы, словари и константы
    print(f"Arrays found: {array_matches}")
    print(f"Dictionaries found: {dict_matches}")
    print(f"Sets found: {set_matches}")

    # Вернуть найденные элементы в виде структуры данных
    return {
        'arrays': array_matches,
        'dictionaries': dict_matches,
        'sets': set_matches
    }

def generate_toml(parsed_data):
    toml_output = ""

    # Обработка массивов
    if parsed_data['arrays']:
        toml_output += "[arrays]\n"
        for array in parsed_data['arrays']:
            # Разделяем элементы массива и обрабатываем их
            array_values = [value.strip() for value in array.split(',')]
            toml_output += f"array = [{', '.join(array_values)}]\n"

    # Пример конвертации словаря в TOML
    section_count = 1
    for dictionary in parsed_data['dictionaries']:
        toml_output += f"[section{section_count}]\n"  # Задаем уникальный раздел для каждого словаря
        
        # Разделим по строкам, чтобы обработать каждую запись в словаре
        lines = dictionary.splitlines()
        for line in lines:
            line = line.strip()  # Убираем лишние пробелы
            if " := " in line:  # Проверяем наличие разделителя
                name, value = line.split(" := ")
                toml_output += f"{name.strip()} = {value.strip()}\n"
        
        section_count += 1

    # Обработка наборов (констант)
    if parsed_data['sets']:
        toml_output += "\n"  # Добавляем новую строку перед набором
        for name, value in parsed_data['sets']:
            toml_output += f"{name.strip()} = {value.strip()}\n"

    return toml_output

def validate_syntax(text):
    # Проверка на наличие ошибок, например, незакрытые блоки begin/end
    if text.count('begin') != text.count('end'):
        raise SyntaxError("Unmatched 'begin' and 'end' blocks")

if __name__ == "__main__":
    # Пример текста для анализа
    text = """
    begin
        set DB_PORT = "123";

        DB_HOST := "localhost";
        DB_USER := "admin";
        DB_PASSWORD := "secret";
        DB_LOL := #(DB_PORT);
    end
    """

    # Валидируем синтаксис перед анализом
    validate_syntax(text)  # Валидация синтаксиса
    
    # Парсим входной текст
    result = parse_input(text)

    # Выводим результат генерации TOML
    toml_result = generate_toml(result)
    print("Generated TOML:\n")
    print(toml_result)