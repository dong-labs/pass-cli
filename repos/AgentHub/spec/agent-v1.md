# Agent Package Specification v1

> 通用智能体包规范

---

## 设计原则

| 原则 | 说明 |
|------|------|
| **通用优先** | 不绑定特定平台，任何 AI Agent 平台均可采用 |
| **人类友好** | 简洁直观，打开就能理解 |
| **程序可解析** | 结构化数据，易于自动化处理 |
| **渐进增强** | 核心字段必需，扩展字段可选 |
| **向后兼容** | v1 之后保持兼容性 |

---

## 包结构

```
my-agent/
├── agent.yaml           # ★ 元信息（必需）
├── IDENTITY.md          # ★ 身份描述（必需）
├── SOUL.md              # ★ 性格设定（必需）
├── CAPABILITIES.md      # ★ 能力描述（必需）
├── MEMORY.template.md   #   记忆模板（推荐）
├── README.md            #   介绍文档（推荐）
├── icon.png             #   图标（推荐，32x32+）
├── assets/              #   资源文件（可选）
└── scripts/             #   安装脚本（可选）
```

★ = 必需文件

---

## agent.yaml 格式

### 最小示例

```yaml
spec: agent/v1
name: 仓咚咚
id: cang
version: 1.0.0
author: gudong
```

### 完整示例

```yaml
# ===== 规范版本 =====
spec: agent/v1

# ===== 基本信息 =====
name: 仓咚咚
id: cang
version: 1.0.0
author: gudong
license: MIT
description: 帮你管钱的小仓鼠，记账、分析、提醒
homepage: https://github.com/gudong/cang-agent

# ===== 展示 =====
icon: assets/icon.png
emoji: 🐹
color: "#F5A623"
tags:
  - finance
  - personal
  - productivity

# ===== 运行时兼容性 =====
runtime:
  # 兼容的平台/框架
  compatible:
    - openclaw >= 0.5.0
    - coze
    - dify
  # 必需的能力
  requires:
    - file_io
    - command_execution

# ===== 能力依赖 =====
capabilities:
  # CLI 依赖
  cli:
    - package: cang-cli
      version: ">=0.1.0"
      install: pip install cang-cli
      optional: false

  # API 依赖
  api:
    - name: openai
      version: ">=1.0.0"
      optional: true

  # 文件能力
  files:
    - read: ["~/Documents/finance/**"]
    - write: ["~/Documents/finance/reports/**"]

# ===== 人格配置 =====
personality:
  # 性格特征
  traits:
    - diligent
    - cautious
    - friendly
  # 说话风格
  style: 认真、谨慎，用"吱"表示惊讶
  # 示例对话
  examples:
    - "吱！你的支出超过预算了！"
    - "让我帮你算算...吱！"

# ===== 初始化配置 =====
init:
  # 用户配置问题（安装时询问）
  questions:
    - key: currency
      prompt: 你使用的货币是什么？
      default: CNY
    - key: budget_monthly
      prompt: 每月预算是多少？
      type: number

  # 环境变量
  env:
    - name: CANG_DATA_DIR
      value: ~/.cang
    - name: CANG Currency
      value: "${currency}"

# ===== 包信息 =====
package:
  # 包含的文件
  includes:
    - IDENTITY.md
    - SOUL.md
    - CAPABILITIES.md
    - MEMORY.template.md
    - assets/*
  # 排除的文件
  excludes:
    - ".git/**"
    - "tests/**"
  # 压缩格式
  format: tar.gz

# ===== 版本历史 =====
changelog: |
  ## 1.0.0 (2026-03-15)
  - 初始发布
```

---

## 字段说明

### 规范字段 (spec)

```yaml
spec: agent/v1  # 必需，规范版本
```

### 基本信息

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `name` | string | ✅ | 显示名称，支持中文 |
| `id` | string | ✅ | 唯一标识符，小写字母+数字+连字符 |
| `version` | string | ✅ | 语义化版本 (semver) |
| `author` | string | ✅ | 作者名称或 ID |
| `license` | string | | 开源协议 (默认: MIT) |
| `description` | string | | 简短描述 (推荐 <100 字) |
| `homepage` | string/URL | | 项目主页 |

**id 命名规则：**
- 只含小写字母、数字、连字符
- 不能以连字符开头/结尾
- 不能有连续连字符
- 推荐：3-20 个字符
- 示例：`cang`, `finance-helper`, `my-agent`

### 展示字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `icon` | path | 图标文件路径 (PNG/SVG, 推荐 256x256) |
| `emoji` | string | Emoji 简写 (fallback 用) |
| `color` | string | 主题色 (十六进制) |
| `tags` | string[] | 分类标签 |

**推荐标签：**

| 类别 | 标签 |
|------|------|
| 功能 | `finance`, `productivity`, `knowledge`, `communication`, `automation` |
| 领域 | `personal`, `business`, `education`, `entertainment`, `health` |
| 技能 | `coding`, `writing`, `analysis`, `management`, `research` |

### 运行时兼容性 (runtime)

```yaml
runtime:
  # 兼容的平台
  compatible:
    - openclaw >= 0.5.0    # 平台 + 最低版本
    - coze                 # 仅平台名
    - dify
    - "*"

  # 必需的能力
  requires:
    - file_io              # 文件读写
    - command_execution    # 命令执行
    - web_request          # 网络请求
    - memory_persistence   # 记忆持久化
```

**预定义能力标识：**

| 能力 | 说明 |
|------|------|
| `file_io` | 读写本地文件 |
| `command_execution` | 执行系统命令 |
| `web_request` | HTTP 请求 |
| `memory_persistence` | 记忆存储 |
| `streaming_response` | 流式输出 |
| `multimodal` | 多模态输入/输出 |

### 能力依赖 (capabilities)

#### CLI 依赖

```yaml
capabilities:
  cli:
    - package: cang-cli           # 包名
      version: ">=0.1.0"          # 版本约束
      install: pip install cang-cli  # 安装命令
      check: cang --version       # 检查命令
      optional: false             # 是否可选
      description: 记账命令行工具
```

**版本约束语法：**

| 约束 | 含义 |
|------|------|
| `>=1.0.0` | 至少 1.0.0 |
| `^1.2.3` | 兼容版本 (>=1.2.3, <2.0.0) |
| `~1.2.3` | 补丁版本 (>=1.2.3, <1.3.0) |
| `*` | 任意版本 |

#### 文件能力

```yaml
capabilities:
  files:
    - read: ["~/Documents/**", "/tmp/data.txt"]
    - write: ["~/Documents/output/**"]
    - execute: ["~/scripts/*.sh"]
```

### 人格配置 (personality)

```yaml
personality:
  traits: [diligent, cautious, friendly]
  style: 认真、谨慎，用"吱"表示惊讶
  examples:
    - "吱！你的支出超过预算了！"
    - "让我帮你算算..."
```

### 初始化配置 (init)

```yaml
init:
  # 安装时询问用户
  questions:
    - key: currency
      prompt: 你使用的货币是什么？
      default: CNY
      type: choice          # text | number | choice | boolean
      options:              # choice 类型时必需
        - CNY
        - USD
        - EUR

  # 环境变量
  env:
    - name: DATA_DIR
      value: ~/.cang
    - name: CURRENCY
      value: "${currency}"   # 引用问题答案
```

### 包信息 (package)

```yaml
package:
  includes: ["**/*.md", "assets/**"]
  excludes: [".git/**", "tests/**", "*.template.md"]
  format: tar.gz            # tar.gz | zip
```

---

## 必需文档规范

### IDENTITY.md

```markdown
# 身份描述

我是仓咚咚，一只负责帮你管钱的小仓鼠。

## 我是谁

- 名称：仓咚咚
- 角色：个人财务管理助手
- 作者：gudong

## 我能做什么

- 记录你的收支
- 分析消费习惯
- 预算提醒
- 生成报表
```

### SOUL.md

```markdown
# 性格设定

## 核心性格

- 认真细致：每笔账都要核对
- 谨慎保守：预警优先于鼓励
- 友好耐心：不因花钱而批评

## 说话风格

- 经常用"吱"表示惊讶或强调
- 重要数字会重复确认
- 用仓鼠的比喻（囤积、坚果等）

## 价值观

- 量入为出
- 未雨绸缪
- 小钱也是钱
```

### CAPABILITIES.md

```markdown
# 能力说明

## 核心能力

### 记账
通过 `cang-cli record` 命令记录收支

### 分析
通过 `cang-cli analyze` 命令生成分析报告

### 提醒
每日检查预算，超支时主动提醒

## 依赖 CLI

- cang-cli >= 0.1.0 (pip install cang-cli)

## 文件访问

- 读取：~/Documents/finance/**
- 写入：~/Documents/finance/reports/**
```

---

## 版本控制

agent.yaml 的 `spec` 字段标识规范版本：

| spec | 状态 | 说明 |
|------|------|------|
| `agent/v1` | 🟢 当前 | 本规范 |
| `agent/v2` | ⚪ 未来 | 向后兼容的扩展 |

**兼容性承诺：** v1.x 系列保持向后兼容

---

## 验证规则

### 必需字段

```python
REQUIRED_FIELDS = ['spec', 'name', 'id', 'version', 'author']

# id 验证
ID_PATTERN = r'^[a-z0-9]([a-z0-9-]*[a-z0-9])?$'

# 版本验证 (semver)
VERSION_PATTERN = r'^\d+\.\d+\.\d+(-[a-zA-Z0-9.]+)?$'
```

### 推荐检查

- [ ] `spec` 为支持的版本
- [ ] `id` 符合命名规则
- [ ] `version` 符合 semver
- [ ] `icon` 文件存在
- [ ] `runtime.requires` 的能力在平台支持列表中
- [ ] `capabilities.cli` 的安装命令安全
- [ ] 必需文档文件存在

---

## 示例包

### 最小包

```
minimal-agent/
├── agent.yaml
├── IDENTITY.md
├── SOUL.md
└── CAPABILITIES.md
```

```yaml
# agent.yaml
spec: agent/v1
name: 最小智能体
id: minimal
version: 1.0.0
author: example
```

### 完整包示例

参考：[examples/cang-agent/](./examples/cang-agent/)

---

## 附录：JSON Schema

<details>
<summary>点击展开 JSON Schema（用于验证）</summary>

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Agent Package v1",
  "type": "object",
  "required": ["spec", "name", "id", "version", "author"],
  "properties": {
    "spec": {
      "type": "string",
      "const": "agent/v1"
    },
    "name": {
      "type": "string",
      "minLength": 1,
      "maxLength": 50
    },
    "id": {
      "type": "string",
      "pattern": "^[a-z0-9]([a-z0-9-]*[a-z0-9])?$",
      "minLength": 3,
      "maxLength": 20
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+(-[a-zA-Z0-9.]+)?$"
    },
    "author": {
      "type": "string"
    },
    "license": {
      "type": "string",
      "default": "MIT"
    },
    "description": {
      "type": "string",
      "maxLength": 200
    },
    "homepage": {
      "type": "string",
      "format": "uri"
    },
    "icon": {
      "type": "string"
    },
    "emoji": {
      "type": "string"
    },
    "color": {
      "type": "string",
      "pattern": "^#[0-9A-Fa-f]{6}$"
    },
    "tags": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "runtime": {
      "type": "object",
      "properties": {
        "compatible": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "requires": {
          "type": "array",
          "items": {
            "type": "string"
          }
        }
      }
    },
    "capabilities": {
      "type": "object",
      "properties": {
        "cli": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["package"],
            "properties": {
              "package": {"type": "string"},
              "version": {"type": "string"},
              "install": {"type": "string"},
              "check": {"type": "string"},
              "optional": {"type": "boolean"},
              "description": {"type": "string"}
            }
          }
        }
      }
    },
    "personality": {
      "type": "object",
      "properties": {
        "traits": {
          "type": "array",
          "items": {"type": "string"}
        },
        "style": {"type": "string"},
        "examples": {
          "type": "array",
          "items": {"type": "string"}
        }
      }
    },
    "init": {
      "type": "object",
      "properties": {
        "questions": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["key", "prompt"],
            "properties": {
              "key": {"type": "string"},
              "prompt": {"type": "string"},
              "default": {"type": "string"},
              "type": {
                "type": "string",
                "enum": ["text", "number", "choice", "boolean"]
              },
              "options": {
                "type": "array",
                "items": {"type": "string"}
              }
            }
          }
        },
        "env": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["name", "value"],
            "properties": {
              "name": {"type": "string"},
              "value": {"type": "string"}
            }
          }
        }
      }
    },
    "package": {
      "type": "object",
      "properties": {
        "includes": {
          "type": "array",
          "items": {"type": "string"}
        },
        "excludes": {
          "type": "array",
          "items": {"type": "string"}
        },
        "format": {
          "type": "string",
          "enum": ["tar.gz", "zip"]
        }
      }
    },
    "changelog": {
      "type": "string"
    }
  }
}
```

</details>

---

*规范版本: agent/v1 | 最后更新: 2026-03-15*
