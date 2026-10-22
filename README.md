# Physics — physics-grounded skills for AI agents

A portable, open-source **Agent Skills** collection for making physics-informed UI interactions, animation, games, and simulation code. The umbrella skill is named `physics`; the first two nested chapter skills are `gravity-physics` and `fluid-physics`.

**Status:** v0.1.0, reference guidance plus basic deterministic checks; *not* a certification of scientific accuracy or a ready-made fluid engine.

## Why

A bounce easing curve is not a collision solver. Blurred metaballs are not automatically water. A droplet fading out is not a mass-conserving evaporation model. This skill makes agents explicitly select an appropriate model, declare assumptions, and run meaningful checks instead of treating visual resemblance as physical correctness.

## Layout

```text
physics/
├── SKILL.md                         # agent's single entry point
├── chapters/
│   ├── gravity-physics/
│   │   ├── SKILL.md                  # spec-compatible nested subskill
│   │   └── references/              # contact, interaction and numerical notes
│   └── fluid-physics/
│       ├── SKILL.md
│       └── references/              # flow, interfaces and phase change
├── references/                     # universal model, rendering, QA, sources
├── scripts/                        # stdlib validator and runnable reference model
├── tests/                          # invariants and edge-case regression tests
└── .github/workflows/              # CI validation
```

## Install

Install from this public repository with the [Skills CLI](https://skills.sh/):

```bash
npx skills add Rkj0123/physics --skill physics
```

Or clone this repository and copy its full folder to an Agent Skills directory, e.g. `~/.agents/skills/physics/`, keeping `chapters/`, `references/`, `scripts/`, and `tests/` alongside `SKILL.md`. Other clients may use different discovery paths. A nested chapter is a valid standalone skill, but most clients do not automatically discover nested folders; **install/use `physics` as the main entry point**. No runtime dependency is required to *read* this skill.

## Example requests

- “Build React tags that fall and collide inside a responsive box, retaining release velocity.”
- “Create a liquid button where droplets merge and separate. State whether the result is visual or simulated.”
- “A glass fills with water, then evaporates as temperature changes. Account for mass, heat, humidity and volume, within stated assumptions.”
- “Review this interaction for momentum/energy violations and frame-rate dependence.”

## Design commitments

1. **Correct model first:** define reference frame, units and boundary conditions.
2. **Appropriate fidelity:** visual approximations are allowed only when declared; higher fidelity requires validation.
3. **Explicit accounting:** check mass, momentum, energy, forces and phase transfer when applicable.
4. **Deterministic verification:** simple known solutions and invariants are built into tests.
5. **Practical UI:** responsive performance, cleanup, keyboard accessibility and reduced motion.

The umbrella is a **chapter router**, not a claim that two chapters exhaust physics.

## Validation

```bash
python3 scripts/validate_skill.py
python3 -m unittest discover -s tests -v
# Optional official reference CLI if installed:
skills-ref validate "$(pwd)"
skills-ref validate chapters/gravity-physics
skills-ref validate chapters/fluid-physics
```

The custom validator checks expected structure, frontmatter and local referenced links. The official `skills-ref` is the reference metadata validator; these two checks serve different purposes.

## References and attribution

See [references/sources.md](references/sources.md) for primary sources and implementation cautions. These files are original explanatory instructions, not copies of third-party tutorial content.

## Limitations

No generic instruction file can guarantee an arbitrary generated implementation never violates physical laws. Real materials depend on temperature, geometry and conditions; finite discretization and floating-point math introduce error. The skill enforces scoped physical contracts, honest disclosures, checks and escalation where fidelity is insufficient.

## Contributing and license

Contributions of well-referenced chapters, reproducible experiments and evaluation cases are welcome; see [CONTRIBUTING.md](CONTRIBUTING.md). MIT license.
