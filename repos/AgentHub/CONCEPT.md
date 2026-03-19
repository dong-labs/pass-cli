# Agent Hub - 智能体市场

> 完整人格 + 能力 + 数据的 Agent 分发平台

---

## 定位

| 平台 | 粒度 | 内容 |
|------|------|------|
| ClawHub | 技能 | 单一能力 |
| **Agent Hub** | 智能体 | 完整人格 + 能力 + 数据 |

---

## Agent 包结构

```
my-agent/
├── agent.yaml           # 元信息
├── IDENTITY.md          # 身份
├── SOUL.md              # 性格
├── TOOLS.md             # 能力
├── WORKFLOW.md          # 工作流（可选）
├── MEMORY.md.template   # 记忆模板
├── USER.md              # 用户画像模板
├── skills/              # 技能包（可选）
├── avatar.png           # 头像
└── README.md            # 介绍
```

---

## agent.yaml 规范

```yaml
name: 仓咚咚
id: cang
version: 1.0.0
author: gudong
description: 帮你管钱的小仓鼠
emoji: 🐹

# 依赖
cli:
  package: cang-cli
  version: ">=0.1.0"

# 分类
tags:
  - finance
  - personal

# 运行环境
runtime:
  - openclaw
```

---

## CLI 命令

```bash
# 搜索
agenthub search finance

# 安装
agenthub install cang

# 列出已安装
agenthub list

# 更新
agenthub update cang

# 发布
agenthub publish ./my-agent
```

---

## 用户安装流程

```bash
agenthub install cang
```

自动完成：
1. 检查 CLI 依赖 → `pip install cang-cli`
2. 下载 Agent 包 → `~/.openclaw/agents/cang/`
3. 创建用户文件 → `MEMORY.md`（从模板）

---

## 与 ClawHub 关系

- 复用 ClawHub 的发布/分发基础设施
- Agent 可以包含多个 skill
- 独立的搜索和分类体系

---

*待续...*
