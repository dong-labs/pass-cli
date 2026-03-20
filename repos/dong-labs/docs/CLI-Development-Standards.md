# 咚咚家族 CLI 开发规范

> 让所有咚咚工具保持统一风格

---

## 1. 命名规范

### 1.1 GitHub 仓库

**格式**：`xxx-cli`

```
✅ 正确：cang-cli, log-cli, read-cli, think-cli, dida-cli, expire-cli, pass-cli, timeline-cli
❌ 错误：dong-cang, dong-log, cang, log
```

### 1.2 PyPI 包名

**格式**：`dong-xxx`

```
✅ 正确：dong-cang, dong-log, dong-read, dong-think, dong-dida
❌ 错误：cang-cli, log-cli, cang, log
```

### 1.3 CLI 命令

**格式**：`dong-xxx`

```bash
✅ 正确：dong-cang, dong-log, dong-read, dong-think, dong-dida
❌ 错误：cang, log, jlog, dr
```

### 1.4 Python 模块名

**格式**：`xxx`（无前缀，无后缀）

```python
✅ 正确：cang, log, read, think, dida, expire, pass_, timeline
❌ 错误：dong_cang, cang_cli, dong-log
```

---

## 2. 项目结构

```
xxx-cli/
├── src/
│   └── xxx/                    # 模块名（无前缀）
│       ├── __init__.py         # 版本号
│       ├── __main__.py         # python -m xxx
│       ├── cli.py              # CLI 入口
│       ├── commands/           # 命令模块
│       │   ├── __init__.py
│       │   ├── init.py
│       │   ├── add.py
│       │   ├── ls.py
│       │   ├── get.py
│       │   ├── update.py
│       │   ├── delete.py
│       │   ├── search.py
│       │   └── stats.py
│       └── db/                 # 数据库模块
│           ├── __init__.py
│           ├── connection.py   # 数据库连接
│           └── schema.py       # Schema 定义
├── tests/                      # 测试
│   ├── conftest.py
│   └── test_init.py
├── pyproject.toml              # 项目配置
├── README.md                   # 文档
├── LICENSE                     # MIT
└── .gitignore                  # Git 忽略
```

---

## 3. 依赖管理

### 3.1 pyproject.toml

```toml
[project]
name = "dong-xxx"               # PyPI 包名
version = "0.1.0"
description = "xxx咚 - xxx管理 CLI"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "typer>=0.12.0",
    "rich>=13.0.0",
    "dong-core>=0.3.0",         # 必须依赖 dong-core
]

[project.scripts]
dong-xxx = "xxx.cli:app"        # CLI 命令

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
```

### 3.2 核心依赖

**必须**：
- `typer` - CLI 框架
- `rich` - 终端美化
- `dong-core` - 咚咚核心库

**可选**：
- `python-dateutil` - 日期处理
- `cryptography` - 加密

---

## 4. 数据存储规范

### 4.1 目录结构

**每个 CLI 模块拥有独立目录**，格式：`~/.dong/<name>/`

```
~/.dong/
├── cang/                # dong-cang
│   ├── cang.db         # 数据库
│   ├── export/         # 导出文件
│   └── import/         # 导入文件
├── log/                 # dong-log
│   ├── log.db
│   ├── export/
│   └── import/
├── read/                # dong-read
│   ├── read.db
│   ├── export/
│   └── import/
├── think/               # dong-think
│   ├── think.db
│   ├── export/
│   └── import/
├── dida/                # dong-dida
│   ├── dida.db
│   ├── export/
│   └── import/
├── expire/              # dong-expire
│   ├── expire.db
│   ├── export/
│   └── import/
├── pass/                # dong-pass
│   ├── pass.db
│   ├── export/
│   └── import/
└── timeline/            # dong-timeline
    ├── timeline.db
    ├── export/
    └── import/
```

### 4.2 数据库路径

**格式**：`~/.dong/<name>/<name>.db`

```python
# 自动由 dong-core 的 Database 类管理
# 继承 Database 后，自动获得正确的路径

from dong.db import Database as DongDatabase

class XxxDatabase(DongDatabase):
    @classmethod
    def get_name(cls) -> str:
        return "xxx"  # 数据库路径: ~/.dong/xxx/xxx.db
```

### 4.3 导出目录

**格式**：`~/.dong/<name>/export/`

```
~/.dong/cang/export/
├── 2026-03-20/
│   ├── transactions.json
│   ├── accounts.json
│   └── summary.md
└── 2026-03-19/
    └── backup.json
```

**导出命令示例**：

```bash
# 导出为 JSON
dong-cang export --format json --output ~/Downloads/

# 导出为 Markdown
dong-cang export --format markdown --output ~/Downloads/

# 按日期导出
dong-cang export --start 2026-03-01 --end 2026-03-20
```

### 4.4 导入目录

**格式**：`~/.dong/<name>/import/`

```
~/.dong/cang/import/
├── pending/           # 待导入文件
│   ├── wechat.csv
│   └── alipay.csv
└── processed/         # 已处理文件
    └── 2026-03-19_wechat.csv
```

**导入命令示例**：

```bash
# 从文件导入
dong-cang import ~/Downloads/bills.csv

# 从微信账单导入
dong-cang import --source wechat ~/Downloads/wechat.csv

# 从支付宝账单导入
dong-cang import --source alipay ~/Downloads/alipay.csv
```

### 4.5 其他文件

每个模块目录下可以存放：

| 目录/文件 | 说明 |
|----------|------|
| `<name>.db` | 数据库文件 |
| `export/` | 导出文件目录 |
| `import/` | 导入文件目录 |
| `config.json` | 模块配置（可选） |
| `cache/` | 缓存目录（可选） |
| `logs/` | 日志目录（可选） |

### 4.6 继承 Database

```python
from dong.db import Database as DongDatabase

class XxxDatabase(DongDatabase):
    """xxx 数据库类
    
    数据库路径: ~/.dong/xxx/xxx.db
    模块目录: ~/.dong/xxx/
    """
    
    @classmethod
    def get_name(cls) -> str:
        return "xxx"
    
    @classmethod
    def get_export_dir(cls) -> Path:
        """获取导出目录"""
        return cls.get_module_dir() / "export"
    
    @classmethod
    def get_import_dir(cls) -> Path:
        """获取导入目录"""
        return cls.get_module_dir() / "import"
```

### 4.7 继承 SchemaManager

```python
from dong.db import SchemaManager

class XxxSchemaManager(SchemaManager):
    def __init__(self):
        super().__init__(
            db_class=XxxDatabase,
            current_version="1.0.0"
        )
    
    def init_schema(self) -> None:
        with XxxDatabase.get_cursor() as cur:
            cur.execute("CREATE TABLE IF NOT EXISTS ...")
```

---

## 5. 命令规范

### 5.1 基础命令（必须）

| 命令 | 说明 |
|------|------|
| `init` | 初始化数据库 |
| `add` | 添加记录 |
| `list` | 列出记录 |
| `get` | 获取详情 |
| `update` | 更新记录 |
| `delete` | 删除记录 |

### 5.2 扩展命令（推荐）

| 命令 | 说明 |
|------|------|
| `search` | 搜索记录 |
| `stats` | 统计信息 |

### 5.3 命令示例

```python
@app.command()
def add(
    content: str = typer.Argument(..., help="内容"),
    tags: str = typer.Option(None, "--tags", "-t", help="标签"),
):
    """添加记录"""
    pass
```

---

## 6. 输出规范

### 6.1 JSON 输出（必须）

**使用 `@json_output` 装饰器**：

```python
from dong import json_output

@json_output
def add(...):
    return {"id": 1, "content": "xxx"}
```

### 6.2 输出格式

```json
{
  "success": true,
  "data": {
    "id": 1,
    "content": "xxx"
  }
}
```

---

## 7. 错误处理

### 7.1 使用 DongError

```python
from dong import DongError

if not is_initialized():
    raise DongError("NOT_INITIALIZED", "请先运行 dong-xxx init")
```

### 7.2 错误码规范

| 错误码 | 说明 |
|--------|------|
| NOT_INITIALIZED | 数据库未初始化 |
| NOT_FOUND | 记录不存在 |
| INVALID_DATE | 日期格式错误 |
| INVALID_RANGE | 时间范围错误 |
| DUPLICATE | 重复记录 |
| NO_UPDATES | 没有更新 |
| INVALID_IMPORTANCE | 无效的重要程度 |
| NO_MASTER_PASSWORD | 缺少主密码 |

### 7.3 错误处理示例

```python
@json_output
def get(event_id: int):
    if not is_initialized():
        raise DongError("NOT_INITIALIZED", "请先运行 dong-xxx init")
    
    with get_cursor() as cur:
        cur.execute("SELECT * FROM xxx WHERE id = ?", (event_id,))
        row = cur.fetchone()
        
        if not row:
            raise DongError("NOT_FOUND", f"未找到 ID={event_id} 的记录")
    
    return {"id": event_id, "data": row}
```

---

## 8. 文档规范

### 8.1 README.md

**必须包含**：
- 安装方式
- 快速开始
- 命令列表
- 数据结构
- 示例

### 8.2 代码注释

```python
def add(content: str, ...):
    """添加记录
    
    Args:
        content: 记录内容
        tags: 标签（逗号分隔）
    
    Returns:
        dict: 添加的记录
    """
    pass
```

---

## 9. 版本管理

### 9.1 版本号规范

**格式**：`MAJOR.MINOR.PATCH`

- **MAJOR**：重大变更
- **MINOR**：新功能
- **PATCH**：Bug 修复

### 9.2 版本递增

| 变更类型 | 版本递增 |
|---------|---------|
| 新功能 | MINOR +1 |
| Bug 修复 | PATCH +1 |
| 重大变更 | MAJOR +1 |

---

## 10. 发布流程

### 10.1 本地测试

```bash
# 本地安装
pipx install .

# 测试命令
dong-xxx init
dong-xxx add "test"
```

### 10.2 发布 PyPI

```bash
# 构建
python3 -m build

# 上传
twine upload dist/*
```

### 10.3 推送 GitHub

```bash
git add -A
git commit -m "Release v0.1.0"
git tag v0.1.0
git push
git push --tags
```

---

## 11. 测试规范

### 11.1 测试文件

```
tests/
├── conftest.py      # 测试配置
├── test_init.py     # 初始化测试
├── test_add.py      # 添加测试
├── test_list.py     # 列表测试
└── test_search.py   # 搜索测试
```

### 11.2 测试示例

```python
from click.testing import CliRunner
from xxx.cli import app

def test_init():
    runner = CliRunner()
    result = runner.invoke(app, ["init"])
    assert result.exit_code == 0
```

---

## 12. AI 友好设计

### 12.1 JSON 输出

**所有命令都返回 JSON**：

```json
{
  "success": true,
  "data": {...}
}
```

### 12.2 搜索功能

**必须支持搜索**：

```bash
dong-xxx search "关键词"
```

### 12.3 标签支持

**推荐支持标签**：

```bash
dong-xxx add "内容" --tags "tag1,tag2"
```

---

## 13. 代码风格

### 13.1 Python 风格

- 遵循 PEP 8
- 使用 type hints
- 函数不超过 50 行

### 13.2 命名风格

| 类型 | 风格 | 示例 |
|------|------|------|
| 函数 | snake_case | `add_record` |
| 类 | PascalCase | `LogDatabase` |
| 常量 | UPPER_CASE | `SCHEMA_VERSION` |

---

## 14. Git 规范

### 14.1 提交信息

**格式**：`<type>: <message>`

```
feat: 添加搜索功能
fix: 修复日期解析错误
docs: 更新 README
refactor: 重构数据库模块
```

### 14.2 分支管理

- `main` - 主分支
- `develop` - 开发分支
- `feature/xxx` - 功能分支

---

## 15. 检查清单

### 15.1 发布前检查

- [ ] 代码测试通过
- [ ] README 已更新
- [ ] 版本号已递增
- [ ] Git 提交已推送
- [ ] PyPI 已发布
- [ ] GitHub Release 已创建

### 15.2 功能检查

- [ ] init 命令正常
- [ ] add 命令正常
- [ ] list 命令正常
- [ ] search 命令正常
- [ ] JSON 输出正常

---

**遵循这些规范，保持咚咚家族统一风格！** 🐮💻✨

from dong import Config

# 创建配置
config = Config("xxx")

# 读取配置
value = config.get("key")

# 写入配置
config.set("key", "value")

# 删除配置
config.delete("key")
```

### 16.4 日期工具 (dong.utils)

```python
from dong.utils import DateUtils

# 获取今天
today = DateUtils.today()

# 获取昨天
yesterday = DateUtils.yesterday()

# 获取本周
week_start, week_end = DateUtils.this_week()

# 获取本月
month_start, month_end = DateUtils.this_month()

# 格式化日期
formatted = DateUtils.format(date, "%Y-%m-%d")

# 解析日期
date = DateUtils.parse("2026-03-19")
```

### 16.5 其他工具

```python
# 标签处理
from dong.utils import parse_tags

tags = parse_tags("tag1,tag2,tag3")  # ["tag1", "tag2", "tag3"]

# JSON 处理
from dong.utils import to_json, from_json

json_str = to_json({"key": "value"})
data = from_json('{"key": "value"}')
```

---

## 17. 更新 dong-core 的标准

### 17.1 应该添加到 dong-core

✅ **应该添加**：
- 多个 CLI 都需要的功能
- 基础设施代码
- 工具函数
- 数据库基类
- 输出装饰器

### 17.2 不应该添加到 dong-core

❌ **不应该添加**：
- 单个 CLI 特有的功能
- 业务逻辑代码
- 特定领域的代码

### 17.3 更新流程

```bash
# 1. 修改 dong-core
cd ~/.openclaw/workspace-madong/repos/dong-labs/dong-core

# 2. 更新版本号
# 编辑 src/dong/__init__.py 中的 __version__

# 3. 发布到 PyPI
python3 -m build
twine upload dist/*

# 4. 推送到 GitHub
git add -A
git commit -m "Release v0.x.0"
git tag v0.x.0
git push && git push --tags

# 5. 更新依赖它的 CLI
# 修改 pyproject.toml 中的 dong-core 版本号
```

---

## 18. 检查清单（完整版）

### 18.1 新建 CLI 项目检查清单

- [ ] 复制现有 CLI 项目
- [ ] 修改项目名（xxx-cli）
- [ ] 修改 pyproject.toml（name = "dong-xxx"）
- [ ] 修改模块名（xxx）
- [ ] 修改 CLI 命令（dong-xxx）
- [ ] 修改数据库名（xxx.db）
- [ ] 继承 Database 和 SchemaManager
- [ ] 实现 init/add/list/get/update/delete 命令
- [ ] 实现 search/stats 命令
- [ ] 使用 @json_output 装饰器
- [ ] 使用 DongError 错误处理
- [ ] 编写测试用例
- [ ] 编写 README.md
- [ ] 本地测试（pipx install .）
- [ ] 发布 PyPI
- [ ] 创建 GitHub 仓库
- [ ] 推送代码
- [ ] 更新 AGENTS.md

### 18.2 发布前检查清单

- [ ] 代码测试通过
- [ ] README 已更新
- [ ] 版本号已递增
- [ ] Git 提交已推送
- [ ] PyPI 已发布
- [ ] GitHub Release 已创建
- [ ] dong-core 依赖版本正确

---

**遵循这些规范，保持咚咚家族统一风格！** 🐮💻✨
