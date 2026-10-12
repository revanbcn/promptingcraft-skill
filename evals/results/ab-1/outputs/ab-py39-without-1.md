```text
Drop Python 3.9 support with the smallest possible diff.

Scope:
- setup.cfg: remove the Python 3.9 classifier and raise the minimum supported Python version to 3.10, preserving any other version constraints.
- CI configuration: remove Python 3.9 from the test matrix, preserving all remaining versions and job settings.

Change nothing else. Do not modify application code, dependencies, tests, documentation, changelogs, or unrelated configuration. Do not refactor or reformat surrounding content.

Verify the configuration changes and confirm the diff contains only these edits. Summarize the changed files and validation performed.
```