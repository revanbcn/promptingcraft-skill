I fixed the verify command in `manifest.json`. It had a typo, `unittset`, and now reads `python3 -m unittest discover -s tests -v`. That matches the command in README.md.

I ran that command, and it executed the existing suite (one test):

```
test_policy_fields_remain_available_to_the_runtime (test_contract.Smoke.test_policy_fields_remain_available_to_the_runtime) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```

The typo was the only edit. These are unchanged:
- **Policy:** `{"schema":1,"fields":["job_id","status"],"terminal":"failed_final"}`
- **Build command:** `python3 build.py`
- **Dependency map:** `{}`

I made no commits, deployed nothing and added no dependencies.