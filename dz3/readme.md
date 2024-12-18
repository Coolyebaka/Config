
# Конвертер конфигурационного языка в TOML

Этот проект предоставляет инструмент командной строки на Python, который преобразует конфигурационный язык в TOML. Этот язык поддерживает различные конструкции, такие как комментарии, массивы, словари, константы и многое другое. Инструмент обнаруживает и обрабатывает синтаксические ошибки, предоставляя пользователю информативные сообщения об ошибках.

## Особенности

- **Константы**: Поддержка объявления и вычисления констант на этапе трансляции.
- **Числовые переменные**: поддержка парсинга числовых переменных.
- **Обработка ошибок**: Надежная обработка ошибок при отсутствии атрибутов или неизвестных констант.
- **Тестирование**: Комплексное тестирование с использованием `unittest` для проверки всех конструкций и преобразований.

## Использование

### Установка

Убедитесь, что у вас установлена версия Python 3.7 или выше.

1. Клонируйте этот репозиторий:

    ```bash
    git clone https://github.com/Coolyebaka/Config
    cd Config/dz3
    ```

### Использование инструмента командной строки

Вы можете использовать конвертер, указав путь к XML файлу:

```bash
python main.py
```

Это стандартный ввод и выведет соответствующую структуру на языке TOML в стандартный вывод.

#### Пример

Для файла следующего вида:

```
set HOST = 19216801;
set PORT = 8080;
dict :=
   begin
        server := #(HOST);
        port := #(PORT);
        ssl_enabled := 1;
    end
```

Выходной TOML:
```toml
[dict]
server = 19216801
port = 8080
ssl_enabled = 1
```

### Обработка ошибок

Если в файле учебного конфигуриционного языка содержатся недопустимые структуры или ссылки на неизвестные константы, инструмент выдаст ошибку и предоставит полезное сообщение для выявления проблемы.

## Тестирование

Этот проект использует `unittest` для тестирования. Чтобы запустить тесты:

1. Запустите тесты:

    ```bash
    pytest -m unittest tests/tests.py
    ```

Вы увидите подобный вывод:

```bash
..
----------------------------------------------------------------------
Ran 2 tests in 0.000s

OK
```

## Примеры конфигураций

Ниже приведены примеры конфигураций учебного языка из разных предметных областей, которые можно использовать с этим инструментом.

### Конфигурация веб-сервера

**Входной учебный язык:**

```
set HOST = 19216801;
set PORT = 8080;
dict :=
   begin
        server := #(HOST);
        port := #(PORT);
        ssl_enabled := 1;
    end
```

**Конвертированный вывод TOML:**

```toml
[dict]
server = 19216801
port = 8080
ssl_enabled = 1
```
**Входной учебный язык:**

```
set DB_PORT = 5432;
set DB_USER = 1;
set DB_PASS = 12345678;

dict :=
    begin
        port := #(DB_PORT);
        credentials :=
            begin
                users := ({12, 32, 4354, 43});
                user := #(DB_USER);
                password := #(DB_PASS);
            end
    end
```

**Конвертированный вывод TOML:**

```toml
Выходной TOML:
[dict]
port = 5432
[dict.credentials]
users = [12, 32, 4354, 43]
user = 1
password = 12345678
```