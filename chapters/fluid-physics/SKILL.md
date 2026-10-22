---
name: fluid-physics
description: Reason about and build physics-informed fluid UI, liquids, droplets, splashes, waves, mixing, viscosity, surface tension, buoyancy and evaporation or condensation. Use when creating water, honey, oil, mercury-like, ink-flow, wave or liquid-glass effects that need an explicit physical model and honest fidelity label, including mass and heat accounting for phase changes.
license: MIT
metadata:
  version: "0.1.0"
---

# Chapter: fluid-physics

Purpose: teach the agent to select a scientifically appropriate **fluid model**, not just a liquid appearance. Start from the umbrella [../../SKILL.md](../../SKILL.md) workflow when nested; for standalone use, write equivalent assumptions/units/invariant checks. **No general-purpose realtime UI solver is accurate for every liquid/material, scale, surface, temperature or regime.** State the model, discretization and unsupported phenomena.

## Choose the phenomenon, then select a model

| Requested behavior | Appropriate starting model | Do not imply |
| --- | --- | --- |
| Gooey, merging UI button | Metaballs, SVG filter, or implicit surface + spring dynamics (**stylized**) | No implicit real mass, capillary dynamics or droplet breakup |
| Flat water ripple on touch | Damped 2D wave/shallow-water approximation | Full 3D free-surface Navier–Stokes |
| Swirling dye/smoke in contained 2D domain | Incompressible Eulerian velocity grid, semi-Lagrangian advection, pressure projection | Automatic sharp **water-air free surface** or conserved dye mass |
| Pouring, free-surface pool, splitting/splashing drops | Particle-based SPH/PBF or grid FLIP/APIC with liquid-air interface tracking | Simple colorful dye grid is enough |
| Small droplets on a surface | Capillarity, wetting/contact angle, gravity + evaporation boundary | All droplets are spherical, perfectly elastic blobs |
| Honey vs water viscosity | Non-Newtonian/temperature-dependent model **if needed**; Newtonian as qualified simplification | Arbitrary shader smoothness equals physical viscosity |
| Water evaporating/condensing | Coupled mass + energy exchange with ambient vapor, geometry and gas conditions | Alpha fade is evaporation or rendered steam is invisible vapor |
| Real material/engineering prediction | Calibrated CFD/thermal solver with experimental validation | Browser particle toy is quantitative |

See [references/governing-equations.md](references/governing-equations.md), [references/interfaces-and-materials.md](references/interfaces-and-materials.md), and [references/phase-change.md](references/phase-change.md). Combine with gravity chapter for moving rigid containers, buoyant rigid objects and fluid-solid collision coupling.

## Core science (know which assumptions permit each equation)

For a single-phase incompressible **Newtonian**, homogeneous fluid of constant density `ρ`:

`∂u/∂t + (u·∇)u = -(1/ρ)∇p + ν∇²u + f` and `∇·u=0`.

- `u`: velocity [m/s], `p`: pressure [Pa], `ρ`: density [kg/m³], `ν=μ/ρ`: kinematic viscosity [m²/s], `μ`: dynamic viscosity [Pa·s], `f`: total body acceleration [m/s²], including gravity. Define axes; with screen-y-down `g_y > 0`.
- `∇·u=0` enforces volume incompressibility **within the fluid**. The PDE alone does not set a moving water-air boundary, phase changes, capillary force, bubbles, turbulence closure, or wall conditions.
- For a free surface, track fluid-air interface and correct fluid stresses: pressure jump across interface depends on surface tension and curvature. Droplet merging/splitting requires topology change; a metaball *rendering* does not automatically update physical fluid mass or momentum.
- Buoyancy: displaced-fluid force magnitude `ρ_fluid*g*V_displaced` upward in a uniform gravitational field for a hydrostatic fluid. A floating rigid object also needs collision/drag/pressure coupling; do not apply a constant arbitrary upward animation.
- For waves, a linearized height-field wave equation or shallow-water equations can suffice **only** when depth, amplitudes, breaking and dispersion are compatible with their assumptions. Wave decay represents damping; capillary effects may matter for small wavelengths.
- For mixture appearance, distinguish passive **advection** of dye by velocity from molecular **diffusion** down concentration gradients. A colorful blend is not evidence that species mass is conserved.

## Fluid workflow (mandatory)

1. **Declare phases and boundaries**: water/air? liquid/vapor? closed tank/open top? Does water contact a wall? Is the free surface tracked? Identify initial volume, density, temperature, ambient humidity, container geometry and external forcing.
2. **Classify regime**, using characteristic size `L`, velocity `U`, `ρ`, `μ`, surface tension `γ`: Reynolds `Re=ρUL/μ` (inertia vs viscosity); Weber `We=ρU²L/γ` (inertia vs capillarity); Bond `Bo=Δρ*g*L²/γ` (gravity vs surface tension, using relevant density difference). These indicate importance, not a magic threshold that picks a universal solver. Do not invent numeric properties/ambient conditions.
3. **State fidelity**: visual illusion / reduced-order height field / discretized fluid solver / validated experiment. UI may choose a lower-cost model, but must describe what it omits.
4. **Implement and boundary-condition correctly**: velocity advection → viscosity/diffusion if modeled → external forces → pressure projection for an incompressible grid. Track fluid-air interface and boundary fluxes separately for water surfaces. Add emission/sinks only with an accounted reservoir. Substep/adapt as needed; use convergence and CFL-style checks appropriate to *each stage* (pressure, advection, waves, particles).
5. **Couple interaction**: pointer injects an impulse/force with explicit time scale and position, not arbitrary displaced dye; draggable solid surfaces impose fluid boundaries or approximation. For liquids in moving UI containers, include accelerated reference frames/inertial forces or approximate with a labeled method.
6. **Mass/energy budgets**: `initial mass + inflow - outflow - evaporation + condensation = current liquid mass` (with sign conventions consistent). A phase-change system should also track vapor species mass where within system; evaporation requires latent heat for thermal fidelity. A constant RGB alpha decrease is illustrative only.
7. **Validate**: still water under gravity at rest, stable no-flux boundary, conserved mass without open sources, grid/refinement test, expected viscosity ordering, droplet breakup/contact angle only if your solver models them, sensible thermal/ambient limits. Try open vs closed container and saturated vs unsaturated ambient.
8. **Render efficiently**: choose SVG for simple blobs, canvas for particles, WebGL/WebGPU for many solver cells; separate solver buffers from render textures, cap iterations/resolution and memory, and implement motion accessibility.

## Important caveats

- The appearance of 'liquid glass' generally models **optics** (refraction, reflection, translucency), not flow; don't claim the glass itself is liquid. Refractive optical effects need surface normal, refractive index, lighting assumptions, and compositor support; distortion filters alone are stylized.
- Mercury is toxic; use it only as a *visual material reference* here. High surface tension and contact angle strongly affect droplet behavior. Do not make safety or real-material predictions from aesthetic shader parameters.
- Evaporation can occur below boiling. Evaporation rate depends on exposed area, vapor concentration gradient, mass transfer, temperature and available energy. At **isothermal vapor-liquid equilibrium**, net transfer tends to zero. Water vapor is invisible; fog/mist and condensation droplets scatter light and become visible.
- Cooling, phase change and non-Newtonian rheology need additional equations. Honey is often approximately Newtonian for many circumstances but strong temperature dependence matters; do not universally equate high viscosity with shear-thinning.
- An incompressible 2D stable-fluid solver with colorful density textures is usually **not** a model of pouring water with a free surface. Do not label it as such.

## UI patterns, examples, evaluation

- Merging blob button → low-cost metaball field with *declared visual illusion*, no conservation assertion.
- Rippling progress glass → 1D/2D height-field for small oscillations, track fill **volume** separately; wave motion should not change average fill permanently in closed container.
- Ink brush → semi-Lagrangian 2D velocity+dye grid; document advection diffusion and mass loss due to numerics, boundaries and resolution.
- Pouring water → SPH/PBF or FLIP/APIC with splash and free surface if required, not a dye shader; cap density/volume error and particle count.
- Evaporating droplet → geometry-based liquid mass change and open-system vapor flux, plus latent heat/saturation if temperature dependent; never simply fade alpha and claim evaporation.

Read [references/governing-equations.md](references/governing-equations.md), [references/interfaces-and-materials.md](references/interfaces-and-materials.md), [references/phase-change.md](references/phase-change.md), [references/ui-examples.md](references/ui-examples.md), and [../../references/quality-gates.md](../../references/quality-gates.md) as relevant. Run tests and communicate all limitations.
