# Torus-Node research roadmap

Status date: 2026-11-15

This roadmap separates finite mathematical work, continuum construction, physical interpretation, and phenomenology. A milestone is complete only when its stated evidence exists; completion of an earlier layer does not silently complete a later one.

## Layer 1 — finite mathematical model

Current status: partially machine checked; global verification report remains `INCOMPLETE`.

- Maintain a stable statement-to-declaration crosswalk.
- Finish independent semantic review of theorem statements and hypotheses.
- Reproduce exact and interval-certified calculations from archived inputs.
- Classify which gauge and matter blocks are canonical and which are selected inputs.
- Record countermodels and non-identifiability results alongside positive results.

Evidence required: pinned source, successful independent build, axiom output, declaration-level review, and reproducible certificate logs.

## Layer 2 — microscopic source and scaling

Current status: open.

- Specify one complete microscopic source, including relation domain, transport, action, state–field map, and reflection.
- Prove uniform stability and moment bounds.
- Construct an exact same-measure coarse-graining map or a controlled alternative.
- Prove tightness and equicontinuity for the full interacting family.
- Identify retained sectors and control discarded modes.

Evidence required: the estimates must apply to the same family throughout. Results from different comparison models cannot be spliced into a stronger claim without an explicit bridge.

## Layer 3 — Euclidean-to-Lorentzian reconstruction

Current status: open/conditional.

- Establish physical reflection positivity for the unrestricted source.
- Verify the complete model-specific Osterwalder–Schrader premise package.
- Construct the Hilbert space, vacuum, positive Hamiltonian, and field content.
- Show that the proposed time orientation and signature survive the limit.

Evidence required: a theorem with matched hypotheses for the actual torus-node family, not only an abstract reconstruction theorem.

## Layer 4 — gauge, matter, and gravity dynamics

Current status: finite structural results with open physical bridges.

- Prove the source-to-Wilson universality bridge.
- Resolve or correctly delimit the Wilson-action photon, interacting electroweak gap, and physical SU(3) gap.
- Control anomaly statements in the continuum representation.
- Derive the Einstein–Hilbert coefficient with a bounded higher-derivative remainder.
- Test uniqueness of representation and vacuum selection.

Evidence required: cutoff-uniform estimates, declared universality class, and no transfer of SU(2) results to SU(3) without a theorem.

## Layer 5 — phenomenology and falsification

Current status: input-dependent comparisons; no parameter-free confirmation.

- Identify observables determined before measurement by the canonical model.
- Preregister parameter-selection and data-splitting rules.
- Propagate theoretical and numerical uncertainty.
- Test predictions on held-out data.
- Publish null results and failed predictions with the same visibility as successes.

Evidence required: a fixed prediction protocol that distinguishes fitted values, conditional outputs, and genuinely new predictions.

## Priority problems

1. Continuum limit and scaling.
2. Reflection positivity of the unrestricted source.
3. D4 dimension-selection stability.
4. Canonicity of S4 ordered-history gauge representations.
5. Controlled emergent Einstein–Hilbert dynamics.
6. Chiral matter and anomaly constraints.
7. New quantitative phenomenological predictions.

The public catalogue is maintained in `assets/js/problems.js`.
