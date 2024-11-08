## Задача 1
Реализовать на Jsonnet приведенный ниже пример в формате JSON. Использовать в реализации свойство программируемости и принцип DRY.

### Решение.
```
{
  groups: [
    std.join("-", ["ИКБО", std.toString(i), "20"]) for i in std.range(1, 24)
  ],

  students: [
    { age: 19, group: "ИКБО-4-20", name: "Иванов И.И." },
    { age: 18, group: "ИКБО-5-20", name: "Петров П.П." },
    { age: 18, group: "ИКБО-5-20", name: "Сидоров С.С." },
    { age: 20, group: "ИКБО-6-20", name: "Кузнецов К.К." } // новый студент
  ],

  subject: "Конфигурационное управление"
}
```

### Результат.
```
{
  "groups": [
    "ИКБО-1-20",
    "ИКБО-2-20",
    "ИКБО-3-20",
    "ИКБО-4-20",
    "ИКБО-5-20",
    "ИКБО-6-20",
    "ИКБО-7-20",
    "ИКБО-8-20",
    "ИКБО-9-20",
    "ИКБО-10-20",
    "ИКБО-11-20",
    "ИКБО-12-20",
    "ИКБО-13-20",
    "ИКБО-14-20",
    "ИКБО-15-20",
    "ИКБО-16-20",
    "ИКБО-17-20",
    "ИКБО-18-20",
    "ИКБО-19-20",
    "ИКБО-20-20",
    "ИКБО-21-20",
    "ИКБО-22-20",
    "ИКБО-23-20"
  ],
  "students": [
    {
      "age": 19,
      "group": "ИКБО-4-20",
      "name": "Иванов И.И."
    },
    {
      "age": 18,
      "group": "ИКБО-5-20",
      "name": "Петров П.П."
    },
    {
      "age": 18,
      "group": "ИКБО-5-20",
      "name": "Сидоров С.С."
    },
    {
      "age": 20,
      "group": "ИКБО-6-20",
      "name": "Кузнецов К.К."
    }
  ],
  "subject": "Конфигурационное управление"
```
}
## Задача 2
Реализовать на Dhall приведенный ниже пример в формате JSON. Использовать в реализации свойство программируемости и принцип DRY.\

### Решение.
```
let Prelude = https://prelude.dhall-lang.org/v20.2.0/package.dhall
let generateGroup = λ(i : Natural) → "ИКБО-" ++ Prelude.Natural.show i ++ "-20"

in  { groups =
      [ generateGroup 1, generateGroup 2, generateGroup 3, generateGroup 4
      , generateGroup 5, generateGroup 6, generateGroup 7, generateGroup 8
      , generateGroup 9, generateGroup 10, generateGroup 11, generateGroup 12
      , generateGroup 13, generateGroup 14, generateGroup 15, generateGroup 16
      , generateGroup 17, generateGroup 18, generateGroup 19, generateGroup 20
      , generateGroup 21, generateGroup 22, generateGroup 23, generateGroup 24
      ]
    , students =
      [ { age = 19, group = "ИКБО-4-20", name = "Иванов И.И." }
      , { age = 18, group = "ИКБО-5-20", name = "Петров П.П." }
      , { age = 18, group = "ИКБО-5-20", name = "Сидоров С.С." }
      , { age = 20, group = "ИКБО-6-20", name = "Кузнецов К.К." } -- новый студент
      ]
    , subject = "Конфигурационное управление"
 }
```
### Результат.
```
{
  "groups": [
    "ИКБО-1-20",
    "ИКБО-2-20",
    "ИКБО-3-20",
    "ИКБО-4-20",
    "ИКБО-5-20",
    "ИКБО-6-20",
    "ИКБО-7-20",
    "ИКБО-8-20",
    "ИКБО-9-20",
    "ИКБО-10-20",
    "ИКБО-11-20",
    "ИКБО-12-20",
    "ИКБО-13-20",
    "ИКБО-14-20",
    "ИКБО-15-20",
    "ИКБО-16-20",
    "ИКБО-17-20",
    "ИКБО-18-20",
    "ИКБО-19-20",
    "ИКБО-20-20",
    "ИКБО-21-20",
    "ИКБО-22-20",
    "ИКБО-23-20",
    "ИКБО-24-20"
  ],
  "students": [
    {
      "age": 19,
      "group": "ИКБО-4-20",
      "name": "Иванов И.И."
    },
    {
      "age": 18,
      "group": "ИКБО-5-20",
      "name": "Петров П.П."
    },
    {
      "age": 18,
      "group": "ИКБО-5-20",
      "name": "Сидоров С.С."
    },
    <добавьте ваши данные в качестве четвертого студента>
  ],
  "subject": "Конфигурационное управление"
} 
```
## Задача 3
Язык нулей и единиц.
10
100
11
101101
000

### Решение.
```
import random

def parse_bnf(bnf_grammar):
    rules = {}
    for line in bnf_grammar.splitlines():
        if not line.strip():  
            continue
        left, right = line.split("=")
        rules[left.strip()] = [x.strip() for x in right.split("|")]
    return rules

def generate_phrase(rules, start_symbol):
    phrase = [start_symbol]
    while True:
        for i, word in enumerate(phrase):
            if word in rules:
                replacement = random.choice(rules[word])
                phrase[i] = replacement
                break
        else:  
            break
    return ''.join(phrase)

BNF = '''
E = 10 | 100 | 11 | 101101 | 000
'''

rules = parse_bnf(BNF)

for i in range(10):
    print(generate_phrase(rules, 'E'))
```
### Результат.
```
100
10
11
000
101101
10
10
10
11
10
```
## Задача 4
Язык правильно расставленных скобок двух видов.

### Решение.
(({((()))}))
{}
{()}
()
{}

```
BNF = '''
E = "()" | "{}" | E E | "(" E ")" | "{" E "}"
'''

for i in range(10):
    print(generate_phrase(parse_bnf(BNF), 'E'))
```
### Результат.
```
()
{}
()()
{{}}
()()()
{()}
{{()()()()()()}}
{{}}
{()()}
{{()()()()()()}}
```
## Задача 5
Язык выражений алгебры логики.
```
BNF = '''
E = "~" E | E "&" E | E "|" E | "(" E ")" | "x" | "y"
'''

for i in range(10):
    print(generate_phrase(parse_bnf(BNF), 'E'))
```
### Результат.
```
x
~y
x&y
(x|y)
x&(~y)
~(x&y)
y|x
x&x
(~y)&x
(x|(y&~x))
```
