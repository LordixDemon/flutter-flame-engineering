# Idea assessment

English | [Русский](ASSESSMENT.ru.md)

Assessment recorded on September 11, 2026.

The idea is useful as a local mechanism for retrieving verifiable context. Its strengths are source and version control, offline access after downloading, reproducible citations, project-specific game examples and predictable updates. A large graph or a long skill does not itself guarantee code quality.

## Existing alternatives

- **Official Flutter/Dart agent skills:** Flutter lists `flutter/agent-plugins`, `dart-lang/skills` and package-skill mechanisms. These provide ready-made instructions for common tasks. [Flutter AI tools](https://docs.flutter.dev/ai/tools).
- **Dart and Flutter MCP:** works with the installed SDK, diagnostics, symbols and a running application. It complements the local index by analyzing the real project. Flutter also describes Developer Knowledge MCP for official documentation search on the same page. [Flutter AI tools](https://docs.flutter.dev/ai/tools).
- **Context7:** provides agents with version-aware documentation and examples by indexing public libraries. [Overview](https://context7.com/docs/overview), [adding libraries](https://context7.com/docs/adding-libraries).
- **Graphify:** was installed in the original development environment and builds graphs over mixed content. It supports exploratory navigation. Its semantic mode needs LLM processing, which requires separate orchestration for automatic updates. [Project](https://github.com/Graphify-Labs/graphify).

Flutter skills already exist, so the idea is not entirely new. The original search did not establish whether the exact combination already existed: local Flutter + Flame release snapshots, a deterministic evidence graph, atomic updates and a skill that checks versions against this index. This is not proof that no equivalent exists.

## Why this approach

SQLite FTS5 handles precise API and terminology queries. The graph connects documentation to source, imports and examples. Preserving exact text and commits takes priority over speculative semantic relations. Updates run without API keys or a continuously running agent.

A vector database, Neo4j or large-scale LLM annotation would add maintenance before a retrieval problem had been measured. They can be evaluated after testing real project queries. The current graph explicitly distinguishes lexical mentions and keyword matches from properties requiring a compiler or behavioral analysis.

## Measuring usefulness

Compare real tasks: whether the correct current API was found, versions matched, citations could be reproduced, code passed analysis and tests, retrieval stayed within a reasonable context budget, and fewer fixes were needed for incorrect APIs. For games, separately measure frame time, input and networking on target devices.

Document and edge counts measure corpus size, not demonstrated code improvement. This version verifies update and evidence-retrieval correctness; a comparative study of generation quality has not been performed.
