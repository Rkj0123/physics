# Model contract and fidelity declaration

Before writing physics code, create a compact contract in code comments or a short design note:

```yaml
phenomenon: falling, colliding tags
fidelity: physically-inspired 2D rigid bodies
space: 2D, positive x right, positive y down
units: solver = m, kg, s; renderer = CSS px
scale: 100 px/m at current container scale
bodies: masses, shape/collider, moments of inertia, restitution, friction
forces: gravity = [0, 9.80665] m/s^2, plus pointer impulses
initial: positions, velocities, spin
boundaries: static box floor and walls; no tunneling target
integration: fixed 1/120 s; solver with collision substeps or CCD
conservation: horizontal momentum except contacts/damping/input; mechanical energy nonincreasing during passive impacts
known omissions: air drag, deformation, heat, depth
acceptance: stable stacks; release velocity; 60/120Hz comparable; no severe penetration
```

For fluids include: phase(s), density ρ, dynamic viscosity μ or kinematic ν, surface tension γ, gravity, temperature, ambient humidity and pressure (if phase change), solver cells or particles, interface and wall boundary conditions, mass/volume budget, and whether a reservoir is open or closed.

## Four fidelity levels

1. **Stylized:** art-directed paths/easing/shaders; do *not* claim governing equations were solved. Use for lightweight decoration.
2. **Physics-inspired:** a reduced-order model (springs, blobs, analytic trajectory, approximate wave), truthful within its explicit assumptions; not suitable for quantitative measurement.
3. **Numerically simulated:** solve a defined physical model, measure discretization error and constraints; provide time step, solver and residual budgets.
4. **Calibrated/validated:** compare against analytic, experimental or trusted reference data under matching material/boundary conditions; report ranges of validity and measurement uncertainty.

A shader's visual realism does not move it into level 3 or 4 by itself.

## Dimensional and sign checks

- `[x]=m`, `[v]=m/s`, `[a]=m/s²`, `[F]=N=kg·m/s²`.
- `[ρ]=kg/m³`, `[μ]=Pa·s`, `[ν]=m²/s`, `[γ]=N/m`, `[p]=Pa`, `[Q]=J`, `[latent heat]=J/kg`.
- Distinguish material mass conservation from control volume mass; an **open** container can lose liquid mass by flux out. If vapor is tracked, total species mass includes liquid and vapor.
- Choose one y-axis sign convention and transform at viewport boundary. Gravity changes velocity; it doesn't set an object's position directly.
- For UI-only normalized parameters, use dimensionless labels and do not present them as measured material properties.

## Escalation triggers

Demand a more sophisticated solver/reference when facing fast small bodies, fast-changing rotations, many simultaneous contacts, capillary breakup, tightly coupled multiphase flows, boiling/condensation, numerical stiffness, safety-critical/engineering claims, or calibrated scientific outputs. If the user wants any physical phenomenon outside installed chapters, research the domain before claiming correct behavior.
