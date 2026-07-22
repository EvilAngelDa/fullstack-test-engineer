# Memory & Isolation（记忆与隔离）

## 1. 什么会进 GitHub / skill 包

| 允许 | 禁止 |
|------|------|
| `SKILL.md`、通用 references、stdlib scripts | **真实项目测试用例**（xlsx/csv/用例正文库） |
| 泛化 playbook 模式（无业务 ID、无客户名） | 个人 `$HOME` 下的 memory 文件 |
| `examples/` 虚构样例 | 内网 host、token、责任人真实 ID |

**别人 clone 本 skill 时：不会带走你的用例，也不会带走你的本地记忆。**

## 2. 本地记忆在哪

```text
$HOME/.fullstack-test-engineer/memory/<workspace-id>.md
```

- 由 `scripts/memory.py` 读写，**不在 skill 仓库内**（`memory/.gitkeep` 仅为占位）。
- `workspace-id` 由当前工作区 git remote / 路径哈希得到 → **同一项目工作区共享一份记忆**。
- **首次使用**：`snapshot` 的 `exists=false`、`common_patterns=[]` 是**正常状态**，不要报错，按空记忆开工。
- **他人机器**：各自 `$HOME` 下独立文件，互不影响。

## 3. 每次跑 skill 必须做什么

1. **Boot**：`memory.py snapshot` → 注入高计数模式（若有）。
2. **交付后强制**：`memory.py update` 写入 **2～8 条泛化经验**（见下）。
3. 可选：高频稳定模式再提议写入 `references/playbook.md`（需用户同意才改仓库）。

## 3.1 记忆与经验 **只增不删**（严格）

| 情况 | 必须怎么做 |
|------|------------|
| 新经验与旧经验 **无冲突** | **只追加**（或同义合并计数）。**禁止删除、覆盖、精简掉**旧 playbook / memory 条目。 |
| 新经验与旧经验 **有冲突** | **禁止自动删旧**。向用户列出：旧规则、新规则、冲突点；**等用户决定**再改。 |
| 改 SKILL checklist / playbook | 可新增章节与条目；重写时必须 **保留全部未冲突的旧细则**（禁止把强制明细收成一行导致内容丢失）。 |

`memory.py update` 本身是 merge 递增；agent **不得**手删 memory 文件条目或 playbook 历史规则来「腾地方」。

## 4. 记忆里写什么 / 不写什么

### 写（泛化经验）

- 分层规则、外显类型矩阵用法、显隐冲突处理方式  
- **模块关联**：同页模块顺序、共用参数、共享状态、联动显隐（用角色名而非真实用例 ID）  
- 可复用的缺口类型：「空串 vs 节点缺失要拆开测」  
- **场景分类**：风控成功空 data ≠ 网络异常 ≠ 4xx/5xx ≠ 错误数据/串号 ≠ 业务空列表；合并删除平台用例前先对场景

### 不写

- 完整用例步骤、预期原文、xlsx 内容  
- 用例编号（如 SUP-01）、客户车系 ID、内网 URL  
- 可识别的业务机密文案  

`memory.py` 会粗过滤 secret/路径；**agent 仍须主动泛化**。

## 5. 跨模块关联（务必记住）

同一产品页常有多模块（摘要卡、看板、参数区等），记忆应沉淀 **关联模式**，例如：

| 关联类型 | 记忆写法示例（泛化） |
|----------|----------------------|
| 页面顺序 | Module A is above Module B; FE cases should assert relative placement |
| 共用上下文 | Both modules bind same entity id; switching entity must refresh both without cross-talk |
| 显隐联动 | If core module hidden on API fail, sibling modules may still show — confirm per PRD |
| 接口族 | Sibling GET APIs share version/deviceType params — reuse required-param matrix |
| 文案/弹层 | Modal title FE-fixed + body from API is a recurring pattern |

Update 时使用 category：`CrossModule`（见 memory 分类）。

同一 workspace 内连续做多模块用例时：**先 snapshot**，把已有 CrossModule 模式带入下一模块设计。

## 6. 用例文件放哪

- 输出到**用户当前项目目录**（如 `deliverables/` 或用户指定路径）。  
- **永不** `write` 进 skill 安装目录或 skill git 仓库的 `examples/`（除非用户明确要求贡献虚构样例）。  
- 检查/补充文档可与用例同目录，同样不属于 skill 包。
