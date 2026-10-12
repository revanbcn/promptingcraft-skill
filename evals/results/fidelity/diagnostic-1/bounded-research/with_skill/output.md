```
Compare two public product specification sheets on battery life and weight.

Sheets: Sheet A and Sheet B are supplied below or attached. Replace the placeholders before sending.
Sheet A: [paste text or attach file, and name the product]
Sheet B: [paste text or attach file, and name the product]

Rules:
- Use only Sheet A and Sheet B. Do not browse, and do not use outside knowledge.
- Do not infer, estimate, or calculate any number that a sheet does not state. If a value for battery life or weight is missing from a sheet, write "unknown" for it.
- For every value you report, cite the sheet and the section where it appears. Use the section heading or label as written in the sheet, for example "Sheet A, Battery". If a sheet has no section labels, say so and quote the short phrase the value came from.
- Do not recommend a purchase.

Output:
1. Battery life: the value for each sheet, with citations, and a plain statement of how they compare. Say "cannot compare" if either value is unknown.
2. Weight: the same.
3. A compact table is optional. If you include one, use rows for Battery life and Weight, columns for Sheet A and Sheet B, and a citation next to each value.
```

**Notes**
- The prompt only tells ChatGPT how to do the comparison. You paste or attach the two sheets yourself, since I can't see them.
- I treated `guidance.md` as synthetic context dated 2026-10-10. It says that nothing here is live-verified official guidance, and that a fresh executor can't see this chat. So the prompt stands alone and makes no claim about official sources.
- I added no requirements beyond your request. The table stays optional. The "cannot compare" wording and the quote-a-phrase fallback for unlabeled sheets only spell out your rules on unknown values and citations.
- You didn't mention unit conversion or conflicting values within a sheet, so I left them open. Say if you want either handled.