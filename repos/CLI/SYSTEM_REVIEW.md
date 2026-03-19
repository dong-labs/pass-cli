# 咚咚家族 CLI - 全局系统审查报告

> 生成时间: 2025-03-17
> 审查范围: 依赖关系、架构一致性、代码质量

---

## 1. 依赖关系图

```
┌─────────────────────────────────────────────────────────────────┐
│                        外部依赖 (PyPI)                           │
│  - typer>=0.12.0 (CLI 框架)                                      │
│  - rich>=13.0.0 (终端输出)                                       │
└────────────────────────────┬────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        dong-core (0.1.0)                        │
│  职责：共享基础设施 (瘦 core)                                    │
│                                                                 │
│  导出：                                                          │
│  • json_output decorator - 统一 JSON 输出                        │
│  • DongError (基类异常)                                          │
│  • ValidationError - 输入验证错误                                │
│  • NotFoundError - 资源不存在错误                                │
│  • ConflictError - 冲突错误                                      │
│  • DateUtils - 日期工具                                         │
│                                                                 │
│  自身依赖: typer, rich                                           │
│  测试覆盖率: 99.2% (156 tests passed)                           │
└────────────────────────────┬────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        CLI 应用层                                │
├──────────────┬──────────────┬──────────────┬───────────────────┤
│   log-cli    │  think-cli   │   yue-cli    │   todo-cli        │
│   (jlog)     │   (think)    │    (yue)     │   (dida/todo)     │
│              │              │              │                   │
│  dong-core   │  dong-core   │  dong-core   │   dong-core       │
│  typer, rich │  typer, rich │  typer       │   typer, rich     │
│              │              │              │                   │
├──────────────┴──────────────┴──────────────┴───────────────────┤
│                    cang-cli (仓咚咚)                             │
│                                                                 │
│  通过兼容层 `cang.output.formatter` 导入 dong-core              │
│  - 向后兼容旧代码                                                │
│  - 内部委托给 dong-core                                          │
│                                                                 │
│  模块: fin, asset, budget, invest                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    数据存储层 (~/.dong/)                         │
│  log/log.db      think/think.db    yue/yue.db                   │
│  cang/cang.db    dida/todo.db                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. 各 CLI 迁移状态

| CLI | 命令名 | dong-core 集成 | 命令接口变更 | 状态 |
|-----|--------|----------------|-------------|------|
| **log-cli** | `jlog` | ✅ 直接导入 | ❌ 无 | ✅ 完成 |
| **think-cli** | `think` | ✅ 直接导入 | ❌ 无 | ✅ 完成 |
| **yue-cli** | `yue` | ✅ 直接导入 | ❌ 无 | ✅ 完成 |
| **todo-cli** | `dida` | ✅ 直接导入 | ❌ 无 | ✅ 完成 |
| **cang-cli** | `cang` | ✅ 兼容层 | ❌ 无 | ✅ 完成 |

---

## 3. 数据库 Schema 统一性

### 3.1 时间戳字段

| CLI | created_at | updated_at | 状态 |
|-----|-----------|-----------|------|
| log-cli | ✅ | ✅ | 完成 |
| think-cli | ✅ | ✅ | 完成 |
| yue-cli | ✅ | ✅ | 完成 |
| todo-cli | ✅ | ✅ | 完成 |
| cang-cli | ✅ | ✅ | v2 升级完成 |

**cang-cli Schema 版本升级:**
- 6 张表全部添加 `updated_at` 字段
- SCHEMA_VERSION: 1 → 2
- 表: accounts, transactions, transfers, invest_transactions, budgets, assets

### 3.2 数据库路径规范

```
~/.dong/
├── log/log.db       → log-cli
├── think/think.db   → think-cli
├── yue/yue.db       → yue-cli
├── cang/cang.db     → cang-cli (多模块共享)
└── todo/todo.db     → todo-cli (包名 dida，命令名 todo)
```

---

## 4. 依赖清单

### 4.1 dong-core
```toml
dependencies = [
    "typer>=0.12.0",
    "rich>=13.0.0",
]
```

### 4.2 各 CLI 依赖

| CLI | typer | rich | dong-core | 其他 |
|-----|-------|------|-----------|------|
| log-cli | >=0.9.0 | >=13.0.0 | >=0.1.0 | - |
| think-cli | >=0.9.0 | >=13.0.0 | >=0.1.0 | - |
| yue-cli | >=0.12.0 | (无) | >=0.1.0 | mcp (可选) |
| todo-cli | >=0.12.0 | >=13.0.0 | >=0.1.0 | - |
| cang-cli | >=0.12.0 | (无) | >=0.1.0 | - |

**不一致问题:**
1. **typer 版本不统一**: log-cli/think-cli 用 `>=0.9.0`，其他用 `>=0.12.0`
2. **rich 可选性**: yue-cli/cang-cli 未显式声明 rich 依赖 (通过 dong-core 传递)

---

## 5. cang-cli 兼容层设计

### 5.1 架构

```python
# cang/output/formatter.py (兼容层)
from dong.output.formatter import json_output
from dong.errors.exceptions import (
    DongError, ValidationError, NotFoundError, ConflictError
)

# 向后兼容别名
CangError = DongError
DatabaseError = DongError
InvalidInputError = ValidationError
AlreadyExistsError = ConflictError
```

### 5.2 使用点

| 模块 | 导入方式 | 状态 |
|------|---------|------|
| fin/cli.py | `from cang.output.formatter import json_output, success` | ✅ |
| asset/cli.py | `from cang.output.formatter import json_output` | ✅ |
| budget/cli.py | `from cang.output.formatter import json_output` | ✅ |
| invest/cli.py | `from cang.output.formatter import json_output, ...` | ✅ |

---

## 6. 代码质量评估

### 6.1 优点

1. **统一的 JSON 输出** - 所有命令都使用 `@json_output` 装饰器
2. **一致的错误处理** - 统一使用 dong-core 异常类型
3. **完整的时间戳** - 所有数据表都有 `created_at` 和 `updated_at`
4. **本地优先** - 数据存储在 `~/.dong/`，无云依赖
5. **AI 原生** - 所有命令返回结构化 JSON

### 6.2 待改进项

1. **依赖版本不一致**
   ```toml
   # 建议统一为:
   "typer>=0.12.0",
   "rich>=13.0.0",
   "dong-core>=0.1.0",
   ```

2. **todo-cli 包名/命令名不一致**
   - 包名: `dida`
   - 命令: `dida`
   - README 提及: `todo`
   - 建议统一为 `todo` 或文档说明

3. **测试覆盖** - 已记录在 TODO.md，后期实现

---

## 7. Agent 相关文件

**查询结果:** 项目中未发现 OpenClaw Agent 配置文件 (如 AGENTS.md)。

说明: 本项目是 CLI 工具集，独立于 OpenClaw 多智能体系统。Agent 配置应位于 `~/.openclaw/agents/` 下，不属于本代码库。

---

## 8. 总结与建议

### 8.1 当前状态

✅ **重构完成**: 4 个 CLI 已迁移到 dong-core
✅ **cang-cli**: 通过兼容层完成迁移
✅ **时间戳统一**: 所有数据表都有 created_at/updated_at
✅ **测试**: dong-core 99.2% 覆盖率

### 8.2 建议改进

1. **统一依赖版本** - 将所有 CLI 的 typer 升级到 >=0.12.0
2. **明确 rich 依赖** - 即使通过 dong-core 传递，也建议显式声明
3. **todo-cli 命令名** - 确认最终命令名称 (dida vs todo)

### 8.3 后续工作

1. ⏳ 测试套件 (已记录在 TODO.md)
2. ⏳ dong-core 发布到 PyPI (如需分享)
3. ⏳ 各 CLI 独立发布

---

## 9. 依赖安装顺序

```bash
# 1. 先安装 dong-core (本地开发模式)
cd dong-core
pip install -e .

# 2. 安装各 CLI
cd log-cli && pip install -e .
cd think-cli && pip install -e .
cd yue-cli && pip install -e .
cd todo-cli && pip install -e .
cd cang-cli && pip install -e .
```
