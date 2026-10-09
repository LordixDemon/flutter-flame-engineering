# Flutter / Flame decisions

Consult only the sections relevant to the requested feature. Verify exact APIs in the indexed release or installed package.

## UI and game lifecycle

- Put the game loop and frame state in Flame. Use Flutter for application screens and overlays; send meaningful score/menu/match events to UI state rather than publishing every frame.
- Preserve the game instance across unrelated widget rebuilds. Verify how the project's `GameWidget`, component mounting, asset loading, pause/resume and disposal interact before changing ownership.
- Check whether an API is safe in `onLoad`, `onMount`, `update` or `onRemove` in the current release. Component insertion/removal may be deferred. Do not assume that adding a component makes it mounted immediately.
- Tie listeners, timers, audio and socket subscriptions to their actual owner. Account for backgrounding, interruptions and return to the foreground on mobile.

## Board games and PvP

- For grid-based falling blocks or match-3, model cells, moves, rules and resolution independently of display coordinates and visual deformation.
- If a Rust server is authoritative, it validates commands and owns results/rewards. Immediate client feedback and reconciliation must share a defined protocol, sequencing and reconnect behavior.
- A variable render delta is not by itself a deterministic simulation clock. If prediction/replay requires determinism, define simulation steps, integer state and random-number behavior explicitly. Sharing a seed alone does not synchronize different algorithms.
- Verify rotations, boundaries, cascades, timing and reconnect behavior with meaningful cases. Cosmetic effects should not alter accepted board state.

## Visuals and performance

- Use the simplest asset/animation technique that produces the requested result. Sprite animation, scale/rotation effects, particles and fragment shaders cover different needs; complicated deformations may need authored animations or mesh work.
- Preload assets needed for a match where appropriate. Pool components only if allocation measurements justify it.
- Measure expensive blur, offscreen layers and full-screen effects on target hardware. Flutter rendering backends can differ between mobile and desktop; prove shader compatibility on the requested targets.
- Derive a frame budget from the requested refresh rate: approximately 16.7 ms at 60 Hz or 8.3 ms at 120 Hz. Report measured behavior, not a frame-rate guarantee from engine choice.

## Platforms and purchases

- Desktop export and Steamworks integration are separate checks. Verify the selected binding's target OS, auth tickets, overlay, achievements and purchases that the feature needs.
- Restore/retry flows and server-side entitlement persistence matter for purchases. Verify current store SDK/plugin behavior and implement idempotent fulfillment when applicable.
- Adapt touch, keyboard and pointer controls to the same game rules. Preserve safe areas, readable scaling and accessible UI where relevant.

## Good starting queries

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
