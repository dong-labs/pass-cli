# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**dong-labs** is a collection of personal CLI tools (the "咚咚家族" / DongDong Family) - AI-native command-line tools for managing personal data. All tools are open source on [GitHub](https://github.com/dong-labs).

### Core Philosophy

1. **AI First, Human Second** - All commands are designed for AI agent consumption first
2. **JSON Native** - Every command returns structured JSON output
3. **Local & Private** - Data stored in `~/.dong/`, never synced to cloud
4. **Minimal Core** - Each tool does one thing well, avoids feature creep

### The CLI Family

| CLI | PyPI Package | Command | Purpose |
|-----|-------------|---------|---------|
| **read-cli** | `dong-read` | `dong-read` | Personal knowledge data layer (bookmarks, excerpts) |
| **think-cli** | `dong-think` | `dong-think` | Idea and inspiration tracking |
| **dida-cli** | `dong-dida` | `dong-dida` | Todo/task management |
| **log-cli** | `dong-log` | `dong-log` | Daily journal logging |
| **cang-cli** | `dong-cang` | `dong-cang` | Personal finance (transactions, assets, budget, investment) |
| **expire-cli** | `dong-expire` | `dong-expire` | Subscription/expiration date tracking |
| **pass-cli** | `dong-pass` | `dong-pass` | Password/account management |
| **timeline-cli** | `dong-timeline` | `dong-timeline` | Timeline visualization |

---

## Architecture

### Monorepo Structure

```
dong-labs/
├── dong-core/          # Shared core library (infrastructure only)
├── read-cli/           # Personal knowledge CLI
├── think-cli/          # Idea tracking CLI
├── dida-cli/           # Todo management CLI
├── log-cli/            # Daily logging CLI
├── cang-cli/           # Finance CLI (4 modules: fin, asset, invest, budget)
├── expire-cli/         # Expiration tracking CLI
├── pass-cli/           # Password management CLI
├── timeline-cli/       # Timeline CLI
└── docs/               # Development standards
    ├── CLI-Development-Standards.md
    └── AI-Friendly-CLI-Design.md
```

### dong-core: The Shared Foundation

**Location**: `dong-core/src/dong/`

The core library is intentionally "thin" - it provides only infrastructure, not business logic:

| Module | Purpose |
|--------|---------|
| `db.Database` | Base class for SQLite database management |
| `db.SchemaManager` | Schema version management |
| `config.Config` | Unified config management (`~/.dong/config.json`) |
| `output.formatter.json_output` | Decorator for consistent JSON output |
| `errors.exceptions` | `DongError`, `ValidationError`, `NotFoundError`, `ConflictError` |
| `dates.utils.DateUtils` | Date range utilities (today, this_week, this_month, etc.) |

### Data Storage Convention

All databases are stored in `~/.dong/`:

```
~/.dong/
├── config.json       # Unified config file
├── read.db
├── think.db
├── dida.db
├── log.db
├── cang.db
├── expire.db
├── pass.db
└── timeline.db
```

---

## Development Standards

### Naming Conventions

| Type | Format | Examples |
|------|--------|----------|
| GitHub repo | `xxx-cli` | `read-cli`, `think-cli`, `cang-cli` |
| PyPI package | `dong-xxx` | `dong-read`, `dong-think`, `dong-cang` |
| CLI command | `dong-xxx` | `dong-read`, `dong-think` |
| Python module | `xxx` | `read`, `think`, `cang`, `pass_` |

### Standard CLI Structure

```
xxx-cli/
├── src/
│   └── xxx/                    # Module name (no prefix/suffix)
│       ├── __init__.py         # Version constant
│       ├── __main__.py         # python -m xxx entry point
│       ├── cli.py              # Typer app entry point
│       ├── const.py            # Constants
│       ├── config.py           # Config subclass
│       ├── db/
│       │   ├── connection.py   # Database subclass
│       │   └── schema.py       # Schema definition
│       ├── core/               # Domain models (optional)
│       └── commands/
│           ├── init.py
│           ├── add.py
│           ├── ls.py
│           ├── get.py
│           ├── update.py
│           ├── delete.py
│           ├── search.py       # AI-friendly
│           └── stats.py        # AI-friendly
├── tests/
├── pyproject.toml
└── README.md
```

### Standard Commands

All CLIs should implement these base commands:

| Command | Purpose |
|---------|---------|
| `init` | Initialize database |
| `add` | Add record |
| `list` | List records |
| `get` | Get single record |
| `update` | Update record |
| `delete` | Delete record |
| `search` | Search content (AI-friendly) |
| `stats` | Statistics overview (AI-friendly) |

---

## Common Development Tasks

### Creating a New CLI

1. Copy an existing CLI (e.g., `think-cli`)
2. Update names in `pyproject.toml`: `name = "dong-xxx"`
3. Rename module directory in `src/`
4. Update `cli.py` and all imports
5. Implement `db/connection.py`:

```python
from dong.db import Database as DongDatabase

class XxxDatabase(DongDatabase):
    @classmethod
    def get_name(cls) -> str:
        return "xxx"  # Matches database filename
```

### Using json_output Decorator

```python
from dong import json_output, ValidationError

@json_output
def my_command(arg: str):
    if not arg:
        raise ValidationError("arg", "Cannot be empty")
    return {"id": 1, "result": arg}
# Output: {"success": true, "data": {"id": 1, "result": "..."}}
```

### Database Access Pattern

```python
from xxx.db import get_cursor

def get_item(item_id: int):
    with get_cursor() as cur:
        cur.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        row = cur.fetchone()
        if not row:
            raise NotFoundError("Item", item_id)
        return dict(row)
```

### Date Utilities

```python
from dong.dates import DateUtils

today = DateUtils.today()
week_start, week_end = DateUtils.this_week()
month_start, month_end = DateUtils.this_month()
```

---

## AI-Friendly Design

All CLIs must support:

1. **JSON Output** - Every command returns `{"success": true/false, "data"/"error": ...}`
2. **Search** - `<cli> search "keyword"` for content discovery
3. **Stats** - `<cli> stats` for data overview
4. **Tags** - Optional tagging system for categorization

This enables AI agents to:
- Discover relevant data without reading everything
- Understand data distribution
- Filter by context/topic

---

## Build & Test Commands

### dong-core

```bash
cd dong-core
pip install -e ".[dev]"
pytest
pytest --cov=dong --cov-report=html
```

### Any CLI

```bash
cd xxx-cli
pip install -e ".[dev]"
pytest
dong-xxx init
```

### Publish to PyPI

```bash
python3 -m build
twine upload dist/*
git tag v0.x.0
git push --tags
```

---

## Key Design Principles

1. **Thin Core** - `dong-core` has no business logic, only infrastructure
2. **Independence** - Each CLI can be used standalone
3. **Shared Config** - All CLIs use `~/.dong/config.json`
4. **Version Alignment** - Update `dong-core` dependency when using new features
5. **Error Codes** - Use standard `DongError` subclasses for consistent error handling

---

## References

- Development Standards: `docs/CLI-Development-Standards.md`
- AI-Friendly Design: `docs/AI-Friendly-CLI-Design.md`
- GitHub: https://github.com/dong-labs
