**The original prompt is already suitable. No material revision is necessary.**

Reviewed text, kept exactly as written:

> Fix settings.py so save_settings returns 500 without showing success when the API returns status 500. Preserve the request payload and the status-200 success behavior. No new dependencies. Local edits and tests are authorized; do not commit or deploy. Verify both 500 and 200 behavior using the existing tests and report actual results.

**Contract check, original to final (nothing lost):**
- **Goal:** `save_settings` returns 500 and doesn't show success when the API returns 500.
- **Invariants:** keep the request payload, and keep the status-200 success behavior.
- **Constraint:** no new dependencies. This forbids adding dependencies only. It doesn't freeze manifests or lockfiles.
- **Authority:** local edits and tests are granted. Commit and deploy are forbidden.
- **Verification:** use the existing tests to check both the 500 and 200 paths, and report the actual results.

**Final clauses back to the original:** every clause traces to the user's own words. I found no added mechanisms, edge cases, handling for other network errors, new test frameworks, coverage gates, or process mandates such as "skip planning" or "plan first". The planning choice stays open. The 500 and 200 checks directly test the requested behavior, so they don't invent new completion criteria. The "report actual results" requirement guards against claiming a pass without evidence.

**Minor observations, not worth changing:**
- The prompt doesn't name a test command or the path to settings.py. The executor can find both in the repo, so this is ordinary discovery.
- If no existing test covers the 500 case, the prompt doesn't say whether to add one. That choice is unresolved. The executor can report it, and I haven't made it a requirement.

**Evidence and freshness:**
- **Supplied, not retrieved by me:** `guidance.md` is a bounded paraphrase of https://code.claude.com/docs/en/best-practices. The controller verified it on 2026-10-12. Its publication date is unknown.
- **Not live-verified by me:** I have no retrieval tool and didn't fetch that page.
- **Dated cached:** the Claude Code notes bundled with the skill, checked 2026-10-12.
- **Executor model:** unknown, so I applied no model-specific tuning.
- **How the guidance applied:** the supplied guidance (context, constraints, a feasible check) is already met. It also treats small-diff shortcuts as conditional advice, not a ban on planning, and says commit/PR workflows don't supply authority. The prompt's explicit "do not commit or deploy" fits that.

This is a self-review by the same model. It supports the contract fidelity of the prompt, not downstream success.