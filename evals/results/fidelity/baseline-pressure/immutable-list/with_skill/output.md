Here's the handoff. I read the Promptcraft contract notes and the Claude Code notes. Retrieval was unavailable, so these are dated cached notes and not live-verified. The target model is not established, so I used agent-level guidance only. I didn't add any queue design names, file paths, a deliverable location or a monitoring requirement, because you didn't give any. The manifest is copied verbatim, and I put the prompt in a four-backtick fence so the inner block can't break it.

````text
Prepare a proposal comparing queue designs.

Authority and constraints:
- Implementation is not authorized. Do not write or modify code, configuration or tests. Planning and read-only investigation are allowed.
- Add no new dependencies.
- The following manifest is immutable. Preserve it exactly, including order and punctuation. Do not reformat, reorder, extend or "improve" it, and do not propose changing it:

```json
{"schema":1,"fields":["job_id","status"],"terminal":"failed_final"}
```

Context:
- The prompt author has not specified which queue designs to compare, or any evaluation criteria. If the repository or your own investigation doesn't make the candidates clear, state which designs you chose to compare and why. Don't present that choice as a user requirement.
- You can't see the author's conversation. Rely only on what you can verify in your own environment.

Deliverable: a written proposal that compares the queue designs. Give it in your reply. Where the manifest is relevant, quote it unchanged.

Optional suggestion: discuss monitoring separately from the main comparison, for example in its own section. This is not required for completion.
````

Checks against your original request:
- **Proposal only:** the prompt covers the comparison and nothing else. It states that implementation isn't authorized and that planning is allowed.
- **Manifest:** it appears once, verbatim, as an immutable constraint. The prompt also tells the executor not to propose changing it, which goes slightly past "preserve exactly". Delete that clause if you want proposals to be able to suggest manifest changes.
- **No new dependencies:** kept as a constraint.
- **Monitoring:** kept as an optional suggestion inside the prompt and not as a completion check.
- **Open choice:** the prompt leaves the candidate designs and criteria open. If you have specific designs in mind, add them before sending it.