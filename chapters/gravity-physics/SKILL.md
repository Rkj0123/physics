---
name: gravity-physics
description: "Design, implement, and audit gravity-driven physical motion: falling UI cards, thrown elements, drag-and-release inertia, 2D rigid-body collisions, bouncing, stacking, constraints and rotational motion. Use when UI or game objects must accelerate, collide, settle or behave according to mechanics rather than easing curves."
license: MIT
metadata:
  version: "0.1.0"
---

# Chapter: gravity-physics

Purpose: let an agent construct physically *plausible* interactive motion, select a solver, and detect common violations. Read the parent `../../SKILL.md` for the universal model contract and gates when used as a nested chapter. For stand-alone installation, apply those same principles here.

## Pick a model before writing motion code

| Requirement | Minimum appropriate model | Never silently substitute |
| --- | --- | --- |
| One falling decorative icon | Analytic ballistic path or semi-implicit Euler | Arbitrary bounce keyframes claimed as gravity |
| Drag/release chip with walls and one or two contacts | Deterministic rigid-body integration, contact response | Position-only collision without impulse |
| Dense pile of chips, rotations, polygons | Mature 2D contact/constraint engine (e.g., Matter.js / Rapier) | Ad-hoc pairwise velocity inversion |
| 3D objects, high-speed thin impacts, joints | Proper 3D rigid-body/CCD constraint engine | 2D CSS transforms pretending to be 3D mechanics |
| Soft jelly, deforming membranes, liquids | Deformable/continuum or fluid model | Perfectly rigid square bodies |

The solver moves collider state; the renderer follows it. Separate collision shape from visual shadow, blur and DOM bounding box. Choose 2D/3D, position axis and gravity sign explicitly.

## Mechanics, units, and invariants

- Newton's second law: **ΣF = m a**. Translational position `x` [m], velocity `v` [m/s], mass `m` [kg], acceleration `a` [m/s²]. Uniform Earth surface gravity: ~`9.80665 m/s²` downward; for **screen-y-down** use `g_y > 0`. Use a clear `pixelsPerMeter` (e.g. 100 px/m) in the adapter; avoid directly calling `9.81` pixels/frame².
- Unforced ballistic motion, no drag: `y(t)=y0+v0y*t+0.5*g*t²`, `vy(t)=v0y+g*t`. The equation is exact for constant g; numerical integrators have discretization error.
- Momentum `p = m v`; angular momentum `L = I ω` for planar rotation about the center of mass. Applied torque `τ=I α`. Include mass moment of inertia and contact lever arms for rotating bodies.
- Mechanical energy `E = 0.5*m*|v|² + m*g*h + 0.5*I*ω²` in a constant-g conservative idealization; friction and inelastic impacts dissipate **mechanical** energy into unmodeled heat/sound/deformation, not create it. `h` is vertical height **up**, not screen y-down.
- Collision restitution `e = -v_after_normal / v_before_normal` for *relative normal speeds of separating vs approaching bodies*, generally 0 to 1 for passive impacts. **Energy fraction** for a simple fixed-wall normal component is `e²` (not `e`), with other modes/velocities unchanged.
- Normal impulse for two bodies, ignoring spin: `j = -(1+e) * (vB-vA)·n / (1/mA+1/mB)` for approaching velocities; `n` points A→B. Update `vA -= j*n/mA`, `vB += j*n/mB`. Static objects have inverse mass zero; handle zero effective mass. For angular contact use the effective-mass denominator with rotational terms; do not reuse this translational shortcut.
- Friction is **tangential** contact impulse bounded by a Coulomb cone (`|j_t| ≤ μ |j_n|`) with material pairing and static/resting treatment. Air drag is not the same as contact friction and must depend on the declared model (linear or quadratic).
- Gravity exerts acceleration independent of mass in vacuum; make mass affect impulses, inertia and contact behavior, not free fall acceleration in the same field.

## Implementing an honest solver

1. Record the model contract: bounding geometry, initial positions, masses and inertias, gravity vector, contact material coefficients, time units and handling of the pointer.
2. Select a **fixed physics step**, typically `dt=1/120 s` for 2D UI (tune with convergence tests); use wall-clock timestamps just to accumulate elapsed seconds. Use a sensible upper bound on catch-up steps, with a documented pause/discard policy. See [../../references/numerics-and-rendering.md](../../references/numerics-and-rendering.md).
3. For an isolated body under known forces, integrate with semi-implicit Euler `v_next=v+a*dt; x_next=x+v_next*dt` as an elementary baseline. For fast/thin impacts, solve time-of-impact or add CCD; never rely solely on final-position overlap.
4. For multi-body collisions, use a physics engine with contact constraints, sleep/wake behavior, collision layers and collision filtering. A manually reversed `velocity.y` works only for a carefully scoped 1D, immovable-floor teaching toy, not general collisions.
5. Handle contacts: calculate relative velocity at each contact point **including `ω × r`** if rotating; reject separating normals; solve normal/tangent impulses; project excessive penetration; impose stable resting contacts; do not repeatedly bounce a resting object.
6. Pointer interaction: model a cursor joint/kinematic handle while grabbed, or pause body dynamics explicitly. Estimate release velocity from multiple timestamped pointer events, converted from px/s to m/s. Don't set velocity to zero on release unless the UI explicitly requests a dead-stop; report injection from user inputs as external work.
7. For DOM rendering, use translation/rotation transforms derived from solver state. Reconcile container resize by changing bounds consistently; remove forces, RAFs, observers and listeners on unmount. Implement reduced motion and keyboard equivalent for essential tasks.
8. Test with analytical trajectories, passive impacts, resting stacks, rapid motion, pause/resume and 30/60/120/144 Hz display rates.

## Interaction policy

- While held, dragging is an **external actuator**; conservation laws for the free-body system need not hold. On release, transition to dynamic mode once, with the measured or intentionally prescribed velocity. Avoid overwriting the velocity in the next frame.
- For fling gestures, cap release speed when the input stream is unreliable and document the cap. Avoid inferring velocity from a single event or from distance without time.
- Maintain distinct collider boundaries and visible decoration boundaries; prevent out-of-bounds if the component is supposed to be contained.
- Rest state should not jitter or gain energy. Consider sleep thresholds and restitution cutoffs for low-speed impacts; use actual engine features rather than layering arbitrary velocity resets that conceal instability.
- Realistic bounces change with material, speed, orientation and spin; one fixed CSS cubic-bezier curve cannot reproduce all scenarios.

## Engine integration notes

Matter.js is a practical 2D UI option, but its default parameters and time units are **engine-specific**, not automatically SI. Read API docs before mapping meters, seconds, friction coefficients, restitution, engine gravity scale or delta. Do not add another gravity force if the engine already supplies gravity. For Rapier or other engines, confirm timestep, collision layers and CCD features in current official documentation before assuming exact APIs.

## Verification gate

- No-force body: constant velocity; uniform-g displacement approaches analytic `0.5*g*t²` as dt shrinks.
- Equal-mass elastic 1D collision: velocities exchange; momentum and kinetic energy conserved to tolerance.
- Immovable wall with `e=0.6`: rebound normal speed ~0.6 of incident; normal KE ~0.36 under ideal isolated assumptions.
- Body released at zero speed from rest: no spontaneous horizontal speed, no upward gravity.
- Bodies in stable contact: no large persistent overlap or unbounded growing kinetic energy.
- High-speed object: no passing through wall without collision.
- 60 vs 120 Hz renderer: same simulation within specified timestep/test policy.

When the request includes flowing, splashing or evaporating liquid, also read the **fluid-physics** chapter. No rigid-body contact hack is a water model.

See [references/contacts-and-constraints.md](references/contacts-and-constraints.md), [references/ui-motion-patterns.md](references/ui-motion-patterns.md), and [../../references/quality-gates.md](../../references/quality-gates.md).
