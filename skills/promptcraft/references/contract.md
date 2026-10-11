# Contract preservation

Load for a complex handoff or a material conflict. Keep a compact working
ledger, not a transcript. User instructions govern the skill's defaults.

| Contract field | What belongs here |
| --- | --- |
| Outcome | The observable user result and intended audience |
| Facts | Confirmed environment, reproduced symptom, available evidence |
| Decisions | Already chosen architecture, language, provider or release route |
| Constraints | Invariants, privacy, compatibility, budget, data ownership |
| Non-goals | Explicit exclusions; don't invent unnecessary prohibitions |
| Checks | Behavior, measurable target, affected regression checks |
| Authority | Exactly permitted edits, commits, PRs, merges and deployment targets |
| Unknowns | Material gaps, provisional assumptions, unavailable evidence |

An authorized implementation epic may include plan → implement → test → review
→ fix → merge → deploy → verify, but only the stages and targets actually granted.
Do not turn a request to write a prompt into authority for those actions here.
A request that mentions a deployment does not establish permission to perform it.
Carry explicit prior permission forward within its original scope.

If two requirements conflict, ask a focused question about the deciding issue.
Do useful independent preparation without silently selecting a winner. If a
metric lacks its measurement environment, state a conservative bounded assumption
or ask if it materially changes acceptance. An illustrative number is not a user
approved performance target.

Do not make claims from absent evidence: "no test coverage observed" is not
"no tests exist"; an opened contact link is not a sent message; a green build
is not production acceptance. Include missing repository artifacts as discovery
steps for the executor rather than pretending the author inspected them.
