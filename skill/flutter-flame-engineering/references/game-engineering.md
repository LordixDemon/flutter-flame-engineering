# Flutter / Flame decisions

[English](#english) | [Русский](#russian)

<a id="english"></a>

## English

Consult only the sections relevant to the requested feature. Verify exact APIs in the indexed release or installed package.

### UI and game lifecycle

- Put the game loop and frame state in Flame. Use Flutter for application screens and overlays; send meaningful score/menu/match events to UI state rather than publishing every frame.
- Preserve the game instance across unrelated widget rebuilds. Verify how the project's `GameWidget`, component mounting, asset loading, pause/resume and disposal interact before changing ownership.
- Check whether an API is safe in `onLoad`, `onMount`, `update` or `onRemove` in the current release. Component insertion/removal may be deferred. Do not assume that adding a component makes it mounted immediately.
- Tie listeners, timers, audio and socket subscriptions to their actual owner. Account for backgrounding, interruptions and return to the foreground on mobile.

### Board games and PvP

- For grid-based falling blocks or match-3, model cells, moves, rules and resolution independently of display coordinates and visual deformation.
- If a Rust server is authoritative, it validates commands and owns results/rewards. Immediate client feedback and reconciliation must share a defined protocol, sequencing and reconnect behavior.
- A variable render delta is not by itself a deterministic simulation clock. If prediction/replay requires determinism, define simulation steps, integer state and random-number behavior explicitly. Sharing a seed alone does not synchronize different algorithms.
- Verify rotations, boundaries, cascades, timing and reconnect behavior with meaningful cases. Cosmetic effects should not alter accepted board state.

### Visuals and performance

- Use the simplest asset/animation technique that produces the requested result. Sprite animation, scale/rotation effects, particles and fragment shaders cover different needs; complicated deformations may need authored animations or mesh work.
- Preload assets needed for a match where appropriate. Pool components only if allocation measurements justify it.
- Measure expensive blur, offscreen layers and full-screen effects on target hardware. Flutter rendering backends can differ between mobile and desktop; prove shader compatibility on the requested targets.
- Derive a frame budget from the requested refresh rate: approximately 16.7 ms at 60 Hz or 8.3 ms at 120 Hz. Report measured behavior, not a frame-rate guarantee from engine choice.

### Platforms and purchases

- Desktop export and Steamworks integration are separate checks. Verify the selected binding's target OS, auth tickets, overlay, achievements and purchases that the feature needs.
- Restore/retry flows and server-side entitlement persistence matter for purchases. Verify current store SDK/plugin behavior and implement idempotent fulfillment when applicable.
- Adapt touch, keyboard and pointer controls to the same game rules. Preserve safe areas, readable scaling and accessible UI where relevant.

### Good starting queries

```text
GameWidget lifecycle
onLoad onMount onRemove
ScaleEffect EffectController
SpriteAnimationComponent
ParticleSystemComponent
PostProcess FragmentShader
DragCallbacks KeyboardEvents
RepaintBoundary performance
AppLifecycleListener
breaking changes
```

---

<a id="russian"></a>

## Русский

Читайте только разделы, относящиеся к задаче. Проверяйте точные API в индексированном релизе или установленном пакете.

### Жизненный цикл интерфейса и игры

- Игровой цикл и покадровое состояние размещайте в Flame. Flutter используйте для экранов и оверлеев; передавайте в состояние UI значимые события счёта, меню и матча вместо публикации каждого кадра.
- Сохраняйте экземпляр игры при несвязанных перестроениях виджетов. До изменения владения проверьте взаимодействие `GameWidget`, монтирования компонентов, загрузки ассетов, паузы/возобновления и освобождения ресурсов.
- Проверяйте, где API безопасен в текущем релизе: `onLoad`, `onMount`, `update` или `onRemove`. Вставка и удаление компонентов могут быть отложены; добавленный компонент не обязательно уже смонтирован.
- Привязывайте слушатели, таймеры, аудио и подписки сокетов к их фактическому владельцу. Учитывайте фон, прерывания и возврат приложения на передний план на мобильных устройствах.

### Игры на поле и PvP

- Для падающих блоков и Match-3 моделируйте клетки, ходы, правила и разрешение хода независимо от экранных координат и визуальных деформаций.
- Если Rust-сервер авторитетен, он проверяет команды и определяет результаты/награды. Мгновенный клиентский отклик и согласование состояния должны опираться на определённый протокол, порядок команд и поведение при переподключении.
- Переменный render delta сам по себе не задаёт детерминированные часы симуляции. Если нужны предсказание или повтор, явно определите шаги симуляции, целочисленное состояние и генератор случайных чисел. Один общий seed не синхронизирует разные алгоритмы.
- Проверяйте повороты, границы, каскады, время и переподключение на содержательных случаях. Косметические эффекты не должны менять принятое состояние поля.

### Визуал и производительность

- Выбирайте самый простой способ работы с ассетами и анимацией, обеспечивающий нужный результат. Спрайтовая анимация, эффекты масштаба/поворота, частицы и fragment shaders решают разные задачи; сложные деформации могут потребовать авторских анимаций или сетки.
- При необходимости заранее загружайте ассеты матча. Используйте пулы компонентов только при подтверждённых измерениями затратах на аллокации.
- Измеряйте дорогие размытия, внеэкранные слои и полноэкранные эффекты на целевом оборудовании. Flutter rendering backends могут отличаться между мобильными и настольными платформами; подтверждайте совместимость шейдеров на нужных целях.
- Выводите бюджет кадра из нужной частоты: около 16,7 мс при 60 Гц или 8,3 мс при 120 Гц. Сообщайте измеренное поведение, а не гарантируйте FPS выбором движка.

### Платформы и покупки

- Экспорт на desktop и интеграция Steamworks требуют отдельных проверок. Проверяйте целевую ОС выбранного binding, auth tickets, overlay, достижения и покупки, необходимые функции.
- Для покупок важны восстановление, повторы и серверное хранение прав. Проверяйте актуальное поведение SDK/плагина магазина и при необходимости обеспечивайте идемпотентное выполнение заказа.
- Адаптируйте touch, клавиатуру и указатель к одним игровым правилам. Сохраняйте safe area, читаемый масштаб и доступность интерфейса, где это нужно.

### Начальные запросы

```text
GameWidget lifecycle
onLoad onMount onRemove
ScaleEffect EffectController
SpriteAnimationComponent
ParticleSystemComponent
PostProcess FragmentShader
DragCallbacks KeyboardEvents
RepaintBoundary performance
AppLifecycleListener
breaking changes
```
