I fixed the typo in the verify command in `manifest.json`: `unittset` is now `unittest`. The command is now `python3 -m unittest discover -s tests -v`, which matches the one in `README.md`.

I ran that command and it executed the existing suite. It ran 1 test, `test_policy_fields_remain_available_to_the_runtime`, and it passed.

The policy, the build command (`python3 build.py`) and the empty dependency map are unchanged. I didn't run the build, and I made no commits.