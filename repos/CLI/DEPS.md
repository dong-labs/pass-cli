# 咚咚家族 CLI - 依赖清单

## 依赖树

```
外部 (PyPI)
├── typer>=0.12.0 (CLI 框架)
└── rich>=13.0.0 (终端输出)
    │
    ▼
dong-core (共享核心库)
│   • json_output decorator
│   • 统一异常类
│   • DateUtils
    │
    ▼
CLI 应用层
├── log-cli (jlog)
├── think-cli (think)
├── yue-cli (yue)
├── todo-cli (dida)
└── cang-cli (cang) - 通过兼容层
```

## 依赖版本对照表

| 包 | typer | rich | dong-core |
|---|-------|------|-----------|
| dong-core | >=0.12.0 | >=13.0.0 | - |
| log-cli | >=0.9.0 | >=13.0.0 | >=0.1.0 |
| think-cli | >=0.9.0 | >=13.0.0 | >=0.1.0 |
| yue-cli | >=0.12.0 | (传递) | >=0.1.0 |
| todo-cli | >=0.12.0 | >=13.0.0 | >=0.1.0 |
| cang-cli | >=0.12.0 | (传递) | >=0.1.0 |

## 安装顺序

```bash
# 1. 先安装 core
pip install -e ./dong-core

# 2. 安装各 CLI
pip install -e ./log-cli
pip install -e ./think-cli
pip install -e ./yue-cli
pip install -e ./todo-cli
pip install -e ./cang-cli
```

## 本地数据位置

```
~/.dong/
├── log/log.db       → jlog 命令
├── think/think.db   → think 命令
├── yue/yue.db       → yue 命令
├── cang/cang.db     → cang 命令
└── todo/todo.db     → dida 命令
```
