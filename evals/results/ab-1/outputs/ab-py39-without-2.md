```text
Drop Python 3.9 support. Limit changes strictly to setup.cfg and the CI Python-version matrix.

- In setup.cfg, raise python_requires from >=3.9 to >=3.10 and remove the Python 3.9 classifier, if present.
- Remove Python 3.9 from the CI matrix. Preserve every other version, matrix dimension, and workflow setting.
- Do not change source code, tests, documentation, dependencies, lockfiles, or unrelated formatting.

Inspect the existing configuration before editing. If it conflicts with these assumptions, report the conflict rather than widening the scope.

Review the final diff to confirm it contains only these changes, then summarize the edited files and validation performed.
```