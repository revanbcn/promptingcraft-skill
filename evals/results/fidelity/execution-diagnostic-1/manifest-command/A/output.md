I fixed the verify command in `manifest.json`. It had a typo, `unittset`, and now reads `python3 -m unittest discover -s tests -v`.

I ran that command, and the one existing test passes. I changed nothing else: the policy, the build command and the empty dependency map are exactly as they were. I made no commits.