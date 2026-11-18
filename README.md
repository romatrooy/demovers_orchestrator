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
создаёт один узел DAG: он нужен для проверки формата передачи и последующей
интеграции, а не для смысловой декомпозиции сложного требования. Если `--scope`
не указан, демо использует `src/orchestrator`. Идентификаторы по умолчанию —
`demo-spec` и версия `1`.

JSON-вход для режима analysis-package можно загрузить через
`load_analysis_package(path)`. Оба способа приводят данные к `AnalysisPackage`,
который передаётся через `DecompositionService`.
