I fixed the verify command in `manifest.json`. It had a typo, `unittset`, which I changed to `unittest`. It now reads `python3 -m unittest discover -s tests -v`.

I ran that command and the one test in the suite passed. I didn't touch the build command, the dependency map or the policy, and I made no commits.