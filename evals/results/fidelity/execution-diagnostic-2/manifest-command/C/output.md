I fixed the verify command in `manifest.json`. It had a typo, `unittset`, which I changed to `unittest`. It now reads `python3 -m unittest discover -s tests -v`.

I ran that command, and the one test in `tests/test_contract.py` passed. The output was:

```
test_policy_fields_remain_available_to_the_runtime (test_contract.Smoke.test_policy_fields_remain_available_to_the_runtime) ... ok

Ran 1 test in 0.000s

OK
```

I left the policy, the build command and the dependency map as they were. I made no commits.