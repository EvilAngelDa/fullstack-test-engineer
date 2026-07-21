# AGENTS.md — Loading `fullstack-test-engineer` on any agent

This file is for **OpenClaw, Codex, Hermes, Claude Code, Cursor, Copilot agents, Grok**, and other LLM coding agents.

## When to activate

Activate when the user asks for any of:

- test cases / 测试用例 / 接口用例 / 前端用例  
- requirement review / 需求疑问 / QA plan  
- bug report template filled from repro  
- `/fullstack-test` `/test-cases` `/qa`  

## Mandatory procedure

1. **Read** `SKILL.md` in this directory (same folder as this file) before writing cases.
2. **Resolve** `SKILL_ROOT` = this directory’s absolute path.
3. **Run** (best-effort):

   ```bash
   python3 "$SKILL_ROOT/scripts/memory.py" snapshot
   ```

4. **Classify** requirements into FE / API / CONTENT / NF. Honor user filters (e.g. frontend-only).
5. **Do not invent** business fixtures; emit 待补充信息清单.
6. **Write** deliverables to the **user project workspace**, not only chat.
7. **Upgrade memory** after delivery via `memory.py update` with privacy-safe patterns.
8. If user will publish artifacts: run `scrub_privacy.py --path <artifacts> --report`.

## Tool permissions needed

| Need | Why |
|------|-----|
| Read files | PRD, API, screenshots, templates |
| Write files | Cases md/xlsx under workspace |
| Shell | `python3 scripts/*.py` |
| Network | Optional; only if user asks live API probe |

No privileged deploy or secret access required.

## Output contract

Every completed run should include:

1. Paths of generated files  
2. Case counts by priority  
3. Layer filter applied  
4. Open questions list  
5. Memory update summary  
6. Privacy scan summary if publishing  

## Anti-patterns (do not)

- Dumping only abstract “test points” without steps/expects  
- Mixing content-generation quality suites into FE-only requests  
- Hardcoding private hostnames, tokens, or personal paths into cases  
- Writing exploits or attack payloads beyond basic injection **strings** for negative input tests  

## Skill path discovery

If the skill is installed as a git submodule or sibling folder:

```text
<workspace>/fullstack-test-engineer/SKILL.md
```

If user-global:

```text
~/.grok/skills/fullstack-test-engineer/SKILL.md
~/.claude/skills/fullstack-test-engineer/SKILL.md   # if mirrored
```

Prefer the path the user names; otherwise search for `fullstack-test-engineer/SKILL.md`.
