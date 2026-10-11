Here is the prompt, ready to paste into ChatGPT. Replace the two placeholders with the sheet text, or attach the sheets.

```text
Compare two public product specification sheets on battery life and weight. Use only the two sheets supplied below. Do not browse, search the web, or use outside knowledge.

Sheet A (paste text or attach file):
[PASTE SHEET A, including its product name and any section headings]

Sheet B (paste text or attach file):
[PASTE SHEET B, including its product name and any section headings]

Requirements:
- Compare the two products on battery life and weight only.
- For every value you report, cite the sheet (A or B) and the section where it appears, using the sheet's own section heading.
- If a sheet does not state a value, write "unknown" for it. Do not infer, estimate, calculate, or fill in missing numbers.
- Do not recommend which product to buy.

Format: A compact table (rows: battery life, weight; columns: Sheet A, Sheet B, with the citation next to each value) would be useful, but it is optional. Use prose if you prefer.

Optional suggestion: if a sheet states a condition for a value (for example a test mode or a weight with or without accessories), report that condition as written.
```

Notes:
- **Source freshness:** `guidance.md` is a synthetic fixture dated 2026-10-10. I used it only as test context, not as live official guidance. No network retrieval was used.
- **Target model:** The prompt is generic manual-ChatGPT text, so I did no model-specific tuning.
- **Drift check:** Every operative clause traces to your request: use only these sheets, cite sections, mark missing values unknown, no browsing or inference, optional table, and no purchase recommendation. The only addition is the condition-reporting line. I marked it as an optional suggestion inside the prompt, and it isn't a completion criterion.
- **Not executed:** I composed the prompt only. I did not compare any sheets.