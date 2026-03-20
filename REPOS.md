# REPOS.md - 咚咚家族仓库规范

> **AI 优先阅读此文档** - 所有项目代码在 `repos/dong-labs/` 目录下

## 仓库位置

```
~/.openclaw/workspace-madong/repos/dong-labs/
```

## 快速索引

| # | 目录 | PyPI 包名 | CLI 命令 | 功能 | 远程仓库 |
|---|------|-----------|----------|------|----------|
| 1 | `log-cli` | `dong-log` | `dong-log` | 日志管理 | github.com/dong-labs/log-cli |
| 2 | `read-cli` | `dong-read` | `dong-read` | 知识管理 | github.com/dong-labs/read-cli |
| 3 | `think-cli` | `dong-think` | `dong-think` | 灵感管理 | github.com/dong-labs/think-cli |
| 4 | `dida-cli` | `dong-dida` | `dong-dida` | 待办管理 | github.com/dong-labs/dida-cli |
| 5 | `cang-cli` | `dong-cang` | `dong-cang` | 财务管理 | github.com/dong-labs/cang-cli |
| 6 | `expire-cli` | `dong-expire` | `dong-expire` | 到期日管理 | github.com/dong-labs/expire-cli |
| 7 | `pass-cli` | `dong-pass` | `dong-pass` | 账号密码管理 | github.com/dong-labs/pass-cli |
| 8 | `timeline-cli` | `dong-timeline` | `dong-timeline` | 关键节点管理 | github.com/dong-labs/timeline-cli |
| - | `dong-core` | `dong-core` | - | 核心共享库 | github.com/dong-labs/dong-core |

## 命名规范（严格遵守）

| 类型 | 命名规则 | 示例 |
|------|----------|------|
| 本地目录 | `xxx-cli` | `log-cli/` |
| GitHub 仓库 | `xxx-cli` | `dong-labs/log-cli` |
| PyPI 包名 | `dong-xxx` | `dong-log` |
| CLI 命令 | `dong-xxx` | `dong-log` |
| Python 模块 | `xxx` | `import log` |
| 数据库文件 | `xxx.db` | `~/.dong/log.db` |

## 标准项目结构

```
xxx-cli/
├── src/xxx/                 # Python 模块 (注意: 模块名不含 -cli)
│   ├── __init__.py          # 包版本号 __version__
│   ├── cli.py               # CLI 主入口，定义 Typer app
│   ├── commands/            # 命令模块目录
│   │   ├── __init__.py
│   │   ├── init.py          # init 命令
│   │   ├── add.py           # add 命令
│   │   ├── ls.py            # list 命令
│   │   ├── get.py           # get 命令
│   │   ├── update.py        # update 命令
│   │   ├── delete.py        # delete 命令
│   │   ├── search.py        # 搜索命令 (AI 友好)
│   │   ├── stats.py         # 统计命令 (AI 友好)
│   │   └── tags.py          # 标签管理 (AI 友好)
│   └── db/                  # 数据库层
│       ├── connection.py    # 数据库连接
│       ├── schema.py        # 表结构定义
│       └── repository.py    # 数据访问层
├── tests/                   # 测试
├── pyproject.toml           # 项目配置
├── README.md                # 项目说明
└── LICENSE                  # 许可证
```

## pyproject.toml 标准模板

```toml
[project]
name = "dong-xxx"              # PyPI 包名: dong-xxx
version = "0.3.0"
description = "中文描述"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "typer>=0.12.0",
    "rich>=13.0.0",
    "dong-core>=0.3.0",        # 必须依赖 dong-core
]

[project.scripts]
dong-xxx = "xxx.cli:app"        # CLI 入口: 模块名.cli:app

[tool.hatch.build.targets.wheel]
packages = ["src/xxx"]           # 注意: 模块名不含 -cli
```

## 核心依赖 dong-core

所有 CLI 必须使用 `dong-core` 提供的基础设施：

```python
# JSON 输出装饰器
from dong.output.formatter import json_output

# 异常类
from dong.errors.exceptions import (
    DongError,
    ValidationError,
    NotFoundError,
    ConflictError,
)

# 数据库基类 (如需要)
from dong.db import Database, SchemaManager
```

## AI 友好功能（必须实现）

每个 CLI 必须包含以下功能：

| 功能 | 命令 | 说明 |
|------|------|------|
| 搜索 | `xxx search <关键词>` | 全文搜索内容 |
| 统计 | `xxx stats` | 数据统计概览 |
| 标签 | `xxx tags` | 列出所有标签 |
| 标签筛选 | `xxx ls --tag <标签>` | 按标签筛选 |
| JSON 输出 | 所有命令 | `{"success": true, "data": {...}}` |

## 开发工作流

```bash
# 1. 进入项目目录
cd ~/.openclaw/workspace-madong/repos/dong-labs/xxx-cli

# 2. 本地开发安装
pipx install . --force

# 3. 测试命令
dong-xxx --help
dong-xxx add "测试内容"

# 4. 构建发布
python3 -m build
twine upload dist/*

# 5. 推送代码
git push origin main
```

## 相关文档

- **开发规范**: `docs/CLI-Development-Standards.md`
- **AI 设计**: `docs/AI-Friendly-CLI-Design.md`
- **智能体配置**: `AGENTS.md`

## 注意事项

1. **所有项目代码必须在 `repos/dong-labs/` 下**
2. **根目录只放配置文件，不放项目代码**
3. **PyPI 包名和 CLI 命令都是 `dong-xxx` 格式**
4. **必须继承 dong-core 的基础设施**
5. **所有命令必须返回 JSON 格式**
