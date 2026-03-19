# Agent Hub CLI - 会议执行摘要

## 📋 决策概览

### 技术选型

| 组件 | 选择 | 理由 |
|------|------|------|
| 语言 | **Python** | 与 OpenClaw 技术栈一致 |
| CLI 框架 | **Click/Typer** | 成熟、类型安全 |
| Registry | **Git 仓库** | 复用 ClawHub 基础设施 |
| 存储位置 | **~/.agenthub/** | 用户本地配置 |

### 架构

```
┌─────────────────────────────────┐
│   CLI Commands (Click)          │  ← 用户交互层
├─────────────────────────────────┤
│   Core Logic                    │  ← 业务逻辑层
│   - Registry (搜索/获取)         │
│   - Validator (格式验证)         │
│   - Installer (依赖安装)         │
├─────────────────────────────────┤
│   Adapters                      │  ← 适配层
│   - Git Registry                │
│   - pip/npm/cargo/go 安装器      │
└─────────────────────────────────┘
```

### 命令结构

```bash
# 用户命令
agenthub search <keyword>      # 搜索
agenthub info <agent-id>       # 详情
agenthub install <agent-id>    # 安装
agenthub list                  # 列表
agenthub update <agent-id>     # 更新
agenthub uninstall <agent-id>  # 卸载

# 作者命令
agenthub init <name>           # 初始化包
agenthub validate              # 验证格式
agenthub package               # 打包
agenthub publish               # 发布
```

## 🎯 开发计划

### Phase 1: MVP (2周)

| 任务 | 优先级 |
|------|--------|
| agent.yaml v1 规范定义 | P0 |
| init/validate/package 命令 | P0 |
| Git Registry 操作 | P0 |
| install 命令 | P0 |

### Phase 2: 完整版 (4周)

| 任务 | 优先级 |
|------|--------|
| search 命令 | P1 |
| 依赖自动安装器 | P1 |
| 测试覆盖 | P1 |
| OpenClaw 集成 | P2 |
| 文档 | P2 |

## 📦 项目结构

```
agenthub/
├── cli.py                  # 入口
├── commands/               # 命令实现
├── core/                   # 核心逻辑
│   ├── registry.py
│   ├── agent.py
│   ├── installer.py
│   └── validator.py
├── models/                 # 数据模型
├── config.py               # 配置
└── utils/                  # 工具函数
```

## ⚠️ 风险与对策

| 风险 | 对策 |
|------|------|
| 依赖安装安全 | 默认显示命令确认，支持 --yes |
| Registry 实时性 | v1 用 Git，v2 考虑 API |
| 跨平台兼容 | 测试 Windows/macOS/Linux |

## ✅ 下一步行动

1. **立即** - 定义 `agent.yaml v1` 规范文档
2. **本周** - 搭建项目框架，实现 init/validate 命令
3. **下周** - 实现 Git Registry 操作和 install 命令

---

**详细会议记录：** [meeting-2026-03-15.md](./meeting-2026-03-15.md)
