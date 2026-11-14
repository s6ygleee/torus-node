const problems = [
  {
    id: 'continuum-limit', code: 'TN-OP-01', area: 'foundations', title: 'Continuum limit and scaling',
    question: 'Can one construct a single microscopic torus-node family whose scaling limit satisfies the paper’s full source-to-continuum premise set?',
    background: 'The finite bounded-geometry model and the unrestricted Poisson-source reading are distinct. A valid bridge must use one common measure, state–field map, relation domain, and temporal transfer across the argument.',
    status: 'Open. Abstract compactness and closedness fragments exist, but source-specific tightness, exact same-measure blocking, and physical pole/vertex identification are not established for the interacting model.',
    assumptions: 'A specified microscopic action; uniform stability and moment bounds; a controlled observable topology; retained sectors or a summable complement; and cutoff-uniform estimates.',
    approaches: ['Constructive RG with explicit polymer norms', 'Stochastic homogenisation on random geometric complexes', 'Prokhorov tightness plus model-specific OS bounds', 'Γ-convergence or operator convergence for quadratic sectors'],
    references: ['Preprint §§2 and audit/source-to-continuum sections', 'Lean archive: ProkhorovOSCore and ReflectionPositiveLimit'],
  },
  {
    id: 'reflection-positivity', code: 'TN-OP-02', area: 'analysis', title: 'Reflection positivity',
    question: 'Is the unrestricted Poisson torus-source measure reflection positive for a physically adequate relational observable algebra?',
    background: 'Finite declared sources and selected comparison models have positivity results. The physical claim requires positivity after averaging the unrestricted random geometry and controlling the fermionic/graded sector.',
    status: 'Open. The release proves finite Gram and weak-limit closure components, not the complete model-specific Osterwalder–Schrader E0–E4 hierarchy.',
    assumptions: 'A well-defined reflection, positive-time algebra, measurable random geometry, normalized interacting state, and a topology in which reflected forms pass to limits.',
    approaches: ['Conditional expectation and reflection factorisation', 'Random-cluster or loop representations', 'Positive-kernel decompositions', 'Counterexample search on finite source ensembles'],
    references: ['Preprint: averaged reflection-positivity hypothesis', 'Lean archive: reflection-positive finite and limit cores'],
  },
  {
    id: 'd4-stability', code: 'TN-OP-03', area: 'geometry', title: 'D₄ dimension-selection stability',
    question: 'Does the four-dimensional carrier and one-time-direction selection survive admissible perturbations, random source variation, and coarse-graining?',
    background: 'The declared finite model uses D₄ roots/moves and a distinguished-axis mechanism. A robust physical explanation needs structural stability beyond the selected finite representative.',
    status: 'Open as a universality question. Finite root counts, partitions, and selected dispersion identities are represented in the formal archive.',
    assumptions: 'A precise perturbation class, a scale-dependent move operator, non-degeneracy criteria, and a definition of stable dimension/signature selection.',
    approaches: ['Spectral perturbation theory', 'Renormalisation of random walk generators', 'Representation-stability analysis', 'Computer-assisted classification of nearby root/move systems'],
    references: ['Preprint sections on D₄ geometry and signature', 'Lean archive: D4, D4Roots, D4Lightcone, V8SignatureCore'],
  },
  {
    id: 's4-gauge', code: 'TN-OP-04', area: 'algebra', title: 'S₄ ordered histories and gauge representations',
    question: 'Which gauge and matter representations follow canonically from the ordered-history algebra, and which depend on retained-block choices?',
    background: 'The four-cusp permutation module alone does not supply the claimed gauge factors. The construction instead uses a right-regular commutant and selected matter-coupled blocks.',
    status: 'The finite commutant calculations have formal cores. Canonicity, uniqueness of block selection, and continuum representation transport remain research questions.',
    assumptions: 'A declared history algebra, involution, matter bimodule, central quotient rule, and physically motivated equivalence relation between representations.',
    approaches: ['Finite-dimensional C*-algebra classification', 'Morita-equivalence analysis', 'Character theory and computational representation theory', 'Anomaly and chirality constraints as selection principles'],
    references: ['Preprint sections on level-three cusps and gauge structure', 'Lean archive: history, charge-block, and matter structural cores'],
  },
  {
    id: 'gravity-dynamics', code: 'TN-OP-05', area: 'gravity', title: 'Emergent Einstein–Hilbert dynamics',
    question: 'Can the metric effective action be derived with a controlled, nonzero Einstein–Hilbert coefficient and bounded higher-derivative remainder?',
    background: 'The dynamical-metric branch introduces a metric axiom and an annealed or quenched effective action. The two-derivative gravitational form is conditional on a low-energy expansion.',
    status: 'Open at the full interacting/source level. The finite model contains algebraic targets and selected conditional coefficient relations.',
    assumptions: 'Axiom M or an alternative derived metric dynamics; regularity of log partition functions; scale separation; and diffeomorphism-compatible renormalisation.',
    approaches: ['Heat-kernel and resolvent expansions with uniform errors', 'Stress-tensor two-point functions and induced gravity', 'Discrete curvature convergence', 'Ward identities excluding a local graviton mass term'],
    references: ['Preprint gravity and scope sections', 'Lean archive: gravity and gravity–gauge algebraic cores'],
  },
  {
    id: 'chiral-anomalies', code: 'TN-OP-06', area: 'matter', title: 'Chiral matter and anomaly constraints',
    question: 'Can chirality, anomaly cancellation, and family structure be obtained without discretionary representation or vacuum inputs?',
    background: 'The finite conditional bimodule yields quantised charges and anomaly-cancellation identities for declared matter content. Generation count and several mass/mixing quantities remain vacuum data or outside current predictive scope.',
    status: 'Finite charge/anomaly calculations are checkable; canonical derivation from the microscopic source and a complete non-perturbative chiral measure remain open.',
    assumptions: 'A selected matter bimodule, chiral action, regulator preserving required symmetries, and a continuum limit with the intended gauge representations.',
    approaches: ['Index-theoretic formulation on the discrete complex', 'Ginsparg–Wilson or overlap constructions', 'Cobordism/global-anomaly analysis', 'Classification under minimality and anomaly constraints'],
    references: ['Preprint matter and anomaly sections', 'Lean archive: Matter, MatterStructural, and charge-block cores'],
  },
  {
    id: 'predictions', code: 'TN-OP-07', area: 'phenomenology', title: 'New quantitative phenomenological predictions',
    question: 'Which observables can be predicted before measurement from the canonical model rather than fitted through free moduli or matching inputs?',
    background: 'Current comparisons use measured couplings and declared threshold, overlap, and matching inputs. The paper labels these input-dependent outputs rather than parameter-free predictions.',
    status: 'Open. Quark masses, CKM and PMNS mixing, neutrino masses, and the primordial perturbation amplitude are not reproduced at leading order.',
    assumptions: 'A preregistered parameter-selection rule, uncertainty propagation, a fixed data split, and an observable insensitive to unresolved continuum choices.',
    approaches: ['Identifiability analysis and parameter counting', 'Blind or held-out prediction protocols', 'Bayesian model comparison with declared priors', 'Search for robust dimensionless ratios or selection rules'],
    references: ['Preprint scope and observational-specialisation sections', 'Research roadmap in this repository'],
  },
];

const list = document.querySelector('[data-problem-list]');
const filters = document.querySelectorAll('[data-filter]');

const escapeHtml = (text) => String(text).replace(/[&<>'"]/g, (char) => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[char]));
const issueUrl = (problem) => `https://github.com/s6ygleee/torus-node/issues/new?template=open-research-problem.yml&title=${encodeURIComponent(`[${problem.code}] ${problem.title}`)}`;

function render(filter = 'all') {
  if (!list) return;
  const selected = filter === 'all' ? problems : problems.filter((problem) => problem.area === filter);
  list.innerHTML = selected.map((problem, index) => `
    <details class="problem-card" id="${escapeHtml(problem.id)}" ${index === 0 && filter === 'all' ? 'open' : ''}>
      <summary><span class="problem-id">${escapeHtml(problem.code)}</span><h2>${escapeHtml(problem.title)}</h2></summary>
      <div class="problem-body">
        <section><h3>Research question</h3><p>${escapeHtml(problem.question)}</p></section>
        <section><h3>Current status</h3><p>${escapeHtml(problem.status)}</p></section>
        <section><h3>Background</h3><p>${escapeHtml(problem.background)}</p></section>
        <section><h3>Assumptions</h3><p>${escapeHtml(problem.assumptions)}</p></section>
        <section><h3>Suggested approaches</h3><ul>${problem.approaches.map((item) => `<li>${escapeHtml(item)}</li>`).join('')}</ul></section>
        <section><h3>Relevant references</h3><ul>${problem.references.map((item) => `<li>${escapeHtml(item)}</li>`).join('')}</ul><p><a href="${issueUrl(problem)}">Open a scoped GitHub Issue →</a></p></section>
      </div>
    </details>`).join('');
}

filters.forEach((button) => button.addEventListener('click', () => {
  filters.forEach((item) => item.setAttribute('aria-pressed', 'false'));
  button.setAttribute('aria-pressed', 'true');
  render(button.dataset.filter);
}));

render();

if (location.hash) {
  requestAnimationFrame(() => {
    const target = document.querySelector(location.hash);
    if (target?.tagName === 'DETAILS') target.open = true;
    target?.scrollIntoView({ block: 'start' });
  });
}
