# Contributing

Use a scientific workflow: state the physical system, governing equations, dimensional units, assumptions, numerical method, boundary conditions, edge cases, fidelity label, and citations to reliable primary references. Provide tests that can fail meaningfully when physics breaks (not just screenshots), and avoid claiming any solver is universally accurate.

To add `new-chapter`, create `chapters/new-chapter/SKILL.md` with correct Agent Skills frontmatter and focused `references/` (if needed). Keep the root router's list up to date. Don't nest unnecessary chains of reading references. Test with `python3 scripts/validate_skill.py && python3 -m unittest discover -s tests -v`; optionally run `skills-ref validate` for every SKILL.md folder. All sample source code should be original, permitted under the repository license, and safe to run locally without API keys.

PRs should include the evaluation prompt, expected observable outcome, tests performed (actual commands/output), and acknowledged approximation/limitations.
