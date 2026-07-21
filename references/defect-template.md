# Defect Report Template

```markdown
### 【严重程度】一句话标题（模块 + 现象）

- **缺陷ID**: （平台生成可空）
- **模块**: 
- **环境**: 测试 / 预发 / 生产（勿写内网真实敏感域名到公开渠道）
- **端**: Web / iOS / Android / Harmony / MiniProgram / API
- **严重程度**: 阻断 | 严重 | 一般 | 轻微
- **优先级**: P0 | P1 | P2 | P3
- **前置条件**: 
- **复现步骤**:
  1. 
  2. 
  3. 
- **预期结果**: 
- **实际结果**: 
- **出现频率**: 必现 / 高 / 偶发
- **附件建议**: 截图、录屏、请求/响应（脱敏）、日志关键字
- **初步定位**: 前端 / 后端 / 数据 / 配置 / 待查
```

## Severity guide

| Level | When |
|-------|------|
| 阻断 | Core path unusable; crash; data corruption; security breach |
| 严重 | Main feature wrong; no workaround; wrong entity data shown |
| 一般 | Secondary path; workaround exists; UI broken but task completable |
| 轻微 | Copy/pixel polish; rare edge; minor inconsistency |
