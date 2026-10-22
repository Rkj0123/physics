# Gravity-to-UI recipes

## Falling chips / cards

Contract: rectangle colliders inside a responsive container, screen-y-down, gravity downward; the boundaries are immovable. Choose a 2D engine for nontrivial piles; each chip keeps a semantic label/button in DOM. On resize update the static walls and reproject any body outside new bounds. With reduced motion, show a stable, well-spaced list or grid preserving every control.

## Throw-and-release

Use Pointer Events; on grab attach a cursor spring/joint rather than teleporting a dynamic body every frame. For simple single-body analytic fling, on release compute velocity `(pointerB - pointerA)/(tB-tA)` using timestamps in seconds (at least two meaningful samples), map px/s to m/s, cap noisy spikes, then let simulation integrate. Handle cancel, lostpointercapture, missing timestamps and mobile event throttling. Keyboard equivalent can move items by fixed increments with explicit positioning (an external actuator).

## Button bounce / impact

If no true collision/interactivity is required, an eased keyframe bounce may be acceptable with fidelity `stylized`. If impact speed, mass and material should change the bounce, use dynamics and restitution instead. Do not advertise keyframes as obeying Newtonian motion. An impact must transfer/dissipate energy appropriately; no bounce amplification in passive materials.

## Magnetic / spring controls

Magnetism is not gravity. Hooke spring is a local restoring force with damping, not a literal inverse-square magnetic law. Label a 'magnetic' button as physics-inspired interaction. If using actual inverse-square attraction ensure singularity avoidance, force falloff, numerical bounds and external forcing are defined.

## Known bad implementations

- `element.style.top += 5` on each RAF: refresh-rate-dependent position, constant-speed fall.
- `onRelease: setVelocity(0, 0)`: destroys momentum rather than modeling impulse or damping.
- `if touching: velocity.y *= -1` for every frame: double-hit energy artifacts and jitter.
- Setting a chip's position directly to the pointer and calling it dynamic: kinematic manipulation without force accounting.
- Every object's acceleration proportional to its mass for uniform Earth gravity: violates equivalence of free-fall acceleration (neglecting drag).

Use known solutions and adversarial cases from the root quality gates; for actual numeric checks run the bundled stdlib tests.
