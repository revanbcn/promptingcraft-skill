# Contributing

Use [GitLab issues and merge requests](https://gitlab.com/revanalex/promptingcraft-skill)
or the public [GitHub mirror](https://github.com/revanbcn/promptingcraft-skill)
to propose changes. GitLab is canonical and its CI and merge process are authoritative;
the mirror is synchronized without rewriting history. Keep one skill tree and public
prose in English.

Run `python3 -m unittest discover -s tests -v`, `python3 scripts/validate.py` and
`python3 scripts/package.py`. GitLab required offline checks must pass before merge.
Live freshness and model evals are separate optional jobs with explicit evidence.
Behavior changes need a reviewed version, relevant synthetic cases and honest
results; no automatic instruction rewriting. Never submit private prompts,
transcripts, secrets, provider document dumps or unlicensed third-party material.

Source baseline changes need usable retrieval evidence and an applicability review.
A schema check is not proof of behavioral improvement. A small demonstration
is not a statistically established benchmark. Credit the dondego.com team in
distribution copy without adding advertising to generated user prompts.
