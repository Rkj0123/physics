---
name: physics
description: Apply physics principles and validation to code, UI animation, interaction design, simulations, games, and visual effects. Use for gravity, falling/bouncing/dragging objects, rigid-body collisions, fluid flow, water, splashes, viscosity, surface tension, waves, buoyancy, evaporation, condensation, or when physically plausible motion and numerical correctness matter.
license: MIT
metadata:
  version: "0.1.0"
---

# Physics — agent skill

Model before animating. This skill supports **physically grounded** design and implementation, not a guarantee of physically exact results. Never claim a stylized effect is a validated simulation; state approximations, calibration requirements, and uncertainty. Apply the laws for the **chosen model and stated assumptions**, conserve quantities as appropriate, and test rather than merely assert correctness.

## Dispatch: load the relevant chapter

- Gravity, free fall, throw/release gestures, collisions, stacks, rigid body, inertia, momentum, rotational dynamics: read [chapters/gravity-physics/SKILL.md](chapters/gravity-physics/SKILL.md), then its referenced notes as needed.
- Liquids, viscosity, waves, free surfaces, splashing, mixing, droplets, evaporation/condensation, buoyancy: read [chapters/fluid-physics/SKILL.md](chapters/fluid-physics/SKILL.md), then its referenced notes as needed.
- A falling/splashing/evaporating liquid: **load both** chapters. Gravity is a body force on the fluid; do not substitute independent rigid-body particles for a cohesive fluid without disclosing the approximation.
- Beyond these chapters: use the universal workflow; identify missing specialized knowledge and references. Do not pretend this version includes validated electromagnetism, acoustics, thermodynamics in general, quantum mechanics, or other future chapters.

## Mandatory physics workflow

1. **Interpret** the observable behavior and interaction: what moves, deforms, collides, flows, heats, changes phase, or appears to do so? Specify whether the result is educational, physically inspired, real-time interactive, or quantitatively accurate.
2. **Write a model contract**: system boundary, coordinate axes, units, dimensionality, parameters with units, initial conditions, boundary conditions, external inputs, conservation laws, assumptions, and allowable tolerances. Prefer SI in the solver and a documented conversion at the renderer boundary. See [references/model-contract.md](references/model-contract.md).
3. **Select the lowest-fidelity adequate method**, not the flashiest: authored CSS/WAAPI/SVG (explicitly illustrative) → analytic or spring/mass model → rigid-body engine or 2D particle/free-surface method → validated specialized solver. Match the model to the phenomenon; don't call timing curves a gravity solver, metaballs a conserved-volume fluid, or opacity fade evaporation.
4. **Derive or cite the equations** and check dimensions. Define every symbol and sign. Distinguish force, acceleration, velocity, position; mass and volume; dynamic and kinematic viscosity; energy and momentum; temperature and humidity. Treat all numeric material properties as example values unless sourced and unit/temperature conditions are given.
5. **Implement state evolution** with a time-aware integrator and stable numerical controls. Rendering must not determine the physical time step. Handle large frame gaps, high-refresh displays, tab visibility, collisions, and user input. See [references/numerics-and-rendering.md](references/numerics-and-rendering.md).
6. **Verify invariant and limiting cases**: no forces; static equilibrium; frame-rate independence; zero/high viscosity; zero restitution; sealed container; saturation/no net evaporation; input release; resize and orientation changes. Record observable violations, error tolerances, and whether the results are qualitative or quantitative.
7. **Ship accessibly and performantly**: reduced-motion mode, static or semantic fallback, capped work and memory, touch/pointer/keyboard handling, clean unmount, no layout thrash. Unavailable GPU features must degrade gracefully.
8. **Explain fidelity honestly** in the deliverable: `Mode: stylized / physically inspired / numerically simulated / calibrated`; solver and units; assumptions; known omissions; evidence from tests. No unrestricted 'obeys all physics laws' guarantee.

## Physics checks that cannot be skipped

- Physical variables evolve by explicit rules rather than instantaneous arbitrary position resets, **except declared interactions** (drag/teleport/reset) that transfer state through a documented constraint/impulse.
- Dimensional analysis is consistent; CSS pixels are **not** meters and milliseconds are **not** seconds.
- In a closed isolated system, no spontaneous creation of mass/energy/momentum beyond numerical tolerance. External boundaries, damping, heat, evaporation, and user input must be accounted for in budgets.
- Collisions do not inject energy for restitution in `[0,1]` unless a documented external actuator acts. Contact should prevent persistent interpenetration.
- Fluid volume/mass must not randomly disappear in a closed container. If liquid evaporates, transfer its mass to vapor/environment reservoir or explicitly model an **open** system.
- If numerical method or approximations cannot meet the fidelity requested, report the limitation and propose a better engine or scope adjustment.

## Agent response contract

For physics-intensive code, include: **Phenomenon → model and fidelity → assumptions/units → method → invariants/tests → limitations**. Show actual implementation and test results where possible. Do not invent tests or performance measurements.

## Extension policy

New chapters live at `chapters/<chapter-name>/SKILL.md` with spec-valid `name` matching their own folder; update dispatch above, add focused references, tests, and an evaluation case. The root stays a compact router. Nested chapters are **referenced subskills**; not every agent client automatically discovers nested skill folders, so install the root skill and follow its dispatch, or install a chapter separately with an agent installer that supports paths.
