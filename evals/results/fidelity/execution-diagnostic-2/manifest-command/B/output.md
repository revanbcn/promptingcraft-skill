The verify command in `manifest.json` had a typo, `unittset` instead of `unittest`. I fixed it, and it now runs the existing suite in `tests/`.

- **New verify command:** `python3 -m unittest discover -s tests -v`. It matches the command in `README.md`.
- **Command I ran:** that same command, from the work directory. I ran the command text directly rather than launching it through the manifest.
- **Result:** 1 test ran (`test_contract.Smoke.test_policy_fields_remain_available_to_the_runtime`) and it passed, with `OK`.

I changed only that one word. The policy `{"schema":1,"fields":["job_id","status"],"terminal":"failed_final"}`, the build command `python3 build.py` and the empty dependency map `{}` are untouched. I didn't run the build command, and there's no `build.py` in the directory. I didn't commit anything.