I fixed the `verify` command in `manifest.json`. It had a typo, `unittset`, and now reads `python3 -m unittest discover -s tests -v`.

I ran that command and the one test in the suite passed.

I didn't touch the `policy` block, the `build` command or the empty `dependencies` map. I made no commits.