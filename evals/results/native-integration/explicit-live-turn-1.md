Initial draft: Make the smallest worker fix so malformed JSON returns HTTP 400. Preserve valid-payload responses and the public API, add no dependencies, and stay within implementation and relevant tests.

Critique: The original prompt is already suitable. No material revision is necessary. It defines an observable outcome, compatibility constraints, and authorization without prescribing an unverified implementation. This matches [official Codex prompting guidance](https://learn.chatgpt.com/docs/prompting), retrieved on 2026-10-12.

```text
We want a minimal fix for a worker that returns success after invalid JSON. Return HTTP 400 for malformed JSON; preserve existing responses for valid payloads and the public API. No new dependencies. Implementation and relevant tests are authorized; no deployment.
```

