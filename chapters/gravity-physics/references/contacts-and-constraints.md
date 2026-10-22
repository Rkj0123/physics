# Gravity: contacts, constraints, solver choice

## 1. Rigid-body state

For a planar rigid body track position `(x,y)` in meters, orientation `θ` in radians, center-of-mass linear velocity `(vx,vy)` m/s, angular velocity `ω` rad/s, mass kg, inertia `I` kg·m², collider geometry, and inverse mass/inertia. Static bodies have inverse mass and inertia zero. If mass is zero, never divide by zero; don't interpret a massless collider as a normal dynamic object.

## 2. Contact kinematics

At contact point `c`, for body `i`: `r_i = c - x_i`, `u_i = v_i + ω_i × r_i`; in 2D `ω × (rx, ry)=(-ω*ry, ω*rx)`. Relative `u_rel = u_B - u_A`. Normal `n` points A→B. `v_n = dot(u_rel,n)`; if `v_n >= 0`, no collision impulse needed **for an isolated separating contact**. Penetration correction may still be needed.

For one scalar normal impulse with both angular terms:

`j_n = -(1+e) * v_n / (invMassA + invMassB + (cross(rA,n)^2)*invIA + (cross(rB,n)^2)*invIB)`

Apply `J = j_n*n`, `v_A -= J*invMassA`, `v_B += J*invMassB`, `ω_A -= cross(rA,J)*invIA`, `ω_B += cross(rB,J)*invIB`. For a real stacked multi-contact solver, run multiple sequential constraint iterations and use bias/position correction appropriately. Do not use this formula alone to implement robust jointed stacks; leverage an engine.

## 3. Friction and restitution

- Restitution is a relative normal **speed ratio**; simple wall-normal kinetic-energy retention is `e²`. `e=1` is ideal lossless normal rebound; `e=0` is no *normal* rebound, not necessarily immediate rest or complete KE loss.
- Tangential impulses oppose relative sliding. Compute contact tangent, effective tangential mass, trial impulse and cap by `μ * j_n` (static vs dynamic coefficients may differ). Sloppy cancellation of tangential velocity can inject spin or violate linear/angular momentum.
- Use restitution threshold under which contact response is non-bouncing to stabilize stacks; rolling resistance/drag must be separately modeled if desired.
- Mass and inertia change collision response. Equal fall acceleration does **not** imply equal impact impulse or angular acceleration.

## 4. Collision detection

- Broad phase (AABB/grid/tree) reduces pair candidates; narrow phase (SAT for convex polygons, circle intersection, etc.) yields contacts/normals. Complex shapes often use compound convex parts.
- Discrete overlap at fixed dt permits tunneling if a small fast body passes completely through another between steps. Use swept shape or CCD/time-of-impact, or smaller adaptive substeps with a verified speed-thickness bound.
- Boundary contact, static obstacles, body-body contact and sleeping states all require testing. When a box changes size, update colliders *and* positions consistently.

## 5. Springs and constraints

Hooke spring: `F = -k(x - x_rest)` along a specified axis, with damping `F_d=-c*v_rel`; `k` N/m, `c` N·s/m. Define anchor, rest length, relative endpoint velocity, and external energy injection. An underdamped spring oscillates and decays; a critically damped system approaches without overshoot in the ideal linear model. For user-facing CSS springs parameters may not be physical units; don't infer them without documentation.

## 6. When to use an engine

Hand-written ballistic demo: fine. A stack of drag-able, rotating DOM cards with walls and varying shapes: use a mature, documented contact solver (Matter.js, Rapier, etc.). Verify engine-specific gravity scale, delta time, friction and sleeping semantics. Preserve accessibility by rendering semantic HTML over or synchronized with simulated bounds.
