# CLI 命名规范化执行计划

> 统一咚咚家族 CLI 的包名和命令命名规范

---

## 1. 目标

### 1.1 包名规范

| 当前包名 | 目标包名 | 改动 |
|---------|---------|------|
| dong-core | dong-core | ✅ 保持 |
| cang-cli | cang-cli | ✅ 保持 |
| jidongdong | **log-cli** | ❌ 需改名 |
| dong-read | **read-cli** | ❌ 需改名 |
| think-cli | think-cli | ✅ 保持 |
| dida-cli | dida-cli | ✅ 保持 |

### 1.2 CLI 命令规范

| 当前命令 | 目标命令 | 改动 |
|---------|---------|------|
| cang | **dong-cang** | ❌ 需改名 |
| jlog | **dong-log** | ❌ 需改名 |
| dr | **dong-read** | ❌ 需改名 |
| think | **dong-think** | ❌ 需改名 |
| dida | **dong-dida** | ❌ 需改名 |

---

## 2. 最终效果

```bash
# 安装
pipx install cang-cli      # dong-cang
pipx install log-cli       # dong-log
pipx install read-cli      # dong-read
pipx install think-cli     # dong-think
pipx install dida-cli      # dong-dida

# 使用
dong-cang add "收入 100"
dong-log add "今天做了XX"
dong-read add "一句话"
dong-think add "一个想法"
dong-dida add "一个待办"
```

---

## 3. 执行步骤

### Phase 1: 代码修改（每个仓库）

#### 3.1 log-cli（记咚咚）

**仓库**：https://github.com/dong-labs/log-cli

**文件修改**：
```toml
# pyproject.toml
[project]
name = "log-cli"  # 从 jidongdong 改为 log-cli

[project.scripts]
dong-log = "log.cli:app"  # 从 jlog 改为 dong-log
```

**数据库路径**：保持 `~/.dong/log.db`（不变）

**提交信息**：`Rename package to log-cli, CLI to dong-log`

---

#### 3.2 read-cli（读咚咚）

**仓库**：https://github.com/dong-labs/dong-read

**文件修改**：
```toml
# pyproject.toml
[project]
name = "read-cli"  # 从 dong-read 改为 read-cli

[project.scripts]
dong-read = "read.cli:app"  # 从 dr 改为 dong-read
```

**数据库路径**：保持 `~/.dong/read.db`（不变）

**提交信息**：`Rename package to read-cli, CLI to dong-read`

**仓库重命名**：GitHub 仓库从 `dong-read` 重命名为 `read-cli`

---

#### 3.3 cang-cli（仓咚咚）

**仓库**：https://github.com/dong-labs/cang-cli

**文件修改**：
```toml
# pyproject.toml
[project.scripts]
dong-cang = "cang.cli:app"  # 从 cang 改为 dong-cang
```

**数据库路径**：保持 `~/.dong/cang.db`（不变）

**提交信息**：`Rename CLI from cang to dong-cang`

---

#### 3.4 think-cli（思咚咚）

**仓库**：https://github.com/dong-labs/think-cli

**文件修改**：
```toml
# pyproject.toml
[project.scripts]
dong-think = "think.cli:app"  # 从 think 改为 dong-think
```

**数据库路径**：保持 `~/.dong/think.db`（不变）

**提交信息**：`Rename CLI from think to dong-think`

---

#### 3.5 dida-cli（事咚咚）

**仓库**：https://github.com/dong-labs/dida-cli

**文件修改**：
```toml
# pyproject.toml
[project.scripts]
dong-dida = "dida.cli:app"  # 从 dida 改为 dong-dida
```

**数据库路径**：保持 `~/.dong/dida.db`（不变）

**提交信息**：`Rename CLI from dida to dong-dida`

---

### Phase 2: 发布流程（每个仓库）

```bash
# 1. 修改代码
git add -A
git commit -m "Rename package/CLI"

# 2. 打标签
git tag v0.4.0  # 新版本号

# 3. 推送到 GitHub
git push && git push --tags

# 4. 发布到 PyPI
hatch build && twine upload dist/*
```

---

### Phase 3: 本地升级

```bash
# 卸载旧版本
pipx uninstall jidongdong dong-read cang-cli think-cli dida-cli

# 安装新版本
pipx install log-cli
pipx install read-cli
pipx install cang-cli
pipx install think-cli
pipx install dida-cli
```

---

### Phase 4: 更新智能体配置

每个智能体的 TOOLS.md 需要更新命令名称。

---

## 4. 版本规划

| 包名 | 当前版本 | 新版本 | 主要改动 |
|------|---------|--------|---------|
| log-cli | 0.3.0 | **0.4.0** | 包名 jidongdong→log-cli，命令 jlog→dong-log |
| read-cli | 0.4.0 | **0.5.0** | 包名 dong-read→read-cli，命令 dr→dong-read |
| cang-cli | 0.3.0 | **0.4.0** | 命令 cang→dong-cang |
| think-cli | 0.3.0 | **0.4.0** | 命令 think→dong-think |
| dida-cli | 0.3.0 | **0.4.0** | 命令 dida→dong-dida |

---

## 5. 负责人分配

| 任务 | 负责人 | 状态 |
|------|--------|------|
| log-cli 改名发布 | cloud code | 待分配 |
| read-cli 改名发布 | cloud code | 待分配 |
| cang-cli 改名发布 | cloud code | 待分配 |
| think-cli 改名发布 | cloud code | 待分配 |
| dida-cli 改名发布 | cloud code | 待分配 |
| 更新智能体 TOOLS.md | 小牛牛 | 待执行 |

---

## 6. 最终对照表

### 6.1 仓库与包名

| 仓库名 | 包名 | CLI 命令 | 功能 |
|--------|------|----------|------|
| dong-core | dong-core | - | 核心库 |
| cang-cli | cang-cli | `dong-cang` | 仓咚咚 - 财务管理 |
| log-cli | log-cli | `dong-log` | 记咚咚 - 日常日志 |
| read-cli | read-cli | `dong-read` | 读咚咚 - 知识摘录 |
| think-cli | think-cli | `dong-think` | 思咚咚 - 灵感想法 |
| dida-cli | dida-cli | `dong-dida` | 事咚咚 - 待办管理 |

### 6.2 数据库路径（不变）

| CLI | 数据库路径 |
|-----|-----------|
| dong-cang | ~/.dong/cang.db |
| dong-log | ~/.dong/log.db |
| dong-read | ~/.dong/read.db |
| dong-think | ~/.dong/think.db |
| dong-dida | ~/.dong/dida.db |

---

## 7. 兼容性说明

- **数据完全兼容**：数据库路径不变，用户数据无需迁移
- **需要重新安装**：旧命令（jlog/dr/cang/think/dida）将不再维护
- **过渡期**：建议保留旧包 30 天后下架

---

**文档版本**：v1.0
**创建时间**：2026-03-19
**作者**：小牛牛 🐮💻
