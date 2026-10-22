"""Tiny SI-unit educational reference models, not general-purpose solvers.

No external dependencies. The examples document analytically tractable pieces
of the Physics Agent Skill and support invariant tests. Do NOT import this as a
complete collision engine or evaporation/CFD model in a production app.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Motion1D:
    x_m: float
    velocity_m_s: float


def ballistic_exact(state: Motion1D, gravity_m_s2: float, time_s: float) -> Motion1D:
    """Constant gravity, screen-y-down, no drag: analytic reference."""
    if time_s < 0 or not math.isfinite(time_s) or not math.isfinite(gravity_m_s2):
        raise ValueError("time must be nonnegative, gravity finite")
    return Motion1D(
        state.x_m + state.velocity_m_s * time_s + 0.5 * gravity_m_s2 * time_s**2,
        state.velocity_m_s + gravity_m_s2 * time_s,
    )


def ballistic_symplectic_step(state: Motion1D, gravity_m_s2: float, dt_s: float) -> Motion1D:
    """One positive fixed step with symplectic Euler; numerical approximation."""
    if dt_s <= 0 or not math.isfinite(dt_s) or not math.isfinite(gravity_m_s2):
        raise ValueError("positive finite dt and finite g required")
    velocity = state.velocity_m_s + gravity_m_s2 * dt_s
    return Motion1D(state.x_m + velocity * dt_s, velocity)


def normal_contact_1d(v_a: float, v_b: float, m_a: float, m_b: float,
                      restitution: float) -> tuple[float, float]:
    """One approaching 1D contact with n pointing A -> B, no spin/friction.

    Bodies may be static (mass=math.inf). Cannot solve two static bodies.
    """
    if not (0 <= restitution <= 1):
        raise ValueError("passive contact restitution must be between zero and one")
    if math.isnan(m_a) or math.isnan(m_b) or m_a <= 0 or m_b <= 0:
        raise ValueError("masses must be positive or infinite for static")
    if not math.isfinite(v_a) or not math.isfinite(v_b):
        raise ValueError("velocities must be finite")
    ia, ib = (0.0 if math.isinf(m) else 1 / m for m in (m_a, m_b))
    if ia + ib == 0:
        raise ValueError("two static bodies have no dynamic contact impulse")
    vn = v_b - v_a
    if vn >= 0:
        return v_a, v_b  # separating or resting
    impulse = -(1 + restitution) * vn / (ia + ib)
    return v_a - impulse * ia, v_b + impulse * ib


def kinetic_energy_1d(v: float, mass_kg: float) -> float:
    if not math.isfinite(v) or not math.isfinite(mass_kg) or mass_kg <= 0:
        raise ValueError("positive finite mass and finite velocity required")
    return 0.5 * mass_kg * v * v


def spherical_radius_from_mass(mass_kg: float, density_kg_m3: float) -> float:
    """Assumes isolated spherical 3D liquid droplet and constant density."""
    if mass_kg < 0 or not math.isfinite(mass_kg):
        raise ValueError("mass must be finite and nonnegative")
    if density_kg_m3 <= 0 or not math.isfinite(density_kg_m3):
        raise ValueError("density must be positive and finite")
    return (3 * mass_kg / (4 * math.pi * density_kg_m3)) ** (1 / 3)


def lumped_evaporation_mass_rate(k_mass_m_s: float, area_m2: float,
                                 surface_saturation_kg_m3: float,
                                 ambient_vapor_kg_m3: float) -> float:
    """Signed liquid->vapor flux [kg/s]; lumped k*A*concentration driving force.

    Illustrative mass-transfer *model*, not a predictive calibrated coefficient.
    Negative flux denotes condensation. All parameters require stated conditions.
    """
    vals = (k_mass_m_s, area_m2, surface_saturation_kg_m3, ambient_vapor_kg_m3)
    if any(not math.isfinite(v) or v < 0 for v in vals):
        raise ValueError("coefficients, area and vapor densities must be finite and nonnegative")
    return k_mass_m_s * area_m2 * (surface_saturation_kg_m3 - ambient_vapor_kg_m3)


def closed_phase_step(liquid_kg: float, vapor_kg: float,
                      net_evap_rate_kg_s: float, dt_s: float) -> tuple[float, float]:
    """Conserve species mass in sealed reservoir with well-mixed ideal transfer.

    Ignores latent heat and pressure equilibration and must not be used to claim
    realistic evaporation without coupling to energy/transport models.
    """
    if any(not math.isfinite(v) or v < 0 for v in (liquid_kg, vapor_kg)):
        raise ValueError("phase masses must be finite and nonnegative")
    if dt_s <= 0 or not math.isfinite(dt_s) or not math.isfinite(net_evap_rate_kg_s):
        raise ValueError("finite flux and positive timestep required")
    transfer_kg = max(-vapor_kg, min(liquid_kg, net_evap_rate_kg_s * dt_s))
    return liquid_kg - transfer_kg, vapor_kg + transfer_kg
