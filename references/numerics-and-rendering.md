# Time stepping, rendering, events, performance

## Frame rate is not simulation rate

`requestAnimationFrame()` timestamps are in milliseconds; elapsed time must be converted to seconds. Simulation clock should use a fixed step (e.g. `1/120 s`) with an accumulator, clamp *incoming wall-clock pause* and cap substeps. A cap avoids runaway work but drops/degrades real elapsed time; state the behavior (pause, slow motion, or resynchronize). Test at 30, 60, 120 and 144 Hz. Never integrate `x += speed` without delta time.

```ts
const fixedDt = 1 / 120;          // seconds
const maxFrame = 0.10;            // seconds, explicit pause policy
const maxSubsteps = 12;
let accumulator = 0;
let lastMs: number | undefined;
function frame(nowMs: number) {
  if (lastMs !== undefined) {
    accumulator += Math.min(Math.max(0, (nowMs - lastMs) / 1000), maxFrame);
    let steps = 0;
    while (accumulator >= fixedDt && steps < maxSubsteps) {
      simulate(fixedDt);
      accumulator -= fixedDt;
      steps++;
    }
    if (steps === maxSubsteps && accumulator >= fixedDt) {
      // Drop accumulated lag explicitly; do not silently claim real-time fidelity.
      accumulator = accumulator % fixedDt;
    }
    render(accumulator / fixedDt); // use stored prior/current states to interpolate
  }
  lastMs = nowMs;
  requestAnimationFrame(frame);
}
```

Actual components must cancel the scheduled frame on unmount, detach listeners, and guard against starting duplicate loops. Pause or reset `lastMs` on visibility change so background pauses do not turn into giant impulses; account for React StrictMode mount/unmount behavior. Use per-frame interpolation only if two previous simulation states exist.

## Integration and accuracy

- Semi-implicit Euler (`v += a*dt; x += v*dt`) is a common baseline for dynamics and is preferable to explicit position-first Euler for many mechanical systems. It is **not an unconditional guarantee** of accuracy or stability.
- Solver parameters and timesteps matter. Stiff springs, fast collisions and fluid advection may need substeps, constraint solvers, implicit schemes or CCD. Decreasing `dt` and checking convergence is a basic validation.
- Numerical damping may dissipate energy; never label it a physical viscosity or friction value without mapping units/models.
- Semi-Lagrangian advection can remain bounded yet be diffusive and non-conservative. “Stable” is not equivalent to “accurate,” “mass-conserving,” or “CFL-free for the entire solver.”

## UI bridge

- Physics state is independent of React re-rendering frequency; render by canvas/WebGL or transforms as appropriate, keep semantic HTML controls accessible.
- Convert SI to CSS px only in rendering/input adapters; recompute offsets on resize; consider DPR, zoom and bounding rect.
- Derive velocity from timestamped pointer samples (px/s converted to m/s); clamp impossible spikes, handle `pointercancel`, `pointerup`, viewport leave, keyboard interaction, and touch behavior.
- Prefer transforms instead of repeatedly writing `top`/`left` and forcing layout. Define collision geometry separately from shadow/glow visual geometry.
- `prefers-reduced-motion`: offer static state or a slower/minimal non-parallax interaction without hiding essential information. Ensure keyboard users have functional alternatives.
- Profile allocation, GPU memory, texture resolution and render loops, particularly mobile and hidden tabs. Explicitly cap particles and iterations. Unmount all observers and WebGL buffers/targets.

Sources: MDN requestAnimationFrame https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame ; MDN reduced motion https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion .
