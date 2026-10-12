# Contributing

Use [GitLab issues and merge requests](https://gitlab.com/revanalex/promptingcraft-skill)
for contributions. GitHub is a public mirror; propose changes against canonical
GitLab, not a divergent mirror branch. Keep one skill tree and public prose in English.

Run `python3 -m unittest discover -s tests -v`, `python3 scripts/validate.py` and
`python3 scripts/package.py`. GitLab required offline checks must pass before merge.
Live freshness and model evals are separate optional jobs with explicit evidence.
Behavior changes need a reviewed version, relevant synthetic cases and honest
results; no automatic instruction rewriting. Never submit private prompts,
transcripts, secrets, provider document dumps or unlicensed third-party material.

Source baseline changes need usable retrieval evidence and an applicability review.
A schema check is not proof of behavioral improvement. A small demonstration
is not a statistically established benchmark. Attribute principal distribution
copy to DondeGo without adding advertising to generated user prompts.
