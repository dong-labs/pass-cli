# Dong Family CLI

> 咚咚家族 - 本地优先的个人数据管理 CLI 工具集

---

## 🎯 我们是谁

咚咚家族是一系列**独立**的 CLI 工具，每个工具专注管理一种个人数据：

| CLI | 命令 | 中文名 | 用途 | 状态 |
|-----|------|--------|------|------|
| [log-cli](./log-cli) | `jlog` | 记咚咚 | 记录日常日志 | ✅ |
| [think-cli](./think-cli) | `think` | 思咚咚 | 记录灵感想法 | ✅ |
| [yue-cli](./yue-cli) | `yue` | 阅咚咚 | 收集阅读摘录 | ✅ |
| [cang-cli](./cang-cli) | `cang` | 仓咚咚 | 管理财务记录 | ✅ |
| [todo-cli](./todo-cli) | `todo` | 事咚咚 | 待办与任务 | 🚧 |

> **设计原则**：每个 CLI 是独立产品，可独立安装、独立使用、独立卸载。

---

## 💡 为什么做

1. **本地优先** - 数据在我电脑上，不上云、不同步、不追踪
2. **一个工具一件事** - 不做全家桶，每个 CLI 只管一件事
3. **AI 原生** - 所有命令返回 JSON，方便 Agent 调用
4. **极简核心** - 只做增删改查，不做报表、分析、推荐

### 目标用户

- **主要用户**：AI Agent（如 OpenClaw 的咚咚家族智能体）
- **次要用户**：终端重度用户（开发者、运维）

---

## 🏗️ 架构

```
┌─────────────────────────────────────────────────────────┐
│                    独立 CLI 层                           │
│   jlog      think     yue      cang     todo           │
│   (独立)    (独立)    (独立)    (独立)    (独立)         │
└──────────────────────┬──────────────────────────────────┘
                       │ 可选依赖
                       ▼
┌─────────────────────────────────────────────────────────┐
│                    dong-core (瘦)                        │
│   • formatter - 统一 JSON 输出格式                       │
│   • errors - 统一错误类型                                │
│   • dates - 日期处理工具 (today/week/month)              │
│   • testing - 测试 fixtures                             │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│                    ~/.dong/                              │
│   log/  think/  yue/  cang/  todo/  ...                 │
└─────────────────────────────────────────────────────────┘
```

### dong-core 的边界

**dong-core 提供：**
- ✅ 统一 JSON 输出格式 (`formatter.py`)
- ✅ 统一错误类型 (`errors.py`)
- ✅ 日期处理工具 (`dates.py`)
- ✅ 测试 fixtures (`testing.py`)

**dong-core 不提供：**
- ❌ 数据模型（每个 CLI 数据结构差异太大）
- ❌ 业务逻辑命令（每个 CLI 需求不同）
- ❌ 数据库 schema（由各 CLI 自己定义）

> **理念**：dong-core 是"工具箱"，不是"框架"。

---

## 📐 设计原则

### 1. 一个工具一件事

每个 CLI 只解决一个核心问题，不做范围蔓延。

| 工具 | 做 | 不做 |
|------|-----|------|
| 记咚咚 | 记流水账 | 日历视图、心情分析 |
| 思咚咚 | 记想法 | 笔记系统、知识图谱 |
| 阅咚咚 | 存摘录 | 自动抓取、全文搜索 |
| 仓咚咚 | 记收支 | 报表、投资建议 |
| 事咚咚 | 管待办 | 习惯追踪、番茄钟 |

> **原则**: 有疑问时，不加。想加新功能？先划掉一个旧的。

### 2. 数据所有权归用户

- 所有数据存放在 `~/.dong/` 下，SQLite 格式
- 每个工具有独立的数据库文件
- 用户可以直接用 SQL 查询自己的数据
- 不加锁、不加密、不混淆

### 3. AI 原生

- 所有命令支持 `--json` 输出
- 返回结构化数据，不是装饰性文本
- Agent 可靠调用，不是给人看的

### 4. 统一数据目录

```
~/.dong/
├── log/log.db
├── think/think.db
├── yue/yue.db
├── cang/cang.db
└── todo/todo.db
```

### 5. 统一技术栈

- **CLI 框架**：Typer（所有 CLI 统一）
- **终端输出**：Rich
- **数据库**：SQLite
- **Python**：3.11+

### 6. 统一命令风格

每个 CLI 必须有以下基础命令：

| 命令 | 说明 |
|------|------|
| `init` | 初始化数据库 |
| `add` | 添加记录 |
| `ls` | 列出记录 |
| `get` | 获取单条 |
| `delete` | 删除记录 |
| `search` | 搜索内容（可选） |

统一参数风格：

| 参数 | 说明 |
|------|------|
| `--limit, -l` | 限制数量 |
| `--json` | JSON 输出 |
| `--today` | 只显示今天 |
| `--week` | 只显示本周 |

### 7. 统一 JSON 输出格式

```json
// 成功
{
  "success": true,
  "data": { ... }
}

// 失败
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "错误信息"
  }
}
```

---

## 🚫 我们不做什么

| 不做 | 原因 |
|------|------|
| 多端同步 | 本地优先，同步由用户决定 |
| 云端备份 | 用户自己 rsync/git |
| GUI/Web | 只做 CLI，其他由用户扩展 |
| 账号系统 | 本地使用，不需要账号 |
| 数据分析 | 只存储，分析由外部工具做 |
| AI 生成摘要 | 只记录，AI 由 Agent 层做 |
| 合并为一个命令 | 保持独立，按需安装 |

---

## 📦 新开发 CLI 指南

### 1. 命名

```
<name>-cli/          # 仓库名
<命令>               # CLI 命令
<中文名>咚咚         # 中文名
```

示例：
- `log-cli` → `jlog` → 记咚咚
- `todo-cli` → `todo` → 事咚咚

### 2. 技术栈

```python
# pyproject.toml
dependencies = [
    "dong-core>=0.1.0",   # 可选，使用通用组件
    "typer>=0.12.0",      # CLI 框架（统一）
    "rich>=13.0.0",       # 终端输出（统一）
]
```

### 3. 项目结构

```
<name>-cli/
├── src/<name>/
│   ├── __init__.py
│   ├── cli.py           # Typer 入口
│   ├── const.py         # 常量（DB_PATH 等）
│   ├── models.py        # 数据模型（自己定义）
│   ├── db/
│   │   └── schema.py    # 数据库表结构
│   └── commands/
│       ├── init.py
│       ├── add.py
│       ├── ls.py
│       ├── get.py
│       └── delete.py
├── tests/
├── pyproject.toml
└── README.md
```

### 4. 数据库路径

```python
# const.py
from pathlib import Path
DB_DIR = Path.home() / ".dong" / "<name>"
DB_PATH = DB_DIR / "<name>.db"
```

### 5. 使用 dong-core（可选）

```python
# 使用统一 JSON 输出
from dong.output import json_output

@json_output
def my_command():
    return {"id": 1, "content": "..."}

# 使用日期工具
from dong.dates import get_today, get_week_range

today = get_today()
start, end = get_week_range()
```

### 6. 测试要求（强制）

#### 6.1 测试配置

```toml
# pyproject.toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "pytest-mock>=3.10",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
addopts = ["-v", "--cov=.", "--cov-report=term-missing"]
```

#### 6.2 测试目录结构

```
<name>-cli/
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # 共享 fixtures
│   ├── unit/                    # 单元测试
│   │   ├── test_commands.py
│   │   └── test_repository.py
│   └── integration/             # 集成测试
│       └── test_cli.py
```

#### 6.3 覆盖率要求

| 模块 | 最低覆盖率 |
|------|-----------|
| 数据库操作 (repository) | 90% |
| 命令逻辑 (commands) | 80% |
| 模型 (models) | 70% |
| 工具函数 (utils) | 80% |

#### 6.4 测试示例

```python
# tests/integration/test_cli.py
import json
from typer.testing import CliRunner
from <name>.cli import app

runner = CliRunner()

def test_add_command():
    """测试添加命令"""
    result = runner.invoke(app, ["add", "测试内容", "--json"])
    assert result.exit_code == 0

    data = json.loads(result.stdout)
    assert data["success"] == True
    assert "id" in data["data"]
```

#### 6.5 AI 辅助开发测试流程

```
1. AI 生成代码
2. 立即运行 pytest 验证
3. 测试失败 → AI 修复 → 重测
4. 通过后检查覆盖率 pytest --cov
5. 达标后提交
```

> **原则**：测试不通过，代码不提交。

---

## 🔧 工程实践

### 版本策略

- `dong-core` 独立版本，使用语义化版本
- 各 CLI 独立版本，不与 core 绑定
- core 破坏性更新必须升主版本 (0.x → 1.0)

### 发布策略

```
1. 先发布 dong-core
2. 逐个发布依赖它的 CLI
3. 使用 CI/CD 自动化
```

### 测试策略

- 单元测试：测试 repository 层
- 集成测试：测试 CLI 命令，验证 JSON 输出
- 使用 dong-core 提供的测试 fixtures

---

## 📝 LICENSE

MIT
