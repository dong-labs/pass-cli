# REPOS.md - 代码仓库索引

> **AI 优先阅读此文档** - 所有项目代码在 `repos/` 目录下

## 仓库映射

| 仓库 | 路径 | GitHub | 说明 |
|------|------|--------|------|
| **ThinkPlus** | `repos/ThinkPlus/` | maoruibin/ThinkPlus | inBox App (Android Kotlin) |
| **thinkflutter** | `repos/thinkflutter/` | maoruibin/thinkflutter | inBox PC版 (Flutter) |
| **dong-labs** | `repos/dong-labs/` | dong-labs/* | 咚咚家族 CLI 工具 |

## Issue 标签 → 仓库映射

| Issue 标签 | 仓库 | 技能 |
|------------|------|------|
| `inBox App` / `app` | ThinkPlus | analyze-issue, new-task, pre-release-scan |
| `inBox PC版` / `pc` | thinkflutter | analyze-issue, new-task |

## 处理 Issue 流程

```bash
# 1. 确定仓库（根据 Issue 标签）
# inBox App → cd repos/ThinkPlus
# inBox PC版 → cd repos/thinkflutter

# 2. 分析 Issue
/analyze-issue <issue_url_or_number>

# 3. 创建任务 + 分支
/new-task

# 4. 开发/修复

# 5. 提交 PR
git push && gh pr create
```

---

## 咚咚家族 CLI (dong-labs)

> 详细规范见 `repos/dong-labs/` 下的 README.md

| # | CLI | PyPI | 功能 |
|---|-----|------|------|
| 1 | `log-cli` | `dong-log` | 日志管理 |
| 2 | `read-cli` | `dong-read` | 知识管理 |
| 3 | `think-cli` | `dong-think` | 灵感管理 |
| 4 | `dida-cli` | `dong-dida` | 待办管理 |
| 5 | `cang-cli` | `dong-cang` | 财务管理 |
| 6 | `expire-cli` | `dong-expire` | 到期日管理 |
| 7 | `pass-cli` | `dong-pass` | 密码管理 |
| 8 | `timeline-cli` | `dong-timeline` | 时间线管理 |

---

## 配置文件

- **repos-config.json** - 机器可读的仓库配置
- **MEMORY.md** - 工作流说明