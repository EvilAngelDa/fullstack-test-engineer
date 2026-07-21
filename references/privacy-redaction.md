# Privacy Redaction Rules (Publish / Share)

Before pushing this skill or generated cases to a **public** GitHub repo, scrub:

## Always remove or replace

| Kind | Example | Replace with |
|------|---------|--------------|
| Absolute home paths | `/Users/alice/projects/...` | `/Users/you/...` or relative paths |
| Internal hosts | `*.corp`, `*.internal`, private mesh gateways | `https://api.example.com` |
| Real production customer domains (if confidential) | company-only endpoints | fictional example hosts |
| Tokens / passwords / API keys | any live secret | `<redacted>` / env var name |
| Personal email / phone | real PII | `user@example.com` |
| Employee IDs used as 责任人 | real platform ids | leave empty |
| Customer raw dumps | real user content | fictional samples |

## Safe to keep

- Generic field names (`seriesId`, `returncode`)
- Fictional sample IDs (`66`, `sample-001`)
- Public standard error shapes
- Generalized process patterns in memory

## Commands

```bash
# From skill root
python3 scripts/scrub_privacy.py --path . --report

# Optional redacted siblings
python3 scripts/scrub_privacy.py --path ./deliverables --write-redacted --report
```

Exit code `2` means **HIGH** findings — do not publish until fixed.

## Memory hygiene

`scripts/memory.py` rejects obvious secrets in pattern text, but **you** must still generalize:

- Bad: `Hide module when agentchat.example-corp fails`
- Good: `Hide module when conclusion API fails or returns empty data`
