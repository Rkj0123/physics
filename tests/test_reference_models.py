"""Simple physical invariants; evidence for the reference formulas only."""

import math
import unittest

from scripts.physics_reference import (
    Motion1D, ballistic_exact, ballistic_symplectic_step,
    normal_contact_1d, kinetic_energy_1d,
    spherical_radius_from_mass, lumped_evaporation_mass_rate,
    closed_phase_step,
)


class GravityTests(unittest.TestCase):
    def test_analytic_one_meter_drop(self):
        g = 9.80665
        impact_time = math.sqrt(2 / g)
        result = ballistic_exact(Motion1D(0, 0), g, impact_time)
        self.assertAlmostEqual(result.x_m, 1.0, places=12)
        self.assertAlmostEqual(result.velocity_m_s, math.sqrt(2 * g), places=12)

    def test_symplectic_convergence_with_smaller_dt(self):
        g, total_s = 9.80665, 1.0
        exact = ballistic_exact(Motion1D(0, 0), g, total_s).x_m
        errors = []
        for steps in [60, 120, 240, 480]:
            dt = total_s / steps
            state = Motion1D(0, 0)
            for _ in range(steps):
                state = ballistic_symplectic_step(state, g, dt)
            errors.append(abs(state.x_m - exact))
        self.assertTrue(all(a > b for a, b in zip(errors, errors[1:])))
        self.assertLess(errors[-1], 0.011)

    def test_no_force_constant_speed(self):
        start = Motion1D(1, 3)
        now = ballistic_exact(start, 0, 2)
        self.assertAlmostEqual(now.x_m, 7)
        self.assertAlmostEqual(now.velocity_m_s, 3)

    def test_equal_mass_elastic_exchange(self):
        a, b = normal_contact_1d(4.0, -2.0, 2.0, 2.0, 1.0)
        self.assertAlmostEqual(a, -2.0)
        self.assertAlmostEqual(b, 4.0)
        self.assertAlmostEqual(2*4+2*(-2), 2*a+2*b)
        self.assertAlmostEqual(kinetic_energy_1d(4, 2)+kinetic_energy_1d(-2, 2),
                               kinetic_energy_1d(a, 2)+kinetic_energy_1d(b, 2))

    def test_inelastic_never_gains_kinetic_energy(self):
        before = kinetic_energy_1d(4, 2) + kinetic_energy_1d(-2, 2)
        for e in (0, 0.2, 0.6, 1):
            a, b = normal_contact_1d(4, -2, 2, 2, e)
            after = kinetic_energy_1d(a, 2) + kinetic_energy_1d(b, 2)
            self.assertLessEqual(after, before + 1e-12)
            self.assertAlmostEqual(2*a+2*b, 2*4+2*(-2))

    def test_static_wall_speed_ratio(self):
        # A travels right into stationary wall B, with n toward the wall.
        speed, static = normal_contact_1d(3, 0, 2, math.inf, 0.6)
        self.assertAlmostEqual(speed, -1.8)
        self.assertEqual(static, 0)
        self.assertAlmostEqual((speed / 3) ** 2, 0.36)

    def test_separating_contact_not_impulsed(self):
        self.assertEqual(normal_contact_1d(0, 2, 1, 1, 0.5), (0, 2))

    def test_contact_rejects_bad_physics_inputs(self):
        with self.assertRaises(ValueError):
            normal_contact_1d(2, 0, 1, 1, 1.2)
        with self.assertRaises(ValueError):
            normal_contact_1d(2, 0, math.inf, math.inf, 0)
        with self.assertRaises(ValueError):
            ballistic_symplectic_step(Motion1D(0,0), 9.8, 0)


class FluidTests(unittest.TestCase):
    def test_sphere_mass_volume_radius(self):
        rho, r = 1000.0, 0.002
        mass = rho * (4 / 3) * math.pi * r**3
        self.assertAlmostEqual(spherical_radius_from_mass(mass, rho), r)

    def test_merge_equal_spheres_volume_not_radius(self):
        rho = 1000.0
        r = 0.001
        single_mass = rho * (4/3) * math.pi * r**3
        combined_radius = spherical_radius_from_mass(2 * single_mass, rho)
        self.assertAlmostEqual(combined_radius, r * 2 ** (1 / 3))
        self.assertLess(combined_radius, 2 * r)

    def test_closed_evaporation_conserves_water_species(self):
        liquid, vapor = 1.0, 0.1
        for _ in range(1000):
            liquid, vapor = closed_phase_step(liquid, vapor, 0.01, 0.1)
            self.assertGreaterEqual(liquid, 0)
            self.assertAlmostEqual(liquid + vapor, 1.1, places=12)

    def test_closed_condensation_conserves_and_caps(self):
        liquid, vapor = closed_phase_step(0.1, 0.2, -9, 1)
        self.assertAlmostEqual(liquid, 0.3)
        self.assertAlmostEqual(vapor, 0)

    def test_saturation_isothermal_balance(self):
        self.assertEqual(lumped_evaporation_mass_rate(0.01, 2, 0.02, 0.02), 0)
        self.assertGreater(lumped_evaporation_mass_rate(0.01, 2, 0.02, 0.01), 0)
        self.assertLess(lumped_evaporation_mass_rate(0.01, 2, 0.02, 0.03), 0)

    def test_mass_flux_dimension_and_area(self):
        a = lumped_evaporation_mass_rate(0.01, 1, 0.02, 0)
        b = lumped_evaporation_mass_rate(0.01, 2, 0.02, 0)
        self.assertAlmostEqual(b, 2*a)

    def test_nonnegative_and_zero_depletion(self):
        self.assertEqual(closed_phase_step(0, 1, 10, 1), (0, 1))
        self.assertEqual(spherical_radius_from_mass(0, 1000), 0)
        with self.assertRaises(ValueError):
            spherical_radius_from_mass(-1, 1000)


if __name__ == "__main__":
    unittest.main()
