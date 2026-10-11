# Source maintenance

Three different objects: versioned skill instructions; external knowledge used
for a particular task; read-only checks for changes to that knowledge. No
scheduled operation rewrites instructions, opens MRs, merges or publishes.

The standalone skill contains [sources.json](../skills/promptcraft/references/sources.json).
Each source has provider, canonical URL, role, applicability and refresh policy.
Official root/product indexes discover newly relevant candidate links instead
of only watching yesterday's guides. Candidates need manual content/applicability
review before adding them or changing skill behavior.

Python 3.11+ stdlib utility:

```sh
python3 scripts/freshness.py --output /tmp/promptcraft-freshness --write-baseline
```

Output: readable `freshness.md`, machine-readable `freshness.json`, and optionally
`baseline-proposed.json`. Raw documents are not stored. Review a proposed baseline
before replacing `sources-baseline.json`; a comparison never mutates the tracked
baseline. Baselines contain hashes, URLs, HTTP validators, candidate links and
observation times only. Failed sources retain their last successful baseline.

States: `new` (no known baseline), `unchanged`, `changed`, `unavailable` (HTTP
response without docs), `error` (invalid content, policy or transport failure).
Index `new_candidates`/`removed_candidates` and `removed_from_registry` are distinct
from withdrawn guidance; inaccessible pages and missing links never prove withdrawal.
The run reports `complete`, `partial` or `error`; partial/error returns exit 2.
Changed/new content is a review signal, not a code-test failure.

Bounds: at most 32 configured pages, 1 MiB each, 15-second socket timeout,
4 redirects per source, explicit error above 5,000 candidate links (no silent
200-link truncation), 180-second run budget between requests, no automatic
retries. The run-budget check occurs between requests; a slow active request can
extend wall time. ETag/Last-Modified are used when supplied; 304 requires a usable
baseline. HTTP fetch times, Last-Modified and source publication/update dates are
separate fields. Publication/update dates remain null when unestablished.

Only explicit public HTTPS host/path policies are fetched, without cookies,
credentials, proxy configuration or private task data. Each redirect is validated;
IP literals, non-public DNS results, credentials, queries and abnormal paths are
refused. Host policies and DNS checks reduce SSRF risk, but are not a hardened
network sandbox against DNS rebinding; don't expose this utility as a service.
Usable normalized text is required; binary, oversized, empty and access-challenge
responses are errors. Scripts/navigation are excluded from HTML hashing where
possible. Markup/layout changes can still produce false-positive drift.

All downloaded content is untrusted data, never executable instructions or
permission to change the skill, disclose secrets or weaken restrictions. Reports
contain metadata, not provider prose. Keep private traces/caches outside Git;
`reports/`, `.cache/`, `dist/` are ignored locally. CI artifacts are public metadata
and archives only. Synthetic fixture tests need no network.

## GitLab jobs and schedule

`verify` is the required offline merge check. `freshness` is a separate manual
job, automatic only in scheduled pipelines; outages do not masquerade as failing
merge checks. Schedule configuration: main branch, `17 6 * * *`, timezone UTC.

Daily schedule: **prepared but disabled** unless the delivery receipt confirms
otherwise. Existing runner availability alone does not establish permission or
remaining included compute quota. Activation requires verifying existing owner
policy and sufficient included runner allowance for one bounded check daily,
without purchases, new credentials or runner provisioning. No claim of background
monitoring follows from this YAML alone. Schedule ID 4486529 was created with `active=false`; namespace API identified
the Free plan but did not establish remaining included compute allowance.
Actual manual job
results belong in the release receipt.
