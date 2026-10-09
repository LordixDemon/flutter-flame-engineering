# Flutter + Flame Engineering

English | [Русский](README.ru.md)

A local knowledge base of official Flutter, Dart and Flame materials: updatable source snapshots, full-text search, an evidence graph and a Codex engineering skill.

The application runs on Python 3.11+ with the standard library, Git and SQLite FTS5. Linux and macOS are supported. Run it directly from this checkout; no API keys, LLM calls, database server or Python runtime dependencies are required. Source retrieval needs access to public GitHub repositories; Flame release discovery uses pub.dev.

Both projects are standalone. [Rust Engineering](https://github.com/LordixDemon/rust-engineering) includes its own copy of the common engine, with separate configuration, data and skill instructions.

## Install from GitHub

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

## Commands

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

## Indexed sources

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

## Search and graph

SQLite FTS5 with BM25 first searches for all query terms, then broadens the search. Chunks preserve original source lines. `context` adds graph definitions while bounding the returned text.

The graph contains documents, Dart types and topics. Its relations are:

- `declares`: a lexically identified class, mixin, enum, extension or typedef declaration;
- `imports`, `exports`, `parts`: explicit local Dart links;
- `links_to`: a resolved document link to another indexed file;
- `mentions_symbol`: an unambiguous lexical mention of a known type name;
- `keyword_tag`: an explicit match against a topic dictionary.

Each edge includes its source document, line, excerpt and immutable Git commit URL. Ambiguous names are skipped and counted in the report. Extraction is not a complete Dart AST, type resolver or semantic analysis: it does not prove function calls, execution order, version compatibility or causality. Markdown templates and links requiring website rendering may remain unresolved.

The graph connects guidance to definitions and examples; it complements the documentation text. The full graph is in `graph.json`; bounded `context`, `related` and `path` responses are usually more useful to an agent. This workflow needs neither a visualizer nor a vector database. If real queries reveal full-text retrieval failures, local embeddings can be evaluated separately against those cases.

## Database updates

1. Git updates four sparse checkouts without executing downloaded code. The Flame release tag is resolved through pub.dev.
2. Every file records its SHA-256, source and commit. Additions, modifications and deletions are counted against the previous snapshot.
3. A new SQLite index and graph are built completely in a separate temporary directory. Network retrieval is incremental; index and graph construction is complete and deterministic.
4. SQLite integrity and foreign keys are verified before atomically switching `current.json`.

A network, graph-building or write failure before publication leaves the previous snapshot available. Empty sources and missing configured paths stop the update. A file lock excludes concurrent writers while readers can continue using the old database. Snapshot history is retained; automatic history cleanup and background scheduling are not enabled.

`rebuild` produces a new snapshot but preserves the actual last network check time. `update --if-older` does not check remote releases when the cache is fresh enough. Use plain `update` for an explicit request for the latest version.

Database updates **do not upgrade the SDK or game dependencies**. An authorized environment upgrade uses `flutter upgrade`; dependency changes belong in the Flutter project, with migration review and tests.

## Codex skill

Source: [flutter-flame-engineering](skill/flutter-flame-engineering/SKILL.md). Install with `python3 ffkb.py install-skill`. Once discovered, Codex can select the skill automatically; invoke it explicitly as `$flutter-flame-engineering`.

The installed wrapper records the companion application path in `installation.json`. Set `FFKB_APP_ROOT` after relocating the checkout. For a separate installation, use `python3 ffkb.py install-skill --destination /path/to/skills`: an existing installation must belong to the same application path.

The skill checks sources against the SDK and `pubspec.lock`, retrieves bounded evidence, respects the Flutter/Flame boundary and verifies the result with the analyzer, relevant tests and profiling. It does not promise perfect code or impose one architecture or state-management library on every project.

Read the [idea assessment and alternatives](docs/ASSESSMENT.md) and the [historical validation results](docs/VALIDATION.md).
