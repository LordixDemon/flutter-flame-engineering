# Idea assessment

[English](#english) | [Русский](#russian)

<a id="english"></a>

## English

Assessment recorded on September 11, 2026.

The idea is useful as a local mechanism for retrieving verifiable context. Its strengths are source and version control, offline access after downloading, reproducible citations, project-specific game examples and predictable updates. A large graph or a long skill does not itself guarantee code quality.

### Existing alternatives

- **Official Flutter/Dart agent skills:** Flutter lists `flutter/agent-plugins`, `dart-lang/skills` and package-skill mechanisms. These provide ready-made instructions for common tasks. [Flutter AI tools](https://docs.flutter.dev/ai/tools).
- **Dart and Flutter MCP:** works with the installed SDK, diagnostics, symbols and a running application. It complements the local index by analyzing the real project. Flutter also describes Developer Knowledge MCP for official documentation search on the same page. [Flutter AI tools](https://docs.flutter.dev/ai/tools).
- **Context7:** provides agents with version-aware documentation and examples by indexing public libraries. [Overview](https://context7.com/docs/overview), [adding libraries](https://context7.com/docs/adding-libraries).
- **Graphify:** was installed in the original development environment and builds graphs over mixed content. It supports exploratory navigation. Its semantic mode needs LLM processing, which requires separate orchestration for automatic updates. [Project](https://github.com/Graphify-Labs/graphify).

Flutter skills already exist, so the idea is not entirely new. The original search did not establish whether the exact combination already existed: local Flutter + Flame release snapshots, a deterministic evidence graph, atomic updates and a skill that checks versions against this index. This is not proof that no equivalent exists.

### Why this approach

SQLite FTS5 handles precise API and terminology queries. The graph connects documentation to source, imports and examples. Preserving exact text and commits takes priority over speculative semantic relations. Updates run without API keys or a continuously running agent.

A vector database, Neo4j or large-scale LLM annotation would add maintenance before a retrieval problem had been measured. They can be evaluated after testing real project queries. The current graph explicitly distinguishes lexical mentions and keyword matches from properties requiring a compiler or behavioral analysis.

### Measuring usefulness

Compare real tasks: whether the correct current API was found, versions matched, citations could be reproduced, code passed analysis and tests, retrieval stayed within a reasonable context budget, and fewer fixes were needed for incorrect APIs. For games, separately measure frame time, input and networking on target devices.

Document and edge counts measure corpus size, not demonstrated code improvement. This version verifies update and evidence-retrieval correctness; a comparative study of generation quality has not been performed.

---

<a id="russian"></a>

## Русский

Проверено 11 сентября 2026 года.

Идея полезна как локальный механизм получения проверяемого контекста. Её сильные стороны — контроль источников и версий, работа офлайн после загрузки, воспроизводимые ссылки, собственные игровые примеры и предсказуемое обновление. Сам по себе большой граф или длинный скилл не гарантирует качества кода.

### Что уже существует

- **Официальные Flutter/Dart agent skills:** Flutter перечисляет репозитории `flutter/agent-plugins` и `dart-lang/skills`, а также механизмы package skills. Это готовые инструкции для типовых задач. [Flutter AI tools](https://docs.flutter.dev/ai/tools).
- **Dart and Flutter MCP:** работает с установленным SDK, диагностикой, символами и запущенным приложением. Он дополняет локальный индекс, потому что анализирует реальный проект. На той же странице Flutter описывает Developer Knowledge MCP для поиска официальной документации. [Flutter AI tools](https://docs.flutter.dev/ai/tools).
- **Context7:** предоставляет агентам документацию и примеры с учётом версий, индексируя публичные библиотеки. [Обзор](https://context7.com/docs/overview), [добавление библиотек](https://context7.com/docs/adding-libraries).
- **Graphify:** уже установлен в этом окружении и строит графы по смешанному корпусу. Он подходит для исследовательской навигации. Его семантический режим требует LLM-обработки, которую нужно отдельно организовать при автоматическом обновлении. [Проект](https://github.com/Graphify-Labs/graphify).

Скиллы Flutter уже есть, поэтому считать идею полностью новой нельзя. В выполненном поиске не установлен факт существования точно такой же комбинации: локальные Flutter + Flame release snapshots, детерминированный evidence graph, атомарное обновление и скилл, который проверяет версии и использует этот индекс. Это не доказательство отсутствия аналогов.

### Почему выбран этот вариант

SQLite FTS5 отвечает на точные запросы по API и терминам. Граф помогает перейти от документации к исходнику, импорту и примеру. Хранение точного текста и commit важнее предположительных семантических связей. Обновление работает без API-ключей и без постоянно запущенного агента.

Векторная база, Neo4j и массовая LLM-разметка добавили бы стоимость сопровождения до появления измеренной проблемы поиска. Их имеет смысл рассматривать после проверки качества на реальных запросах проекта. Текущий граф явно отделяет лексические упоминания и ключевые слова от фактов, требующих компилятора или анализа поведения.

### Как измерять пользу

На реальных задачах сравнивать: найден ли нужный актуальный API; совпадают ли версии; можно ли воспроизвести источник; проходит ли код анализатор и тесты; сколько контекста ушло на поиск; стало ли меньше исправлений из-за неверных API. Для игры отдельно измерять frame time, управление и сетевое поведение на целевых устройствах.

Количество документов и рёбер показывает размер корпуса, а не доказанное улучшение кода. В этой версии проверяется техническая корректность обновления и извлечения доказательств; сравнительное исследование качества генерации ещё не проводилось.
