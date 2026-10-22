# Fluid governing models: assumptions, methods, numerical checks

## Governing conservation laws

General continuum form (single constituent):
- Mass continuity `∂ρ/∂t + ∇·(ρ u) = 0`. For **constant-density incompressible** flow, `∇·u=0`.
- Momentum balance `ρ (∂u/∂t + u·∇u) = -∇p + ∇·τ + ρ g + f_other`. Newtonian constant-`μ` isotropic model gives `τ=μ(∇u+∇uᵀ)` and simplifies (for ∇·u=0) to `μ∇²u`.
- Species with diffusivity `D` (ideal passive tracer): `∂c/∂t + u·∇c = D∇²c + S` for incompressible carrier (with appropriate units and BCs). This does **not** itself conserve numerical species mass with semi-Lagrangian sampling; measure error.
- Energy (when heat is relevant) may include conduction, convection, heat source and latent heat. Isothermal solvers should not claim to predict evaporation cooling, boiling or condensation temperature feedback.

## Eulerian grid (contained smoke / swirling dye)

Maintain face/cell velocity, cell pressure, and species/tracer. Each fixed physical step commonly: (1) advect velocities/tracers, (2) diffuse if solving viscosity/species transport, (3) apply gravity/user forcing, (4) pressure projection by Poisson solve to reduce divergence, (5) advect and enforce boundaries consistently. Order depends on chosen scheme; document it and assess truncation error. Verify no-flow wall condition (`u·n=0`); choose slip/no-slip appropriately.

A traditional 'stable fluids' semi-Lagrangian step samples `field_new(x) = field_old(x - u(x)*dt)` (with suitable backtracing and interpolation). Interpolation introduces numerical diffusion, generally fails exact conservation, and advection stability alone says nothing about projection/boundary accuracy or free-surface topology. Dye drawn from opaque color is typically **not** fluid volume.

## Height field ripples

Small disturbances may use `∂²h/∂t² = c²∇²h - β∂h/∂t`, with `c` [m/s] and `β` [1/s]. This is a linear wave approximation, not the universal water-surface dispersion law. The numerical wave step is sensitive to grid spacing/time step (`c dt / dx`); satisfy the scheme's dimension-dependent stability restriction, not an arbitrary frame rate. Damping represents energy loss. For a progress container, enforce mean fill consistent with liquid volume separately.

For shallow-water flow use depth-averaged conservation equations; don't treat a height ripple implementation as capable of breaking/splashing/free-surface overturning.

## Lagrangian particles / free surfaces

SPH (smoothed particle hydrodynamics): approximate density from weighted neighboring particle masses (`ρ_i=Σ m_j W(x_i-x_j,h)`), compute consistent pressure/viscous terms and boundary handling. A pile of ballistic particles without pressure forces is not SPH water. Common alternatives include PBF (position-based fluids; approximate incompressibility via density constraints) and FLIP/APIC (grid-particle transfer). All require a valid neighbor search, resolution/convergence tests and explicit free-surface/boundary treatment.

SPH/PBF may look compelling but is not automatically consistent with calibrated surface tension, evaporation, turbulent mixing or variable temperature. Mass is tracked by particle mass, but careless particle deletion or incompatible boundary handling can leak water. A blob implicit render should derive from particles or conserve volume when claimed physically motivated.

## Tests and diagnostics

- Track relative mass error `abs(m(t)-m0)/m0` when no open flow or phase change.
- Track divergence residual `||∇·u||` for an incompressible grid, with units/scales and tolerance explained.
- Test zero-gravity/zero-force still fluid; uniform flow in a periodic box; pressure equilibration; no-penetration of walls; point source only if intended.
- Refine spatial grid and time step and compare; failure to converge signals numerical/model limitations.
- Do **not** claim direct reproduction of realistic splashing if only a closed rectangular Eulerian dye domain is simulated. Verify the volume fraction/free-surface representation.

Reference: [NVIDIA GPU Gems 38](https://developer.nvidia.com/gpugems/gpugems/part-vi-beyond-triangles/chapter-38-fast-fluid-dynamics-simulation-gpu) (its canonical example does **not** model free surfaces).
