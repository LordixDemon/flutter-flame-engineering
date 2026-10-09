# Implementation validation

English | [Русский](VALIDATION.ru.md)

This is a historical validation record from the original implementation, before this repository was extracted. Versions and corpus sizes below apply to that date, not to a fresh clone. Build the current database with `python3 ffkb.py update`.

Performed on September 11, 2026, on macOS arm64.

## Environment

- Flutter was upgraded with `flutter upgrade`: **3.47.4 stable**, commit `9584c6713b324636289d067944a46fd6b49df14b`.
- Bundled Dart: **3.13.3**.
- Flame: **1.38.2**, official release commit `03ca24704cdbeb6f81141f1a676e849aeea65d14`.
- `doctor --strict` confirmed SDK/index and Flame/index agreement in an isolated test project.

## Data and updates

Initial official-source retrieval, an online update and a repeated offline rebuild succeeded.

Validated snapshot: `20260911T204241-7ee3f25b`.

| Metric | Value |
|---|---:|
| Documents / source files | 4,658 |
| Search chunks | 22,268 |
| Nodes | 14,176 |
| Edges with source locations | 71,176 |
| Skipped ambiguous mentions | 10,068 |

The repeated build recognized all 4,658 files as unchanged. It rebuilt the full graph while preserving the last network check time. `update --if-older 24` returned `fresh` without downloading again.

## Automated utility checks

`python3 -W error::ResourceWarning -m unittest discover -s tests -q`: **19 tests passed**.

Checks covered reproducible source text and lines, declarations and imports, ambiguous-symbol omission, changes and deletions, context bounds, safe query handling, graph paths, exact stable release tags, writer locking, preservation after network/export failures, empty sources, skipped files, pubspec.lock parsing, version diagnostics and skill installation with a working wrapper.

Ruff: **All checks passed**. Installed `SKILL.md`: **Skill is valid**, according to the system skill-creator validator.

## Sample queries

For `ScaleEffect`, `GameWidget`, `PostProcess`, `AppLifecycleListener` and `RepaintBoundary`, the defining file appeared among the first five results when constrained to the relevant source. This is a small navigation check for known APIs, not a general retrieval-quality evaluation.

## Flutter API application check

The installed skill retrieved documentation and source for `ScaleEffect`, `EffectController`, `EffectTarget` and `Effect.update`. An isolated package using the Flutter SDK and Flame 1.38.2 was created in `.data/verification/flutter_probe`.

Results:

- `dart format lib test` — completed;
- `flutter analyze` — **No issues found**;
- `flutter test --reporter expanded` — **1 test passed**.

The test checks a landing animation: scale changes to `(1.2, 0.8)` and returns to `(1, 1)`, while component size remains `32 × 32`. This verifies API compatibility and behavior, not visual quality, phone FPS or the complete future game client.
