# 到期日管理需求分析

> 咕咚的需求：管理各种服务的到期日，提前提醒续费

---

## 1. 场景分析

### 1.1 用户场景

| 服务类型 | 示例 | 周期 | 金额 | 提醒时间 |
|---------|------|------|------|----------|
| 云服务 | 阿里云ECS | 年付 | 1200元 | 30天、7天 |
| AI服务 | 智谱AI套餐 | 月付 | 99元 | 7天、1天 |
| 域名 | gudong.site | 年付 | 68元 | 30天、7天 |
| SSL证书 | Let's Encrypt | 3个月 | 免费 | 7天、1天 |
| 会员 | GitHub Copilot | 月付 | $10 | 7天 |
| 软件 | JetBrains | 年付 | $149 | 30天 |

### 1.2 核心需求

1. **记录到期日**：服务名称、到期日期、金额、分类
2. **提前提醒**：可配置提前多少天提醒
3. **周期续费**：支持月付/年付/自定义周期
4. **分类管理**：按服务类型分类
5. **即将到期视图**：快速查看30天内到期的服务
6. **续费记录**：记录续费历史

---

## 2. 现有工具分析

### 2.1 dida（事咚咚）现有功能

**已有字段**：
- content: 内容
- due_date: 到期日期 ✅ 已有
- priority: 优先级
- tags: 标签
- completed: 是否完成

**问题**：
- 待办是"完成后标记 done"，到期日是"到期后续费"，逻辑不同
- 缺少金额、周期、分类字段

### 2.2 其他方案

| 工具 | 说明 |
|------|------|
| Google Calendar | 可以设置提醒，但不够专业 |
| Notion | 灵活，但不是 CLI |
| 自建 CLI | 最灵活，符合咚咚家族风格 |

---

## 3. 方案对比

### 方案 A：扩展 dida

在现有 dida 基础上增加 `expire` 类型待办：

```bash
# 添加到期项
dong-dida add "阿里云ECS" --expire 2027-04-15 --cost 1200 --repeat yearly

# 查看即将到期
dong-dida expiring --days 30

# 续费
dong-dida renew 1 --to 2028-04-15
```

**数据结构**：
```sql
ALTER TABLE todos ADD COLUMN type TEXT DEFAULT 'task';  -- task/expire
ALTER TABLE todos ADD COLUMN cost REAL;
ALTER TABLE todos ADD COLUMN repeat TEXT;  -- monthly/yearly/none
```

**优点**：
- 复用现有代码
- 统一管理

**缺点**：
- 待办和到期混在一起
- 逻辑复杂

---

### 方案 B：新建 dong-expire（推荐）

专门的到期日管理工具：

```bash
# 安装
pipx install dong-expire

# 添加服务
dong-expire add "阿里云ECS" --expire 2027-04-15 --cost 1200 --category "云服务" --repeat yearly

# 列出所有
dong-expire list

# 按分类筛选
dong-expire list --category 云服务

# 即将到期
dong-expire remind --days 30

# 续费
dong-expire renew 1 --to 2028-04-15
dong-expire renew 1 --auto  # 自动延长一个周期

# 查看续费历史
dong-expire history 1

# 统计
dong-expire stats  # 本月/本年需续费的金额
```

**数据结构**：
```sql
CREATE TABLE expires (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,           -- 服务名称
    category TEXT,                -- 分类（云服务/AI服务/域名/证书）
    expire_date TEXT NOT NULL,    -- 到期日期
    cost REAL,                    -- 费用
    currency TEXT DEFAULT 'CNY',  -- 币种
    repeat TEXT,                  -- 重复周期（monthly/yearly/none）
    remind_days TEXT,             -- 提醒天数（30,7,1）
    status TEXT DEFAULT 'active', -- active/expired/cancelled
    note TEXT,                    -- 备注
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE renewals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expire_id INTEGER NOT NULL,
    old_date TEXT NOT NULL,
    new_date TEXT NOT NULL,
    cost REAL,
    renewed_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (expire_id) REFERENCES expires(id)
);
```

**优点**：
- 专注到期管理
- 逻辑清晰
- 独立数据库

**缺点**：
- 新增一个 CLI

---

## 4. 推荐方案：dong-expire

### 4.1 功能设计

| 命令 | 说明 |
|------|------|
| `dong-expire init` | 初始化数据库 |
| `dong-expire add` | 添加到期项 |
| `dong-expire list` | 列出所有 |
| `dong-expire remind` | 查看即将到期 |
| `dong-expire renew` | 续费 |
| `dong-expire history` | 续费历史 |
| `dong-expire stats` | 统计费用 |
| `dong-expire search` | 搜索 |
| `dong-expire update` | 更新 |
| `dong-expire delete` | 删除 |

### 4.2 使用示例

```bash
# 初始化
dong-expire init

# 添加服务
dong-expire add "阿里云ECS" --expire 2027-04-15 --cost 1200 --category "云服务" --repeat yearly
dong-expire add "智谱AI套餐" --expire 2026-04-15 --cost 99 --category "AI服务" --repeat monthly
dong-expire add "gudong.site域名" --expire 2027-03-20 --cost 68 --category "域名" --repeat yearly

# 查看即将到期（30天内）
dong-expire remind --days 30

# 输出：
# 即将到期：
# 1. 智谱AI套餐 - 2026-04-15 (还有 27 天) - ¥99
# 2. gudong.site域名 - 2027-03-20 (还有 365 天) - ¥68

# 续费
dong-expire renew 1 --auto  # 自动延长一个月
dong-expire renew 1 --to 2026-05-15  # 指定新日期

# 统计
dong-expire stats --year 2026
# 输出：
# 2026年到期费用统计：
# - 云服务: ¥1200
# - AI服务: ¥1188 (12个月)
# - 域名: ¥68
# 总计: ¥2456
```

### 4.3 提醒机制

**方案 A：手动查询**
```bash
# 用户主动查询
dong-expire remind --days 30
```

**方案 B：定时任务**
```bash
# 每天早上检查并发送通知
0 9 * * * dong-expire remind --days 7 --notify telegram
```

**方案 C：集成到智能体**
```python
# 小闹钟每天检查
if has_expiring_soon():
    notify_user()
```

---

## 5. AI 友好设计

```bash
# JSON 输出
dong-expire remind --days 30 --json

# 搜索
dong-expire search "阿里云"

# 按分类统计
dong-expire stats --category 云服务 --json
```

---

## 6. 数据库路径

```
~/.dong/expire.db
```

---

## 7. 版本规划

| 版本 | 功能 |
|------|------|
| v0.1.0 | 基础 CRUD、提醒 |
| v0.2.0 | 续费历史、统计 |
| v0.3.0 | 定时提醒、通知集成 |

---

## 8. 下一步

1. 确认方案（A 还是 B）
2. 开始开发
3. 集成到智能体

---

**文档版本**：v1.0
**创建时间**：2026-03-19
**作者**：小牛牛 🐮💻
