import re


class ConfigParser:
    def __init__(self):
        self.constants = {}
        self.output = {}
        self.context_stack = []  # Стек для поддержки вложенных контекстов

    def parse_input(self, input_text):
        """Главный метод для обработки входного текста"""
        lines = input_text.strip().splitlines()
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue

            # Проверяем константы
            if line.startswith("set "):
                self.handle_set(line)
            elif line == "dict :=":
                self.handle_dict_initialize()
            elif line == "begin":
                self.handle_dict_start()
            elif line == "end":
                self.handle_dict_end()
            elif re.match(r"(\w+) :=\s*", line):  # Проверяем `key_name :=`
                key_match = re.match(r"(\w+) :=\s*", line)
                if key_match:
                    key_name = key_match.group(1)
                    # Проверяем, начинается ли после этой строки блок begin
                    if i + 1 < len(lines) and lines[i + 1].strip() == "begin":
                        self.handle_nested_dict_start(key_name)
                        i += 1  # Пропускаем строку `begin`
                    else:
                        self.handle_assignment(line)
            elif re.match(r"(\w+) := (.+);", line):
                self.handle_assignment(line)
            else:
                raise SyntaxError(f"Unknown syntax or command: {line}")
            i += 1

    def handle_set(self, line):
        """Обработка объявления константы"""
        match = re.match(r"set (\w+) = (\d+);", line)
        if match:
            name, value = match.groups()
            self.constants[name] = int(value)
        else:
            raise SyntaxError(f"Invalid syntax in line: {line}")

    def handle_dict_initialize(self):
        """Инициализация начального словаря при 'dict := '"""
        new_context = {}
        self.context_stack = [new_context]
        self.output["dict"] = new_context

    def handle_dict_start(self):
        """Начало нового блока словаря"""
        new_context = {}
        if self.context_stack:
            self.context_stack[-1]["__context__"] = new_context
        self.context_stack.append(new_context)

    def handle_dict_end(self):
        """Завершение словаря и возврат к предыдущему контексту"""
        if len(self.context_stack) <= 1:
            raise SyntaxError("Unexpected 'end' without a matching 'begin'.")
        self.context_stack.pop()

    def handle_nested_dict_start(self, key_name):
        """Начало вложенного словаря"""
        new_context = {}
        if self.context_stack:
            self.context_stack[-1][key_name] = new_context
        self.context_stack.append(new_context)

    def handle_assignment(self, line):
        """Обработка присваивания и массивов/констант"""
        match = re.match(r"(\w+) := (.+);", line)
        if match:
            key, value = match.groups()
            if value.startswith("#(") and value.endswith(")"):  # Обработка констант
                const_name = value[2:-1]
                if const_name in self.constants:
                    value = self.constants[const_name]
                else:
                    raise ValueError(f"Undefined constant: {const_name}")
            elif re.match(r"\(\{(.+)}\)", value):  # Массив
                array_values = [int(x.strip()) for x in re.findall(r"\d+", value)]
                value = array_values
            else:
                try:
                    value = int(value)
                except ValueError:
                    pass  # Значит строка или другой формат

            if self.context_stack:
                self.context_stack[-1][key] = value
            else:
                raise SyntaxError("No context started for assignments.")
        else:
            raise SyntaxError(f"Invalid assignment syntax in line: {line}")

    def to_toml(self):
        if not list(self.output.keys()):
            return ""
        self.output[list(self.output.keys())[0]] = self.output[list(self.output.keys())[0]]["__context__"]
        """Преобразуем внутренние данные в TOML-совместимый формат"""
        def convert_to_toml(data, prefix=""):
            """Рекурсивная функция для обработки вложенных словарей и их конвертации"""
            output_lines = []
            for k, v in data.items():
                if isinstance(v, dict):
                    # Вложенный словарь
                    output_lines.append(f"[{prefix + k}]")
                    output_lines.extend(convert_to_toml(v, prefix + k + "."))
                elif isinstance(v, list):
                    toml_list = "[" + ", ".join(map(str, v)) + "]"
                    output_lines.append(f"{k} = {toml_list}")
                else:
                    output_lines.append(f"{k} = {v}")
            return output_lines

        toml_output = convert_to_toml(self.output)
        return "\n".join(toml_output)


def main():
    import sys
    print("Введите конфигурацию (для завершения ввода используйте Ctrl+D [UNIX] или Ctrl+Z [Windows]):")

    # Считываем весь текст из стандартного ввода
    input_lines = sys.stdin.read()

    parser = ConfigParser()
    try:
        parser.parse_input(input_lines)
        toml_output = parser.to_toml()
        print("\nВыходной TOML:")
        print(toml_output)
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
