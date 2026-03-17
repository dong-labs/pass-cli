# dong-core

咚咚家族核心库 - 共享基础设施。

## 开发状态

项目正在开发中，以下模块待实现：

- `output/formatter.py` - JSON 输出装饰器
- `errors/exceptions.py` - 错误类型
- `dates/utils.py` - 日期处理工具
- `testing/fixtures.py` - 测试 fixtures

## 测试

测试框架已准备就绪，等待模块实现完成后编写具体测试。

### 运行测试

```bash
# 运行所有测试
pytest

# 运行单元测试
pytest tests/unit/

# 运行带覆盖率的测试
pytest --cov=dong --cov-report=html

# 查看覆盖率报告
open htmlcov/index.html
```

### 测试文件结构

```
tests/
├── __init__.py
├── conftest.py          # pytest 配置和共享 fixtures
├── data/                # 测试数据
├── unit/                # 单元测试
│   ├── test_formatter.py
│   ├── test_exceptions.py
│   ├── test_dates.py
│   └── test_fixtures.py
└── integration/         # 集成测试
    └── test_integration.py
```

## 覆盖率目标

- `formatter.py`: 90%+
- `exceptions.py`: 100%
- `dates.py`: 90%+
- `fixtures.py`: 80%+
- 整体: >= 80%
