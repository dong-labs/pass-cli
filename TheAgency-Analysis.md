# The Agency 项目分析报告

> 研究对象：https://github.com/msitarzewski/agency-agents
> 日期：2026-03-17

---

## 1. 项目概览

| 项目 | 信息 |
|------|------|
| **名称** | The Agency |
| **Star** | 50,124 ⭐ |
| **描述** | 完整的 AI 代理机构 - 各类专业 AI Agent 集合 |
| **许可** | MIT |
| **创建时间** | 2025-10-13 |
| **语言** | Shell (脚本) |
| **主要分类** | Engineering, Design, Marketing, Sales, Product, PM, Testing, Support, Spatial Computing, Specialized |

---

## 2. Agent 设计规范 ⭐⭐⭐

### 2.1 YAML Frontmatter 格式

```yaml
---
name: Agent Name
description: One-line description
color: cyan
emoji: 🖥️
vibe: One-line personality hook
services:
  - name: Service Name
    url: https://...
    tier: free
---
```

### 2.2 Agent 结构

```
# Agent Name

## 🧠 Your Identity & Memory
- Role
- Personality
- Memory
- Experience

## 🎯 Your Core Mission
- Primary responsibilities with deliverables

## 🚨 Critical Rules You Must Follow
- Domain-specific constraints

## 📋 Your Technical Deliverables
- Code samples
- Templates
- Documents

## 🔄 Your Workflow Process
- Step-by-step process

## 💭 Your Communication Style
- How communicates
- Example phrases

## 🔄 Learning & Memory
- What learns from
- What remembers

## 🎯 Your Success Metrics
- Quantitative metrics
- Qualitative indicators

## 🚀 Advanced Capabilities
- Specialized techniques
```

### 2.3 设计原则

| 原则 | 说明 |
|------|------|
| **🎭 Strong Personality** | 有个性、有声音、不通用 |
| **📋 Clear Deliverables** | 提供具体代码示例、模板 |
| **✅ Success Metrics** | 可衡量的成功指标 |
| **🔄 Proven Workflows** | 经过实战测试的工作流 |
| **💡 Learning Memory** | 能学习、能记住 |

---

## 3. 社区建设 ⭐⭐⭐

### 3.1 CONTRIBUTING.md 的详细程度

**优点：**
- ✅ Code of Conduct
- ✅ 如何贡献（4 种方式）
- ✅ 完整的 Agent 设计模板
- ✅ Agent 设计原则（5 条）
- ✅ Pull Request 流程
- ✅ PR Template
- ✅ Style Guide（写作风格、格式、代码示例、Tone）
- ✅ Recognition 机制（贡献者致谢）

**可借鉴：**
1. **PR 流程清晰** - 明确什么可以 PR，什么需要先讨论
2. **风格指南详细** - 包括代码示例格式
3. **贡献者致谢** - 鼓励社区参与

---

## 4. 多工具支持 ⭐⭐⭐

### 4.1 convert.sh 脚本功能

**支持的工具：**
```
antigravity  — Antigravity skills
gemini-cli   — Gemini CLI extension
opencode     — OpenCode agent files
cursor       — Cursor rule files
aider        — CONVENTIONS.md
windsurf     — .windsurfrules
openclaw     — OpenClaw SOUL.md
qwen         — Qwen SubAgent files
```

### 4.2 OpenClaw 集成方式

**输入：** Markdown Agent 文件（与咕咚 Agent Hub 格式兼容）

**输出：**
```
integrations/openclaw/<agent-slug>/
└── SOUL.md              # 人格部分
└── AGENTS.md            # 操作部分
```

**转换逻辑：**
- 根据 header 关键字分类
- SOUL 关键字：identity, memory, communication, style, critical rules
- AGENTS 关键字：mission, deliverables, workflow, metrics, advanced

**优点：**
- ✅ 自动化转换，不需要手动调整
- ✅ 统一格式，适合不同工具
- ✅ 支持 OpenClaw

---

## 5. Agent 文档质量 ⭐⭐

### 5.1 示例 Agent：Frontend Developer

**优点：**
- ✅ 完整的结构（Identity、Mission、Rules、Deliverables、Workflow、Style、Learning、Metrics、Capabilities）
- ✅ 真实可运行的代码示例（React Component）
- ✅ 具体的成功指标（Lighthouse 90+）
- ✅ 清晰的工作流（4 个阶段）
- ✅ 实用的交付物模板

### 5.2 示例 Agent：Reddit Community Builder

**优点：**
- ✅ 强烈的个性（"Fluent in Reddit culture"）
- ✅ 具体数字指标（10,000+ karma, 85%+ upvote）
- ✅ Reddit 特定规则（90/10 Rule）
- ✅ 实战工作流

**可借鉴：**
1. **代码示例质量高** - 真正可运行的代码，不是伪代码
2. **指标具体化** - 10,000+ karma, 85%+ upvote，不是模糊的"做得好"
3. **交付物实用** - 有具体的模板、文档

---

## 6. 项目结构 ⭐⭐

```
agency-agents/
├── .github/
│   └── workflows/
│       └── lint-agents.yml
├── academic/           # 学术相关
├── design/             # 设计类
├── engineering/        # 工程类 ⭐
├── examples/           # 示例
├── game-development/   # 游戏开发
├── integrations/       # 集成文件（转换后）
├── marketing/          # 营销类 ⭐
├── paid-media/         # 付费媒体
├── product/            # 产品类 ⭐
├── project-management/ # 项目管理 ⭐
├── sales/              # 销售类 ⭐
├── scripts/            # 脚本 ⭐
│   ├── convert.sh
│   ├── install.sh
│   └── lint-agents.sh
├── spatial-computing/  # AR/VR
├── specialized/        # 特殊领域
└── testing/            # 测试类 ⭐
```

**分类特点：**
- ✅ 按领域清晰分类
- ✅ 覆盖面广（学术、设计、游戏、营销、销售、产品、PM、测试、支持、AR/VR）
- ✅ scripts/ 目录负责工具链

---

## 7. 用户体验 ⭐⭐

### 7.1 安装流程

```bash
# 1. 克隆项目
git clone https://github.com/msitarzewski/agency-agents.git

# 2. 转换格式
./scripts/convert.sh

# 3. 安装到工具
./scripts/install.sh [--tool <name>]
```

### 7.2 install.sh 功能

**特点：**
- ✅ 自动检测已安装的工具
- ✅ 支持并行安装
- ✅ 显示进度条
- ✅ 支持 all（所有检测到的工具）

**安装位置：**
- OpenClaw: `~/.openclaw/agency-agents/`
- Claude Code: `~/.claude/agents/`
- Cursor: `.cursor/rules/`

---

## 8. 值得学习的亮点 ⭐⭐⭐

### 8.1 多工具集成系统

**优势：**
1. **统一格式** - Markdown Agent 文件，一份内容多平台使用
2. **自动化转换** - convert.sh 脚本自动适配不同工具格式
3. **易于扩展** - 新增工具只需写转换逻辑
4. **用户友好** - 一键安装，自动检测

**可借鉴到咚咚家族：**
- 把仓咚咚、阅咚咚等 Agent 转换成 The Agency 格式
- 自动转换适配 Cursor、Windsurf、Claude Code 等工具
- 方便用户在不同工具中使用咚咚家族

### 8.2 Agent 设计模板

**优势：**
1. **结构化** - 清晰的章节划分
2. **可执行** - 有代码示例、模板、工作流
3. **可衡量** - 有具体指标
4. **可扩展** - Advanced Capabilities 留空间

**可借鉴到咕咚 Agent Hub：**
- 用他们的模板重新设计仓咚咚 Agent
- 增加具体指标（不是模糊的"做得好"）
- 增加代码示例（如果适用）

### 8.3 社区建设

**优势：**
1. **贡献指南详细** - CONTRIBUTING.md 很完整
2. **PR 流程清晰** - 明确什么可以 PR，什么需要讨论
3. **风格指南详细** - 包括代码格式、Tone
4. **贡献者致谢** - 鼓励社区参与

**可借鉴到咚咚家族：**
- 写详细的 CONTRIBUTING.md
- 设计清晰的贡献流程
- 写一个类似 Style Guide 的文档

### 8.4 文档质量

**优势：**
1. **示例完整** - Frontend Developer Agent 有完整的代码示例
2. **指标具体** - 10,000+ karma, 85%+ upvote
3. **实用性强** - 有具体的模板、工作流

**可借鉴到咕咚：**
- 把仓咚咚 Agent 的文档写得像他们一样详细
- 增加具体的使用场景和指标

---

## 9. 咚咚家族可以借鉴的地方

### 9.1 短期（直接借鉴）

| 借鉴项 | 具体做法 |
|--------|----------|
| **Agent 格式** | 用他们的 YAML frontmatter + Markdown 格式 |
| **Agent 结构** | 复制他们的章节结构（Identity、Mission、Deliverables、Workflow、Metrics） |
| **多工具支持** | 写一个 convert.sh，适配 Cursor、Windsurf、Claude Code |
| **文档质量** | 增加代码示例、具体指标、实用模板 |

### 9.2 中期（社区建设）

| 借鉴项 | 具体做法 |
|--------|----------|
| **CONTRIBUTING.md** | 写一份详细的贡献指南 |
| **Style Guide** | 写一个咚咚家族的写作风格指南 |
| **PR 流程** | 设计清晰的贡献流程 |
| **社区运营** | 建立 GitHub Discussions、Write "Agent of the Week" |

### 9.3 长期（生态系统）

| 借鉴项 | 具体做法 |
|--------|----------|
| **Agent 市场** | 建立咚咚 Agent 市场，用户可以贡献 Agent |
| **社区评审** | 建立 Agent 评审机制 |
| **教程体系** | 写教程，教用户如何贡献 Agent |
| **荣誉系统** | 建立贡献者荣誉体系 |

---

## 10. 需要注意的差异

| 差异 | 说明 |
|------|------|
| **咕咚 vs The Agency** | 咕咚是个人助手系统，The Agency 是专业 Agent 集合 |
| **CLI 依赖** | 咚咚家族每个 Agent 有 CLI，The Agency 没有 |
| **个性化** | 咕咚是为咕咚定制的，The Agency 是通用的 |
| **规模** | The Agency 60+ Agent，咕咚 5 个 Agent |

---

## 11. 总结

### 核心优点

1. **多工具集成系统** - 自动转换，用户友好
2. **Agent 设计模板** - 结构化、可执行、可衡量
3. **社区建设完善** - CONTRIBUTING.md、PR 流程、风格指南
4. **文档质量高** - 完整示例、具体指标、实用模板

### 咚咚家族可以快速落地的点

1. **格式转换** - 写 convert.sh 适配 Cursor、Windsurf
2. **文档升级** - 用他们的模板重写仓咚咚 Agent
3. **贡献指南** - 写一份 CONTRIBUTING.md

### 咚咚家族需要长期建设的点

1. **社区** - 建立讨论区、贡献流程
2. **市场** - Agent 贡献和共享机制
3. **生态系统** - 外部工具集成

---

**报告完成时间**：2026-03-17
**下一步**：等你休息的时候讨论如何应用到咚咚家族
