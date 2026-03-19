# 咚咚家族 CLI - 待办事项

## ✅ 已完成

- [x] dong-core 开发完成 (99.2% 测试覆盖率)
- [x] log-cli 迁移到 dong-core
- [x] think-cli 迁移到 dong-core
- [x] yue-cli 迁移到 dong-core
- [x] todo-cli (dida-cli) 完成开发并使用 dong-core
- [x] cang-cli 通过兼容层迁移到 dong-core
- [x] 所有数据库添加 updated_at 字段
- [x] cang-cli schema v1 → v2 升级

## 测试任务（后期进行）

- [ ] log-cli 测试套件（目标覆盖率 >= 80%）
- [ ] think-cli 测试套件（目标覆盖率 >= 80%）
- [ ] yue-cli 测试套件（目标覆盖率 >= 80%）
- [ ] todo-cli 测试套件（目标覆盖率 >= 80%）
- [ ] cang-cli 测试套件（目标覆盖率 >= 80%）

## 可选优化

- [ ] 统一 typer 版本到 >=0.12.0 (log-cli/think-cli 目前用 >=0.9.0)
- [ ] 显式声明 rich 依赖 (yue-cli/cang-cli)
- [ ] 确认 todo-cli 命令名 (dida vs todo)
