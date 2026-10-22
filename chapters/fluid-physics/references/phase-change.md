# Evaporation, condensation and phase change

## First law: disappearing pixels ≠ disappearing mass

An evaporating liquid surface exchanges **mass and energy** with the surrounding gas. Define the system boundary: open container vs sealed chamber. In a closed, leak-free chamber, water **species** mass is redistributed between liquid and vapor; in an open room model, vapor leaves through a specified outward flux. If drops shrink, calculate their liquid mass change and the corresponding volume change using density, not arbitrary alpha.

Let `m_l` be liquid mass, `m_v` water-vapor mass **within** a closed control volume, and `ṁ_evap ≥ 0` / `ṁ_cond ≥ 0` be phase rates [kg/s]:

`dm_l/dt = -ṁ_evap + ṁ_cond + ṁ_l,in - ṁ_l,out`

`dm_v/dt = +ṁ_evap - ṁ_cond + ṁ_v,in - ṁ_v,out`

For sealed system with no other transfer, `d(m_l+m_v)/dt=0`; heat can still enter from outside. Do not mistake total moist-air mass for liquid plus vapor species mass.

## Rate depends on transport and equilibrium

A commonly used **mass-transfer abstraction** for a specified interface is:

`ṁ_evap - ṁ_cond = k_m A (ρ_v,sat(T_surface) - ρ_v,ambient)`

where `k_m` [m/s] is an effective mass-transfer coefficient, `A` [m²] is exposed area, vapor densities are [kg/m³]; the right side is [kg/s]. This is a **lumped illustrative model**, not universal, and needs calibration for airflow, geometry, and transport. Temperatures, saturation curves and pressure cannot be replaced by a single magic percentage. The gas immediately at interface may differ from bulk conditions.

Relative humidity `RH` is vapor partial pressure divided by saturation vapor pressure at ambient gas temperature. **At the same temperature** and equilibrium saturated vapor, net evaporation tends to zero; if surface and ambient temperatures differ, `RH=100%` at ambient **alone** does not force zero net transfer. A drop can condense when interfacial/bulk vapor gradients drive transport inward.

## Thermal/latent heat constraint

Evaporation draws latent heat approximately `Q̇_latent = L_v * ṁ_evap` with `L_v` [J/kg], subject to ambient conductive/convective/radiative heat exchange and sensible heating/cooling. For a closed liquid lump, schematic balance: `m_l c_p dT/dt ≈ Q̇_in - L_v (ṁ_evap - ṁ_cond)` with changing mass, heat capacities, phase enthalpy reference, and work neglected. For quantitative results derive a consistent enthalpy balance including mass-flux enthalpy; the compact equation is a simplifying demonstration only. Strong forced evaporation without an energy source cannot maintain arbitrary constant temperature.

## Geometric update

For constant liquid density: `V_l=m_l/ρ_l`.
- **Free spherical droplet in 3D**, no substrate: `V=4πr³/3` ⇒ `r=(3m/(4πρ_l))^(1/3)`.
- Sessile pinned droplet: contact line and angle evolve; don't use free sphere volume formulas. If contact radius remains fixed, droplet height/contact angle change, not necessarily the contact radius.
- A `D²` evaporation law (`D(t)²≈D0²-Kt`) can describe **certain** quasi-steady, diffusion-controlled isolated spherical-droplet regimes; not a universal law for every puddle, coffee droplet, airflow, humidity or boiling. `K` must be inferred from conditions or measured, not invented. No negative squared diameter; stop at physical exhaustion.

## Evaporation vs boiling vs visible mist

- **Evaporation**: molecules transfer from liquid to gas across an interface and can occur below boiling temperature.
- **Boiling**: vapor bubble nucleation/growth within the liquid when local thermodynamic/pressure conditions permit; needs different modeling.
- **Condensation**: vapor transitions to liquid, can produce droplets/fog on cool surfaces or in supersaturated gas.
- **Water vapor is invisible**. White 'steam' near a kettle is mainly suspended condensed droplets (mist) that scatter light. Animated upward particles are a *visual proxy*, not the molecular vapor itself.

## Tests before shipping

1. Close all inflow/outflow; with evaporation active, verify `m_l + m_v` conserved within the integrator's tolerance.
2. Evaporate into dry air in the stated lumped model: positive net rate, drop mass and volume decrease monotonically and nonnegatively.
3. Equal surface/ambient temperature with equilibrium saturation: zero net mass transfer (within tolerance).
4. Change bulk humidity at fixed other parameters: smaller positive driving force near saturation; check sign around equilibrium.
5. Track surface temperature or explicitly prescribe an **external thermal reservoir**; never imply heat conservation in a thermostat-controlled toy.
6. Never render a negative radius or emit vapor after liquid mass is zero. Confirm finite output at zero radius/zero surface area.
7. Validate any numeric evaporation rate against measured conditions; arbitrary `k_m` values are demonstrations, not predictions.

Reference model background: [Ansys Fluent droplet vaporization models](https://ansyshelp.ansys.com/public/Views/Secured/corp/v251/en/flu_th/flu_th_sec_disp_law2.html).
