# 🗂️ ⏲️ 📅 Todozer

[![black](https://github.com/vkostyanetsky/Todozer/actions/workflows/black.yml/badge.svg)](https://github.com/vkostyanetsky/Todozer/actions/workflows/black.yml) [![pytest](https://github.com/vkostyanetsky/Todozer/actions/workflows/pytest.yaml/badge.svg)](https://github.com/vkostyanetsky/Todozer/actions/workflows/pytest.yaml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Консольное приложение для ведения списка задач внутри обычного текстового файла. Основная идея — сократить количество действий, связанных с постановкой и планированием задач. 

Отчасти навеяно [Todo.txt](http://todotxt.org) (но этот проект, по-моему, понесло куда-то не туда). 

Основные возможности: 

- Автоматическое создание регулярных задач
- Вывод списка задач за прошедшие и на будущие дни
- Расчет времени, потраченного на работу над задачами
- Отправка напоминаний о задачах в [Telegram](https://telegram.org)

## Планирование

```commandline
todozer make
```

## Просмотр 

```commandline
todozer show
```

## Будильники 

```commandline
todozer beep
```

## Самопроверки

Поскольку все управление ведется через текстовые файлы, в них относительно легко сделать какие-то ошибки (т.е. нарушить формат так, что Тудузер не сообразит, что делать). Программа умеет находить такие ситуации; для проверки нужно запустить команду: 

```commandline
todozer test
```

Если в файлах найдутся какие-то ошибки, то Тудузер выведет их в виде списка.