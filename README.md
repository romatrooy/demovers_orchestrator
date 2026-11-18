# Оркестратор

На текущем этапе декомпозицию можно запустить в тестовом режиме без Tracker.
Входом служит текстовый файл с описанием одной задачи; позже этот источник можно
заменить адаптером Tracker, сохранив `AnalysisPackage` как объект для аналитика.

## Формат `analysis-package`

Поля соответствуют модели `AnalysisPackage` в коде:

```json
{
  "specification": {},
  "documents": [],
  "constraints": [],
  "previous_results": [],
  "remarks": []
}
```

`specification` содержит данные утверждённой версии спецификации; `documents` и
`previous_results` — массивы JSON-объектов; `constraints` и `remarks` — массивы
строк. Все пять полей обязательны. Для первой декомпозиции `previous_results`
может быть пустым.

## Демо декомпозиции из TXT

Из корня проекта:

```powershell
$env:PYTHONPATH = "src"
python -m orchestrator.main .\task.txt --scope src/orchestrator/domain --output .\dag.json
```

Можно указать несколько областей через повторный `--scope`. Тестовый аналитик
превращает каждый пункт списка в TXT в отдельную задачу DAG. Это простое правило
разбиения для демо, а не смысловая декомпозиция LLM. Если `--scope` не указан,
демо использует `src/orchestrator`. Идентификаторы по умолчанию — `demo-spec` и
версия `1`.

В тестовом режиме строки списка из TXT превращаются в атомарные задачи. Если
описание содержит требование запускать проверку до Tracker, добавляется
интеграционная задача, зависящая от задач проверок. JSON-вход для режима
analysis-package можно загрузить через `load_analysis_package(path)`. Оба способа
приводят данные к `AnalysisPackage`, который передаётся через `DecompositionService`.

## Демо жизненного цикла

Для показа локальной проверки DAG и цикла с Mock Tracker используется черновик
`data/input_graph.json`:

```powershell
python .\scripts\run_demo.py
```

Скрипт сначала проверяет граф. При ошибке он останавливается до импорта. Валидный
граф передаётся в Mock Tracker, который возвращает `task_id` для каждого
`client_key` и выдаёт задачи, чьи зависимости уже приняты. Оркестратор назначает
заглушку-исполнителя, создаёт попытку и отправляет результат как `complete` или
`fail`. Для непрерывного показа зависимых задач Mock Tracker автоматически
принимает успешный результат; это демо-политика вместо реального human review.

Для демонстрации ошибки валидации:

```powershell
python .\scripts\run_demo.py --input .\data\invalid_graph.json
```

Для демонстрации отказа заглушки-исполнителя на текущем `input_graph.json`:

```powershell
python .\scripts\run_demo.py --fail-task validate-scope
```
