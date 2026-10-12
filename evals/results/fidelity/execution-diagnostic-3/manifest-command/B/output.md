I fixed the verify command in `manifest.json`. It had a typo, `unittset`, and now reads `python3 -m unittest discover -s tests -v`.

The build command, the empty dependency map and the policy are unchanged. The policy is still `{"schema":1,"fields":["job_id","status"],"terminal":"failed_final"}`.

I ran the command from the README, which is the same as the repaired verify command. It ran the existing suite in `tests/test_contract.py`, and the test passed:

```
test_policy_fields_remain_available_to_the_runtime (test_contract.Smoke.test_policy_fields_remain_available_to_the_runtime) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```

`manifest.json` is the only file I changed. I made no commits.