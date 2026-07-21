# Full-Stack Test Engineer Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skill](https://img.shields.io/badge/Agent-Skill-blue)](#install)
[![Privacy](https://img.shields.io/badge/Privacy-scrubbed-green)](references/privacy-redaction.md)

A portable **AI agent skill** that turns product requirements, API docs, and UI prototypes into **executable QA deliverables**: requirement gap lists, API cases, frontend functional cases, defect reports, and light perf/security checklists.

Designed for multi-agent use: **Grok**, **Codex**, **OpenClaw**, **Hermes**, **Claude Code**, **Cursor**, and similar tools that can load a `SKILL.md` (or follow `AGENTS.md`).

---

## Why this skill

Most agents dump generic test ideas. This skill enforces a **senior QA workflow**:

| Habit | Behavior |
|-------|----------|
| No hallucination of fixtures | Missing business data → **待补充信息清单**, not invented expects |
| Layer split | Auto-separate **Frontend / API / Content / NF** |
| Template-native cases | Columns compatible with common case-import Excel |
| Experience upgrade | Local memory of generalized patterns across runs |
| Publish-safe | Privacy scanner before GitHub |

---

## What’s included

```text
fullstack-test-engineer/
├── SKILL.md                 # Agent instructions (entry)
├── AGENTS.md                # Multi-agent load guide
├── README.md                # This file
├── LICENSE
├── references/              # Templates, matrix, playbook, privacy
├── scripts/
│   ├── memory.py            # Experience memory (snapshot/update)
│   ├── scrub_privacy.py     # Pre-publish privacy scan
│   └── write_cases_xlsx.py  # Excel exporter (openpyxl)
├── examples/                # Fictional sample API + FE requirements
└── memory/                  # Placeholder (runtime memory is under $HOME)
```

Runtime learning data is stored **outside the repo**:

```text
$HOME/.fullstack-test-engineer/memory/<workspace-id>.md
```

so clones stay clean and privacy-safe.

---

## Install

### Option A — Grok (user skill)

```bash
git clone https://github.com/EvilAngelDa/fullstack-test-engineer.git \
  ~/.grok/skills/fullstack-test-engineer
```

Then invoke: `/fullstack-test` or ask for 测试用例 / 接口用例 / 前端用例.

### Option B — Claude Code / Cursor

Copy or clone into the project or user skills directory your tool uses (often `.claude/skills/`, `.cursor/skills/`, or docs-specified path). Ensure the agent is allowed to read `SKILL.md` and run `scripts/*.py`.

### Option C — Codex / OpenClaw / Hermes / generic agents

1. Clone this repository next to your project (or as a submodule).
2. Add to agent instructions (see [AGENTS.md](./AGENTS.md)):

```text
When the user asks for test cases, QA analysis, or /fullstack-test:
1. Read ./fullstack-test-engineer/SKILL.md
2. Follow it end-to-end
3. Prefer scripts under ./fullstack-test-engineer/scripts/
```

### Python deps (for Excel export)

```bash
pip install openpyxl
```

`memory.py` and `scrub_privacy.py` use **stdlib only**.

---

## Quick start (for humans or agents)

1. Collect inputs: PRD, API doc, screenshot/prototype, optional case template.
2. Tell the agent, for example:

```text
按 fullstack-test-engineer skill：
- 只写前端功能用例
- 模版列与 examples 一致
- 输出 xlsx + 疑问清单
附件：需求.md、样式.png
```

3. Agent should:
   - `memory.py snapshot` (load past patterns)
   - Classify FE vs API vs content
   - Write cases + gap list
   - `memory.py update` (learn)
   - `scrub_privacy.py` if publishing

### Manual script demos

```bash
# Memory snapshot
python3 scripts/memory.py snapshot

# Privacy scan (run from skill root)
python3 scripts/scrub_privacy.py --path . --report

# Write xlsx from JSON
python3 scripts/write_cases_xlsx.py --out /tmp/demo_cases.xlsx --cases-json - <<'JSON'
{
  "cases": [
    {
      "name": "【展示】有数据时展示结论卡片",
      "module": "/Demo/Frontend/Summary",
      "tags": "前端;功能;P0",
      "precondition": "接口返回非空结论",
      "steps": [
        {"action": "进入详情页", "expected": "展示标题与正文"},
        {"action": "点击正文非展开区域", "expected": "不发生跳转"}
      ],
      "mode": "STEP",
      "level": "P0"
    }
  ]
}
JSON
```

---

## Deliverables the skill can produce

1. **需求疑问清单** — ambiguities, conflicts, missing boundaries  
2. **测试方案/计划** — short and executable  
3. **测试用例** — Markdown + optional Excel  
4. **缺陷报告** — severity template  
5. **兼容 / 简易性能 / 基础安全** checklist  
6. **上线验收 / 巡检** list  

---

## Auto-upgrade (experience memory)

After each successful run, the agent writes **generalized** patterns (no hosts, tokens, PII):

```bash
python3 scripts/memory.py update <<'JSON'
{
  "patterns": [
    {"category": "Frontend", "description": "Reset expand state when switching entity context"},
    {"category": "API", "description": "Test missing and empty-string required query params separately"}
  ],
  "run": {
    "description": "FE expand-collapse module",
    "deliverables": ["fe-cases"],
    "key_patterns": ["Hide whole module on API failure"]
  }
}
JSON
```

Stable patterns can be promoted into [`references/playbook.md`](references/playbook.md).

---

## Privacy & public GitHub

This repository is intended to be **public-safe**:

- Examples use `api.example.com` and fictional IDs only  
- No company internal gateways, employee paths, or live tokens  
- Use `scripts/scrub_privacy.py` before every push of generated artifacts  

See [references/privacy-redaction.md](references/privacy-redaction.md).

> If you generated cases from **private** PRDs, keep those xlsx/md in a private repo or redact before attaching here.

---

## Compatible agents

| Agent | How to hook |
|-------|-------------|
| Grok | `~/.grok/skills/fullstack-test-engineer` |
| Claude Code | Project/user skill dir + read SKILL.md |
| Codex CLI | Instruction file + path to SKILL.md |
| OpenClaw | Skill/plugin path → this folder |
| Hermes | Agent toolkit / skill manifest pointing here |
| Cursor | Rules or skills: “read SKILL.md on QA tasks” |

---

## Versioning

- Skill version: see `metadata.version` in `SKILL.md`  
- Breaking changes to case columns or memory schema → bump minor/major and note in playbook  

---

## License

MIT — see [LICENSE](./LICENSE).

## Contributing

1. Keep examples fictional  
2. Run `python3 scripts/scrub_privacy.py --path . --report`  
3. Prefer generalized playbook entries over project anecdotes  
4. PRs that add agent adapters (OpenClaw manifest, Codex pack) are welcome  

---

## Disclaimer

This skill helps structure QA work. It does **not** replace human sign-off for release, security audits, or compliance. Do not use it to generate attack exploits or to process unlawful personal data.
