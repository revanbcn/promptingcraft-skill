I fixed the verify command in `manifest.json`. It had a typo, `unittset`, which I changed to `unittest`. It now reads `python3 -m unittest discover -s tests -v`.

I ran that command locally. It found and ran the existing suite, which is 1 test (`test_policy_fields_remain_available_to_the_runtime`), and it passed.

I left the build command, the dependency map and the policy `{"schema":1,"fields":["job_id","status"],"terminal":"failed_final"}` as they were. I made no commits.