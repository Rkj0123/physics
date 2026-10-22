# Review gates and adversarial evaluation

## PR review rubric (each must be answered)

1. **Specification:** physical contract, system boundary, units, sign, phase(s), mode and tolerance present?
2. **Equation/model match:** does solver update the same phenomenon described in UX? Easing != free fall; blur != conserved liquid; fading != mass transfer.
3. **Laws:** no untracked mass source/sink, passive contact energy gain, unsupported force, magically constant acceleration when friction should matter? If using artistic exceptions, identified clearly?
4. **Numerics:** fixed simulation step and time units; stable dt/resolution; collision tunneling and overlapping contacts; solver convergence? All boundary conditions present?
5. **Interactivity:** pointer release preserves velocity, collisions with moving walls behave, resize doesn't teleport through boundaries, frame rate won't change simulated motion?
6. **Accessibility/performance:** reduced motion, keyboard controls or equivalent, semantic components, mobile fallback, cleanup and frame/particle caps?
7. **Evidence:** analytical/limit-case tests, visual behavior, error/residual results, measured performance, justified limitations? Never claim tests not run.

## Twelve essential agent evaluation prompts

| Prompt | Expected key checks |
| --- | --- |
| Drop a card 1 m, no drag | t=sqrt(2h/g)≈0.4515 s, v≈4.429 m/s; units |
| Throw a card horizontally | x linear absent drag; y accelerates; no magic sideways slowdown |
| Elastic head-on equal masses | velocities exchange for e=1; momentum and KE conserved |
| Inelastic impact | e=0 normal relative separation speed 0; KE cannot increase |
| Stack many items | no indefinite interpenetration, jitter bounds, resting contact |
| Fast small projectile vs thin wall | CCD or substeps; no tunneling |
| Drag and fling | timestamped release velocity; input accounted as external impulse |
| Slider in a sealed water tank | mass/volume budget; wall no-flux condition |
| Water-like vs honey-like flow | proper viscosity ordering with same boundary/forcing; no unjustified constant values |
| Two droplets merging | surface/volume conserved approximately if physics-simulated; metaballs labeled illustrative |
| Evaporate into 100% saturated air | no evaporation in isothermal equilibrium; net depends on temperatures/gradients |
| Splash then evaporate | gravity, liquid transfer, vapor budget and latent heat accounted for or omissions explicit |

Avoid 'matches GIF' as the sole test. Replay at varied rates/resolutions; compare against reference/analytic data with tolerances specific to the numerical scheme.
