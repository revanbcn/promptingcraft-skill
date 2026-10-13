# One-pass critique rubric

Load when critiquing a draft. Use findings, not a self-awarded numeric score.

- Coverage: can every required outcome and invariant be traced to the prompt?
- Truth: are unsupported facts, conflicting claims and unknowns labeled?
- Authority: did any permission appear, disappear or expand during revision?
- Reality: can this executor access the named context/tools? Are commands confirmed?
- Acceptance: do checks test the result and regressions, with obtainable evidence?
- Provenance: does each operative final clause trace to original user wording or
  faithful decomposition? Are optional/inferred/unresolved items nonmandatory?
- Suggestions: are added preferences visibly optional inside the copyable prompt,
  absent from required behavior and completion gates?
- Context: does the handoff survive transfer to a fresh agent without chat memory?
- Privacy: does it exclude secrets and unnecessary private data from sources/output?
- Immutable text: are expressly fixed spans copied verbatim, with quantities/order?
  Did a weaker invariant such as no new dependencies become a whole-file freeze?
- Mode and choices: does discussion remain discussion; are ambiguous targets open?
  Are planning and implementation process choices sourced, rather than invented?
- No-change: if the original already works, preserve it; if a material defect
  remains, give the correction or deciding question. Activity is not a criterion.
- Economy: does every instruction change a decision, preserve a constraint or
  support verification? Keep a small task small.

Start the critique on the ORIGINAL task before authoring a replacement. For an
adequate original, no-change is the outcome; generating a new prompt first biases
the workflow toward keeping invented clauses. For a necessary correction, change
only the defective span and preserve surrounding requirements. Equally plausible
source files/logs remain an identity question. Missing-value inference and arithmetic
from supplied numbers are different operations; do not strengthen the prohibition.
Compare final against the ORIGINAL contract, not just against the draft.
If a material defect remains after one revision, make one targeted extra pass;
if still unresolved, disclose it or ask the deciding question. Do not optimize
indefinitely. Self-review is not independent verification or proof of improved
coding outcomes. Do not show hidden reasoning.
Record concise findings. Structural checks and an author's self-declared pass
do not establish semantic preservation or downstream success.
