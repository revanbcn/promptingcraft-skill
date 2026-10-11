Here is the prompt, ready to paste into ChatGPT along with the two sheets.

```text
Task: Compare two public product specification sheets on two attributes only, battery life and weight.

Inputs: I will supply Sheet A and Sheet B (pasted text or attached files) in this conversation. Before you begin, label them "Sheet A" and "Sheet B" and give each product's name exactly as the sheet states it. If either sheet is missing or unreadable, say so and stop. Do not substitute anything else.

Rules:
- Use only the two supplied sheets. Do not browse, use outside knowledge, or consult other versions of these products.
- Do not infer, estimate, convert between conditions, or calculate any number the sheet does not state. Unit conversions (for example grams to ounces) are allowed only if you show the arithmetic and mark the result "converted".
- If a value is absent from a sheet, write "Unknown (not stated in Sheet X)". Do not fill it in from memory.
- For every value, cite the sheet and its section, table, or heading (for example "Sheet A, Specifications > Battery"). If the sheet has no section labels, give a short verbatim quote instead.
- Record battery life with its stated test conditions or usage scenario (for example "video playback" or "standby") and every scenario listed. Do not treat figures from different scenarios as equivalent. If the two sheets use different scenarios or measurement methods, say the figures are not directly comparable.
- For weight, record exactly what the sheet describes (for example with or without battery, with or without accessories, or variant-specific) and the stated unit.
- If a sheet gives conflicting values for the same attribute, report both with citations and do not resolve the conflict.

Output:
1. A compact table with these columns: Attribute | Sheet A value (citation) | Sheet B value (citation) | Comparability note. Use one row per battery-life scenario and per weight configuration.
2. Up to five bullets stating only what the sheets support: which product has the higher stated figure where the comparison is valid, and which items are unknown or not comparable.
3. A short "Unknowns and caveats" list.

Do not recommend a purchase, rank the products overall, or comment on any attribute other than battery life and weight.

Before you answer, check that every number in your output appears in a sheet and has a citation, and that every missing value is marked Unknown.
```

- **Target:** The target is ChatGPT used manually, and the model is unspecified. I wrote it as a general prompt, not as a coding-agent handoff.
- **Sources:** I used `guidance.md`, a synthetic fixture dated 2026-10-10. It is not live-verified official guidance, and no network retrieval was available. I used it only for the general principles: the prompt must stand alone, say what it wants, set constraints, and give checks you can observe.
- **Table:** The table is included but marked as the default format, so you can drop it.
- **Assumption:** I added one assumption: unit conversions are allowed only with the arithmetic shown. You can delete that line if you want no conversions at all.