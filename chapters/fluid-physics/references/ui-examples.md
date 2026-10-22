# Agent recipes: fluid-like UI components

## A. Liquid pill button (metaball visual)

Fidelity: **stylized**. Use 2D distance fields/metaballs + smooth union geometry or SVG Gaussian blur/color matrix with a spring on offset/shape. The goo effect is a contour interpolation and is **not** a real fluid with density, viscosity or surface tension; conserve visual blob area only if intended and if you can measure it. Keyboard focus and `prefers-reduced-motion` must preserve an accessible, conventional button. For minimal UI affordance, choose this rather than an expensive SPH engine.

## B. Water cup progress widget

Fidelity: physically inspired height field. Track fill fraction `f = liquidVolume/containerCapacity` separately from displacement of the free surface. Surface wave uses damped height function whose **spatial mean must remain zero** if fill is fixed. On progress update, change fill level via an explicit inflow volume event; wave motion alone must not permanently change fluid amount. Use a stable linear wave/shallow-water approximation, with damping and boundary reflection appropriate to a 2D cross-section. A sine-wave mask can be a declared artistic approximation.

## C. Swirling ink canvas

Fidelity: numerical approximation for a *contained velocity field with advected dye*, not pouring water. Solve advection/diffusion/force/pressure projection, apply pointer forces with units/proportional timestamps, use wall or periodic boundaries explicitly. Separate tracer opacity from mass; evaluate divergence and dye integral to quantify losses due to semi-Lagrangian advection. Sim resolution affects numerical viscosity; report it.

## D. Pouring and splashing

Fidelity: approximate free-surface fluid. Choose PBF/SPH/FLIP/APIC (or a maintained fluid engine with appropriate guarantees), track masses/colliders, gravity and interface geometry. Droplets can separate and merge; check total fluid volume/mass unless allowed outflow. Collision response with container and moving solids must be coupled, not simply positional clipping. Choose a performance budget for particles, iterations, frame time and mobile fallback.

## E. Evaporating droplet

Fidelity: choose physical vs artistic explicitly. Scientific mode: represent mass `m` [kg], geometry (free sphere or pinned sessile drop), temperature, exposed area, saturation vapor state, `k_m` or a more validated transport model, gas/thermal reservoir, and latent heat. Update `dm/dt` with nonnegative bounds and stop at depletion. Convert mass to geometry, then render. Artistic mode may shrink a blob with a fade **but must say it's a visual metaphor, not evaporation physics**.

## F. Liquid-glass navigation

Fidelity: optical stylization. Use deformable boundary, normals, Fresnel-like reflection and screen refraction if appropriate to the platform; enable fallback for devices without backdrop capture. Don't claim a refractive shader solves flow or rigid/liquid coupling. Avoid hiding semantic labels under distortion.

## Acceptance report template

```text
Component: ...
Phenomenon: ...
Fidelity: ...
Parameters (SI / normalized): ...
Solver: ... timestep ... boundary conditions ...
Conserved budgets: ... measured tolerance ...
Tests actually run: ... results ...
Unsupported phenomena and visual cheats: ...
Performance budget, accessibility fallback: ...
```
