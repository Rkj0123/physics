# Material response, interface physics, optics

## Distinguish materials by measurable physics

- Density `ρ` [kg/m³]: inertia, hydrostatic pressure and buoyancy.
- Dynamic viscosity `μ` [Pa·s]: resistance to shear, often strongly temperature-dependent; kinematic viscosity `ν=μ/ρ` [m²/s]. Do **not** substitute arbitrary visual 'viscosity' scalar for either without calibration.
- Surface tension `γ` [N/m] for liquid–gas interface: creates pressure jump and smooths curvature; capillary pressure difference approximately `Δp=γ κ` with signed mean curvature convention specified (sphere in 3D: `Δp=2γ/R`). Different dimensions/curvature conventions alter coefficients.
- Contact angle `θ` [degrees/radians]: describes wetting on a specific solid/liquid/gas combination; pinning/contact-angle hysteresis may stop or distort rolling droplets.
- Gravity vs surface tension: Bond `Bo = Δρ g L² / γ`; inertia vs surface tension: Weber `We = ρ U² L / γ`; inertia vs viscosity: Reynolds `Re = ρ U L / μ`. Define characteristic scales and reference density. These ratios are guides, not universal thresholds for breakup or fingering.

## Capillary/wetting UI

- Droplets may coalesce to reduce interfacial area, but coalescence also evolves momentum, redistributes mass, and can have contact-line dissipation. A **metaball** is only a visual implicit surface until physical volume, motion and pressure are modeled.
- For a physically simulated closed two-drop merge, resulting volume is `V_after ≈ V_1 + V_2` at constant density; if assuming spherical drops in 3D, radius `R_after=(R_1³+R_2³)^(1/3)`. **Not** `R_1+R_2`. A 2D cross-section uses area and must not be confused with 3D volume.
- Free surface boundary condition includes normal stress due to curvature and tangential stress, plus wetting at walls; pressure Poisson alone won't make liquid droplets bead realistically.

## Buoyancy and coupling to solids

For a submerged solid in an approximately hydrostatic fluid, `|F_b|=ρ_fluid g V_displaced` upward. A neutrally buoyant body can remain suspended absent flows; a heavy body may sink; a light body floats until its submerged displaced mass equals its weight (plus any other vertical forces). Force acts at center of buoyancy and can create torque. For freely moving liquid and object, couple fluid pressures/drag and solid contacts instead of prescribing an unrelated bobbing sine wave.

## Fluid optics and visual look

Refraction, Fresnel reflectance, scattering, absorption, normal maps and caustics control material *appearance*, not fluid dynamics. Snell law `n1 sinθ1 = n2 sinθ2` is relevant for ray direction at ideal interfaces. A 'liquid glass' UI often means only a curved, refractive overlay without flowing liquid. Blur plus distortion is an art technique; use a fidelity label. Do not expose a physically measured index of refraction if the shader ignores geometry or viewing angle.

## Examples and classification

| Concept | Honest label | What physics is missing |
| --- | --- | --- |
| CSS border-radius blob | Stylized | Mass, pressure, capillary forces |
| SVG goo filter | Stylized | Volume, energy, mass transfer |
| Springs connecting UI circles | Physics-inspired soft body | Hydrodynamic pressure and free surface |
| Height-field ripple | Reduced wave simulation | Overturn, droplet breakup, full 3D flow |
| PBF with particle masses | Simulated approximate liquid | Usually true viscosity, thermal coupling, small-scale capillarity depending on implementation |
| Refractive overlay | Optical stylization or ray model | Liquid flow entirely |
