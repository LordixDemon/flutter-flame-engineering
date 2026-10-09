# Flutter + Flame Engineering

[English](#english) | [Русский](#russian)

<a id="english"></a>

## English

A local knowledge base of official Flutter, Dart and Flame materials: updatable source snapshots, full-text search, an evidence graph and a Codex engineering skill.

The application runs on Python 3.11+ with the standard library, Git and SQLite FTS5. Linux and macOS are supported. Run it directly from this checkout; no API keys, LLM calls, database server or Python runtime dependencies are required. Source retrieval needs access to public GitHub repositories; Flame release discovery uses pub.dev.

Both projects are standalone. [Rust Engineering](https://github.com/LordixDemon/rust-engineering) includes its own copy of the common engine, with separate configuration, data and skill instructions.

### Install from GitHub

```bash
git clone https://github.com/LordixDemon/flutter-flame-engineering.git
cd flutter-flame-engineering
python3 ffkb.py install-skill
python3 ffkb.py update
```

The skill source is in `skill/flutter-flame-engineering/`. Its wrapper requires this companion checkout: installation records its path in a local `installation.json`. The `.data/` cache, downloaded upstream sources and local paths are excluded from Git; `update` builds your own database. Run checks without network access:

```bash
python3 -W error::ResourceWarning -m unittest discover -s tests -q
```

### Commands

Run from the `flutter-flame-engineering` directory:

```bash
# Fetch current sources and atomically publish a new snapshot
python3 ffkb.py update

# Refresh when the last source check is older than one day
python3 ffkb.py update --if-older 24

# Rebuild the database and graph from cached sources without network access
python3 ffkb.py rebuild

# Inspect versions, corpus size, changes and source check times
python3 ffkb.py status
python3 ffkb.py doctor --project /path/to/flutter-project --strict

# Find documentation, examples and exact declarations
python3 ffkb.py search 'ScaleEffect EffectController' --source flame
python3 ffkb.py context 'GameWidget lifecycle' --max-chars 12000
python3 ffkb.py related ScaleEffect --source flame --limit 20
python3 ffkb.py path ScaleEffect EffectController
python3 ffkb.py read 'flame:packages/flame/lib/src/effects/scale_effect.dart' --start 1 --lines 100

# Locate the full graph, report and manifest
python3 ffkb.py graph

# Install the skill in the user's Codex skills directory
python3 ffkb.py install-skill

# Verify application behavior with isolated fixtures
python3 -m unittest discover -s tests -v
```

Commands return JSON; update progress goes to stderr. Global options `--data-dir` and `--config` go **before** the subcommand, for example: `python3 ffkb.py --data-dir /tmp/my-kb update`.

`context --max-chars` bounds the evidence text; JSON metadata and URLs are additional. Short English API names and terms work best. A small Russian keyword dictionary is included, but it is not general semantic translation or multilingual search.

### Indexed sources

Configuration is in [sources.json](sources.json).

| Source | Content | Version policy |
|---|---|---|
| flutter/website | Guides, migrations and examples | `main`, rolling documentation |
| flutter/flutter | Framework source with API comments and examples | Latest `stable`, exact commit and matching release tag |
| dart-lang/site-www | Dart language, guidance and examples | `main`, rolling documentation |
| flame-engine/flame | Documentation, core, bridge packages, examples and changelog | Latest stable Flame release from pub.dev, exact Git tag |

The corpus covers the configured official repositories, **not every piece of Flutter knowledge**. Binary images, videos, issue discussions, third-party libraries, Apple/Google/Steam guides and the complete Dart VM/engine are outside its scope. Test and asset directories are excluded. Files larger than 2 MB and unsupported formats are counted as skipped; `skipped.excluded` counts excluded directories. Each source's license is recorded in the manifest; local indexing does not replace its terms.

Add an official repository to `sources.json` with its HTTPS GitHub URL, Git ref, directory paths and file extensions. To pin Flame, replace `@pub-stable:flame` with an exact release tag; Flutter accepts a release tag instead of `stable`. Rebuilding offline after changing a ref is rejected: fetch the corresponding sources first.

Documentation on `main` may be ahead of the installed SDK. A source's Flame version identifies the monorepo snapshot; bridge packages have their own versions in `pubspec.yaml`. `doctor` compares the Flutter commit and the resolved main Flame package version in `pubspec.lock`. Other dependency compatibility requires the project's resolver and analyzer.

### Search and graph

SQLite FTS5 with BM25 first searches for all query terms, then broadens the search. Chunks preserve original source lines. `context` adds graph definitions while bounding the returned text.

The graph contains documents, Dart types and topics. Its relations are:

- `declares`: a lexically identified class, mixin, enum, extension or typedef declaration;
- `imports`, `exports`, `parts`: explicit local Dart links;
- `links_to`: a resolved document link to another indexed file;
- `mentions_symbol`: an unambiguous lexical mention of a known type name;
- `keyword_tag`: an explicit match against a topic dictionary.

Each edge includes its source document, line, excerpt and immutable Git commit URL. Ambiguous names are skipped and counted in the report. Extraction is not a complete Dart AST, type resolver or semantic analysis: it does not prove function calls, execution order, version compatibility or causality. Markdown templates and links requiring website rendering may remain unresolved.

The graph connects guidance to definitions and examples; it complements the documentation text. The full graph is in `graph.json`; bounded `context`, `related` and `path` responses are usually more useful to an agent. This workflow needs neither a visualizer nor a vector database. If real queries reveal full-text retrieval failures, local embeddings can be evaluated separately against those cases.

### Database updates

1. Git updates four sparse checkouts without executing downloaded code. The Flame release tag is resolved through pub.dev.
2. Every file records its SHA-256, source and commit. Additions, modifications and deletions are counted against the previous snapshot.
3. A new SQLite index and graph are built completely in a separate temporary directory. Network retrieval is incremental; index and graph construction is complete and deterministic.
4. SQLite integrity and foreign keys are verified before atomically switching `current.json`.

A network, graph-building or write failure before publication leaves the previous snapshot available. Empty sources and missing configured paths stop the update. A file lock excludes concurrent writers while readers can continue using the old database. Snapshot history is retained; automatic history cleanup and background scheduling are not enabled.

`rebuild` produces a new snapshot but preserves the actual last network check time. `update --if-older` does not check remote releases when the cache is fresh enough. Use plain `update` for an explicit request for the latest version.

Database updates **do not upgrade the SDK or game dependencies**. An authorized environment upgrade uses `flutter upgrade`; dependency changes belong in the Flutter project, with migration review and tests.

### Codex skill

Source: [flutter-flame-engineering](skill/flutter-flame-engineering/SKILL.md). Install with `python3 ffkb.py install-skill`. Once discovered, Codex can select the skill automatically; invoke it explicitly as `$flutter-flame-engineering`.

The installed wrapper records the companion application path in `installation.json`. Set `FFKB_APP_ROOT` after relocating the checkout. For a separate installation, use `python3 ffkb.py install-skill --destination /path/to/skills`: an existing installation must belong to the same application path.

The skill checks sources against the SDK and `pubspec.lock`, retrieves bounded evidence, respects the Flutter/Flame boundary and verifies the result with the analyzer, relevant tests and profiling. It does not promise perfect code or impose one architecture or state-management library on every project.

Read the [idea assessment and alternatives](docs/ASSESSMENT.md) and the [historical validation results](docs/VALIDATION.md).

---

<a id="russian"></a>

## Русский

Локальная база официальных материалов для разработки на Flutter, Dart и Flame: обновляемые исходники, полнотекстовый поиск, граф проверяемых связей и скилл для Codex.

Приложение написано на Python 3.11+ и использует стандартную библиотеку, Git и SQLite с FTS5. Поддерживаются Linux и macOS. Запускается прямо из этой папки, без API-ключей, LLM-запросов, серверов баз данных и установки Python-зависимостей. Для Git нужен доступ к публичному GitHub; для определения релиза Flame — к pub.dev.

Оба проекта самостоятельны. [Rust Engineering](https://github.com/LordixDemon/rust-engineering) содержит собственную копию общего движка; у профилей отдельные настройки, данные и скиллы.

### Установка из GitHub

```bash
git clone https://github.com/LordixDemon/flutter-flame-engineering.git
cd flutter-flame-engineering
python3 ffkb.py install-skill
python3 ffkb.py update
```

Исходник скилла находится в `skill/flutter-flame-engineering/`. Его wrapper
требует этот репозиторий: установка записывает путь к нему в локальный
`installation.json`. Кеши `.data/`, полученные официальные исходники и локальные
пути не публикуются в Git; `update` создаёт собственную базу. Проверки без сети:

```bash
python3 -W error::ResourceWarning -m unittest discover -s tests -q
```

### Команды

Запускать из папки `flutter-flame-engineering`:

```bash
# Скачать актуальные источники и атомарно опубликовать новый снимок
python3 ffkb.py update

# Перед работой: обновить, если последний опрос источников старше суток
python3 ffkb.py update --if-older 24

# Перестроить базу и граф из уже скачанных исходников, без сети
python3 ffkb.py rebuild

# Версии, объём корпуса, изменения и время проверки источников
python3 ffkb.py status
python3 ffkb.py doctor --project /path/to/flutter-project --strict

# Найти документацию, примеры и точные определения
python3 ffkb.py search 'ScaleEffect EffectController' --source flame
python3 ffkb.py context 'GameWidget lifecycle' --max-chars 12000
python3 ffkb.py related ScaleEffect --source flame --limit 20
python3 ffkb.py path ScaleEffect EffectController
python3 ffkb.py read 'flame:packages/flame/lib/src/effects/scale_effect.dart' --start 1 --lines 100

# Показать пути к полному графу, отчёту и манифесту
python3 ffkb.py graph

# Установить скилл в пользовательскую папку Codex
python3 ffkb.py install-skill

# Проверить поведение приложения на изолированных фикстурах
python3 -m unittest discover -s tests -v
```

Вывод команд — JSON, сообщения о ходе обновления идут в stderr. `--data-dir` и `--config` — общие параметры **до** подкоманды. Например: `python3 ffkb.py --data-dir /tmp/my-kb update`.

`context --max-chars` ограничивает объём текста доказательств; JSON-метаданные и URL добавляются сверх него. Для естественных запросов лучше использовать короткие английские API/термины. Есть небольшой словарь русских ключевых слов, но это не полноценный семантический или многоязычный поиск.

### Что собирается

Настройки находятся в [sources.json](sources.json).

| Источник | Содержимое | Версия |
|---|---|---|
| flutter/website | Руководства, миграции, примеры | `main`, rolling docs |
| flutter/flutter | Исходники Flutter framework с API-комментариями и примеры | Последняя `stable`, точный commit и совпавший release tag |
| dart-lang/site-www | Язык Dart, рекомендации и примеры | `main`, rolling docs |
| flame-engine/flame | Документация, ядро, bridge-пакеты, примеры и changelog | Последний stable-релиз Flame с pub.dev, точный Git tag |

Это содержимое настроенных официальных репозиториев, **не все существующие сведения о Flutter**. Бинарные картинки, видео, обсуждения issues, сторонние библиотеки, руководства Apple/Google/Steam и полный Dart VM/engine не входят в корпус. Исключены тестовые/asset-каталоги; файлы более 2 МБ и неподдерживаемые форматы учитываются в пропусках. `skipped.excluded` считает исключённые каталоги. Лицензия каждого источника указана в манифесте; локальное индексирование не заменяет её условия.

Новый официальный репозиторий можно добавить в `sources.json`, указав HTTPS GitHub URL, Git ref, пути каталогов и расширения. Если нужен конкретный Flame-релиз, заменить `@pub-stable:flame` на его точный Git tag. Для Flutter можно указать номер release tag вместо `stable`. Офлайн-перестроение после смены ref не допускается: сначала нужно получить соответствующие исходники.

Руководства на `main` могут быть новее установленного SDK. Номер Flame в источнике относится к снимку монорепозитория; у bridge-пакетов свои номера в `pubspec.yaml`. Команда `doctor` сравнивает Flutter commit и разрешённую версию основного пакета Flame из `pubspec.lock`. Совместимость остальных зависимостей проверяется штатным resolver/analyzer проекта.

### Поиск и граф

Поиск использует SQLite FTS5 с BM25: сначала совпадение всех слов, затем более широкий поиск. Чанки сохраняют строки исходника. `context` дополняет результаты определениями из графа, ограничивая объём текста.

Граф содержит документы, типы Dart и темы. Связи:

- `declares`: лексически найдено объявление class/mixin/enum/extension/typedef;
- `imports`, `exports`, `parts`: явные локальные ссылки Dart;
- `links_to`: разрешённая ссылка из документа на другой индексированный файл;
- `mentions_symbol`: однозначное лексическое упоминание известного имени типа;
- `keyword_tag`: явно помеченное совпадение с тематическим словарём.

Каждое ребро содержит документ, номер строки, выдержку и ссылку на неизменяемый Git commit. Неоднозначные имена пропускаются и считаются в отчёте. Извлечение не является полным Dart AST/type resolution или семантическим анализом: оно не доказывает вызовы функций, порядок исполнения, совместимость версий или причинно-следственные связи. Markdown-шаблоны и ссылки, которые требуют рендеринга сайта, могут остаться неразрешёнными.

Граф помогает перейти от рекомендации к определению и примеру. Он не заменяет текст документации. Полный граф находится в `graph.json`; для агента удобнее ограниченные `context`, `related` и `path`. Визуализатор и векторная база не нужны для этого рабочего процесса. Если появятся доказанные промахи полнотекстового поиска, можно отдельно оценить локальные embeddings на наборе реальных запросов.

### Как обновляется база

1. Git получает изменения четырёх sparse checkout без запуска скачанного кода. Flame release tag разрешается через pub.dev.
2. Для каждого файла сохраняются SHA-256, источник и commit. Считаются добавления, изменения и удаления относительно предыдущего снимка.
3. В отдельной временной папке полностью строятся новый SQLite-индекс и граф. Сетевое получение инкрементальное; построение индекса/графа полное и детерминированное.
4. Проверяются целостность SQLite и внешние ключи. Только затем атомарно переключается `current.json`.

Если сеть, сборка графа или запись завершается ошибкой до публикации, предыдущий снимок остаётся доступен. Пустой источник или исчезнувший настроенный путь останавливает обновление. Файловая блокировка исключает двух одновременных писателей; чтение старой базы продолжает работать. История снимков сохраняется; автоматическое удаление истории и фоновое расписание не включены.

`rebuild` создаёт новый снимок, но сохраняет фактическое время последней сетевой проверки источников. `update --if-older` не проверяет удалённые релизы, если кэш достаточно свежий. Для явного запроса «самая последняя версия» запускайте обычный `update`.

Обновление базы **не обновляет SDK и зависимости игры**. Для разрешённого обновления окружения используется `flutter upgrade`, а зависимости меняются внутри Flutter-проекта с проверкой миграций и тестов.

### Скилл

Исходник: [flutter-flame-engineering](skill/flutter-flame-engineering/SKILL.md#russian). Установка: `python3 ffkb.py install-skill`. После обнаружения скилла Codex сможет выбирать его автоматически; явно вызвать можно как `$flutter-flame-engineering`.

Установленный wrapper хранит путь к приложению в `installation.json`. При переносе папки можно задать `FFKB_APP_ROOT`. Для параллельной установки используйте `python3 ffkb.py install-skill --destination /path/to/skills`: существующая установка должна принадлежать тому же пути приложения.

Скилл сопоставляет источники с SDK и `pubspec.lock`, извлекает небольшие порции доказательств, учитывает границу Flutter/Flame и проверяет итоговый код анализатором, подходящими тестами и профилированием. Он не обещает «идеальный код» и не навязывает всем проектам одну архитектуру или библиотеку управления состоянием.

Оценка идеи и существующие альтернативы: [ASSESSMENT.md](docs/ASSESSMENT.md#russian).

Фактически выполненные проверки, версии SDK и результат теста анимации: [VALIDATION.md](docs/VALIDATION.md#russian).
