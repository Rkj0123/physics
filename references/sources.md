# References for further verification

Primary/authoritative sources chosen for concepts; do not assume third-party example constants are SI-calibrated.

- [Agent Skills specification](https://agentskills.io/specification) — required metadata, paths, progressive disclosure and reference validator.
- [Agent Skills official repository](https://github.com/agentskills/agentskills) — format and `skills-ref` reference validator.
- [Cornell CS5643: rigid bodies](https://www.cs.cornell.edu/courses/cs5643/2025sp/assignments/A2.html) — symplectic Euler, impulses, contact solving.
- [Matter.js Body API](https://brm.io/matter-js/docs/classes/Body.html) — **engine-specific** parameter semantics; its `restitution` is a velocity coefficient used in pair contacts, not simply “percent energy retained.”
- [NVIDIA GPU Gems 38](https://developer.nvidia.com/gpugems/gpugems/part-vi-beyond-triangles/chapter-38-fast-fluid-dynamics-simulation-gpu) — incompressible Navier–Stokes grid fluids, advection and pressure projection; **no free-surface solver** in its base setup.
- [PavelDoGreat WebGL Fluid Simulation](https://github.com/PavelDoGreat/WebGL-Fluid-Simulation) — interactive GPU flow visualization; inspect its exact solver behavior before making physical conservation claims.
- [Ansys Fluent droplet vaporization](https://ansyshelp.ansys.com/public/Views/Secured/corp/v251/en/flu_th/flu_th_sec_disp_law2.html) — phase-change mass/heat exchange models and limits.
- [MDN requestAnimationFrame](https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame) — timestamp semantics and display refresh differences.
- [MDN prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion) — accessible animation fallback.

Do not copy code or instructional passages from these links into new chapters without checking licenses and attribution requirements. Sources support models; they do **not** validate generated artifacts by citation alone.
