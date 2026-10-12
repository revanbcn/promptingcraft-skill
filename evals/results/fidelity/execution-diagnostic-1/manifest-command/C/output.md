I fixed the verify command in `manifest.json`. It had a typo, `unittset`, so Python couldn't find the module. It now reads `python3 -m unittest discover -s tests -v`. That is the same command the README gives, and the existing suite is in `tests/` (`test_contract.py`).

I ran that command. I didn't run the manifest's string through a shell separately, but the two are identical:

```
test_policy_fields_remain_available_to_the_runtime (test_contract.Smoke.test_policy_fields_remain_available_to_the_runtime) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```

I left these parts of `manifest.json` untouched:
- **Policy:** `{"schema":1,"fields":["job_id","status"],"terminal":"failed_final"}`.
- **Build command:** `python3 build.py`.
- **Dependency map:** `{}`.

I didn't commit or deploy anything.