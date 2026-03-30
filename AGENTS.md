# AGENTS.md - 小码牛操作说明

我是咕咚的编码助手 🐮💻，咕咚的编码助手。

## 📁 优先阅读

**找代码/仓库？** → 先读 [`REPOS.md`](./REPOS.md) - 完整的仓库索引和规范

---

## 我能做什么

- 写代码
- 修 bug
- 代码审查
- 重构代码
- 解释代码逻辑
- **开发咚咚家族 CLI 工具**

## 使用方式

把代码仓库放到 `repos/` 目录下，我直接在那里干活。

```bash
cd ~/.openclaw/workspace-coder/repos
git clone <你的仓库>
```

## 工作原则

1. 先理解问题，再改代码
2. 最小改动修复 bug
3. 能跑先跑起来
4. 代码 > 解释

---

## 🛠️ 咚咚家族 CLI 开发指南

### 项目地址

- **仓库索引**：`REPOS.md` ⭐ **AI 首选**
- **规范文档**：`docs/CLI-Development-Standards.md`
- **项目代码**：`repos/dong-labs/`
- **GitHub**：https://github.com/dong-labs
- **数据库**：`~/.dong/xxx/xxx.db`

### 命名规范

| 类型 | 格式 | 示例 |
|------|------|------|
| **本地目录** | `xxx-cli` | log-cli, read-cli |
| **GitHub 仓库** | `xxx-cli` | dong-labs/log-cli |
| **PyPI 包名** | `dong-xxx` | dong-log, dong-read |
| **CLI 命令** | `dong-xxx` | dong-log, dong-read |
| **Python 模块** | `xxx` | import log, import read |
| **数据库** | `~/.dong/xxx/xxx.db` | ~/.dong/log/log.db, ~/.dong/read/read.db |

### 核心依赖

**必须依赖 dong-core**：
```toml
dependencies = [
    "dong-core>=0.3.0",
]
```

### 项目结构

```
xxx-cli/
├── src/xxx/
│   ├── cli.py
│   ├── commands/
│   │   ├── init.py
│   │   ├── add.py
│   │   ├── ls.py
│   │   ├── get.py
│   │   ├── update.py
│   │   ├── delete.py
│   │   ├── search.py
│   │   ├── stats.py
│   │   └── tags.py
│   └── db/
│       ├── connection.py
│       └── schema.py
├── tests/
├── pyproject.toml
└── README.md
```

### 开发流程

1. **复制模板**：复制现有 CLI 项目
2. **修改命名**：修改包名、模块名、CLI 命令
3. **继承 dong-core**：继承 Database 和 SchemaManager
4. **实现命令**：实现 init/add/list/get/update/delete/search/stats
5. **本地测试**：`pipx install .`
6. **发布 PyPI**：`python3 -m build && twine upload dist/*`
7. **推送 GitHub**：`git push && git push --tags`

### 必须功能

- ✅ JSON 输出（使用 `@json_output`）
- ✅ 错误处理（使用 `DongError`）
- ✅ 搜索功能（`search` 命令）
- ✅ 统计功能（`stats` 命令）
- ✅ 标签支持（`--tags` 参数）

### dong-core 使用

```python
# 继承 Database
from dong.db import Database as DongDatabase

class XxxDatabase(DongDatabase):
    @classmethod
    def get_name(cls) -> str:
        return "xxx"

# 继承 SchemaManager
from dong.db import SchemaManager

class XxxSchemaManager(SchemaManager):
    def init_schema(self) -> None:
        with XxxDatabase.get_cursor() as cur:
            cur.execute("CREATE TABLE IF NOT EXISTS ...")

# 使用 @json_output
from dong import json_output

@json_output
def add(content: str):
    return {"id": 1, "content": content}
```

### 已完成的 CLI

| # | 工具 | GitHub | PyPI | CLI |
|---|------|--------|------|-----|
| 1 | 小仓鼠 | cang-cli | dong-cang | dong-cang |
| 2 | 记录 | log-cli | dong-log | dong-log |
| 3 | 阅读 | read-cli | dong-read | dong-read |
| 4 | 灵感 | think-cli | dong-think | dong-think |
| 5 | 待办 | dida-cli | dong-dida | dong-dida |
| 6 | 到期 | expire-cli | dong-expire | dong-expire |
| 7 | 密码 | pass-cli | dong-pass | dong-pass |
| 8 | 时间线 | timeline-cli | dong-timeline | dong-timeline |

---

*让我看看代码...*
