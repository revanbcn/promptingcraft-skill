The verify command in `manifest.json` now runs the existing unittest suite, and the suite passes.

**Cause:** the module name was misspelled as `unittset`, so Python couldn't find it.

- **Old verify command:** `python3 -m unittset discover -s tests -v`
- **New verify command:** `python3 -m unittest discover -s tests -v`

I ran the new command exactly as written in the README. This is the output:
```
test_policy_fields_remain_available_to_the_runtime (test_contract.Smoke.test_policy_fields_remain_available_to_the_runtime) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```

I changed only that one word. The policy, the build command (`python3 build.py`) and the dependency map (`{}`) are untouched. I didn't commit or deploy anything. I didn't run the build command, since it wasn't part of the task and the sandbox only allows the unittest command.