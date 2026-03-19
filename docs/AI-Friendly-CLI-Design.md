# AI 友好 CLI 设计方案

> 咚咚家族 CLI 工具 AI 优化方案

---

## 1. 背景

### 1.1 为什么需要 AI 友好的 CLI？

咚咚家族 CLI（jlog/dr/think/dida）的设计初衷是 **AI Native** —— 让 AI 能够像人类一样使用这些工具来管理信息。

**核心问题**：AI 的上下文窗口有限，不能一次性读取所有数据。AI 需要：
- 快速搜索定位相关信息
- 获取数据概览/统计
- 通过标签/关键词筛选
- 理解数据摘要

**现状**：大部分 CLI 缺少这些 AI 友好功能。

---

## 2. 当前状态分析

### 2.1 功能支持情况

| CLI | search | stats | tags 字段 | summary | AI 可用性 |
|-----|--------|-------|-----------|---------|-----------|
| **jlog** | ❌ | ❌ | ❌ | ❌ | ⚠️ 低 |
| **dr** | ✅ | ❌ | ❌ | ❌ | ⚠️ 中 |
| **think** | ✅ | ✅ | ❌ | ❌ | ✅ 中高 |
| **dida** | ✅ | ✅ | ❌ | ❌ | ✅ 中高 |

### 2.2 具体问题

#### jlog（记咚咚）
- ❌ **无法搜索**：AI 找不到相关日志，只能遍历
- ❌ **无统计**：不知道有多少条、按分组分布
- ❌ **无标签**：无法按主题分类

#### dr（读咚咚）
- ✅ 有搜索
- ❌ **无统计**：不知道收集了多少摘录、按类型分布
- ❌ **无标签**：无法按主题分类

#### think（思咚咚）
- ✅ 有搜索
- ✅ 有统计
- ❌ **无标签**：想法无法按主题分类

#### dida（事咚咚）
- ✅ 有搜索
- ✅ 有统计
- ❌ **无标签**：待办无法按项目分类

---

## 3. 解决方案

### 3.1 设计原则

1. **AI 和人类共用同一套命令**：不搞 `ai` 子命令
2. **JSON 优先**：所有输出默认 JSON，AI 直接解析
3. **最小改动**：只补充缺失功能，不改架构
4. **统一接口**：所有 CLI 保持一致的命令和参数

### 3.2 功能设计

#### 3.2.1 search 命令（所有 CLI）

```bash
# 全文搜索
<cli> search "关键词" [--limit N] [--field FIELD]

# 示例
jlog search "inBox" --limit 10
dr search "AI" --field content
think search "三层架构"
dida search "微博" --limit 5
```

**输出格式**：
```json
{
  "success": true,
  "data": {
    "query": "inBox",
    "total": 3,
    "items": [...]
  }
}
```

#### 3.2.2 stats 命令（所有 CLI）

```bash
# 统计概览
<cli> stats [--recent ND]

# 示例
jlog stats
jlog stats --recent 7d
dr stats
think stats
dida stats
```

**输出格式**：
```json
{
  "success": true,
  "data": {
    "total": 45,
    "recent_7d": 12,
    "by_group": {"work": 10, "life": 20, "indie": 15},
    "by_tag": {"重要": 8, "日常": 12}
  }
}
```

#### 3.2.3 tags 字段（所有 CLI）

**数据库新增 tags 字段**：
```sql
ALTER TABLE logs ADD COLUMN tags TEXT;  -- jlog
ALTER TABLE items ADD COLUMN tags TEXT; -- dr
ALTER TABLE ideas ADD COLUMN tags TEXT; -- think
ALTER TABLE todos ADD COLUMN tags TEXT; -- dida
```

**CLI 支持**：
```bash
# 添加时指定标签
<cli> add "内容" --tags "标签1,标签2"

# 按标签筛选
<cli> list --tag "标签"
<cli> list --tags "标签1,标签2"  # 多标签 OR

# 列出所有标签
<cli> tags
```

**输出格式**：
```json
{
  "success": true,
  "data": {
    "id": 1,
    "content": "...",
    "tags": ["重要", "工作"],
    ...
  }
}
```

---

## 4. 各 CLI 改造详情

### 4.1 jlog（记咚咚）

**新增命令**：
| 命令 | 说明 |
|------|------|
| `jlog search "关键词"` | 搜索日志内容 |
| `jlog stats` | 统计日志（总数、分组分布、标签分布） |
| `jlog tags` | 列出所有标签及数量 |

**改造命令**：
| 命令 | 改动 |
|------|------|
| `jlog add` | 新增 `--tags` 参数 |
| `jlog list` | 新增 `--tag` 参数 |

**数据库改动**：
```sql
ALTER TABLE logs ADD COLUMN tags TEXT DEFAULT '';
CREATE INDEX idx_logs_tags ON logs(tags);
```

### 4.2 dr（读咚咚）

**新增命令**：
| 命令 | 说明 |
|------|------|
| `dr stats` | 统计摘录（总数、类型分布、标签分布） |
| `dr tags` | 列出所有标签及数量 |

**改造命令**：
| 命令 | 改动 |
|------|------|
| `dr add` | 新增 `--tags` 参数 |
| `dr ls` | 新增 `--tag` 参数 |

**数据库改动**：
```sql
ALTER TABLE items ADD COLUMN tags TEXT DEFAULT '';
CREATE INDEX idx_items_tags ON items(tags);
```

### 4.3 think（思咚咚）

**新增命令**：
| 命令 | 说明 |
|------|------|
| `think tags` | 列出所有标签及数量 |

**改造命令**：
| 命令 | 改动 |
|------|------|
| `think add` | 新增 `--tags` 参数 |
| `think list` | 新增 `--tag` 参数 |

**数据库改动**：
```sql
ALTER TABLE ideas ADD COLUMN tags TEXT DEFAULT '';
CREATE INDEX idx_ideas_tags ON ideas(tags);
```

### 4.4 dida（事咚咚）

**新增命令**：
| 命令 | 说明 |
|------|------|
| `dida tags` | 列出所有标签及数量 |

**改造命令**：
| 命令 | 改动 |
|------|------|
| `dida add` | 新增 `--tags` 参数 |
| `dida ls` | 新增 `--tag` 参数 |

**数据库改动**：
```sql
ALTER TABLE todos ADD COLUMN tags TEXT DEFAULT '';
CREATE INDEX idx_todos_tags ON todos(tags);
```

---

## 5. AI 使用示例

### 5.1 场景：AI 查找用户的工作日志

```bash
# AI 先看统计
jlog stats
# {"total": 45, "by_group": {"work": 10, ...}}

# AI 搜索工作相关
jlog search "工作" --limit 10
# {"items": [...]}

# AI 按标签筛选
jlog list --tag "重要"
# {"items": [...]}
```

### 5.2 场景：AI 了解用户最近在关注什么

```bash
# AI 获取最近统计
jlog stats --recent 7d
dr stats --recent 7d
think stats --recent 7d
dida stats --recent 7d

# AI 综合分析，给用户建议
```

### 5.3 场景：AI 帮用户整理知识库

```bash
# AI 查看标签分布
dr tags
# {"tags": [{"name": "AI", "count": 5}, {"name": "设计", "count": 3}]}

# AI 搜索特定主题
dr search "Agent" --limit 20
# {"items": [...]}

# AI 总结给用户
```

---

## 6. 实现计划

### Phase 1：jlog 增强（优先级最高）
- [ ] 新增 `search` 命令
- [ ] 新增 `stats` 命令
- [ ] 新增 `tags` 命令
- [ ] `add` 支持 `--tags`
- [ ] `list` 支持 `--tag`
- [ ] 数据库迁移脚本

### Phase 2：dr 增强
- [ ] 新增 `stats` 命令
- [ ] 新增 `tags` 命令
- [ ] `add` 支持 `--tags`
- [ ] `ls` 支持 `--tag`
- [ ] 数据库迁移脚本

### Phase 3：think 增强
- [ ] 新增 `tags` 命令
- [ ] `add` 支持 `--tags`
- [ ] `list` 支持 `--tag`
- [ ] 数据库迁移脚本

### Phase 4：dida 增强
- [ ] 新增 `tags` 命令
- [ ] `add` 支持 `--tags`
- [ ] `ls` 支持 `--tag`
- [ ] 数据库迁移脚本

---

## 7. 版本规划

| CLI | 当前版本 | 目标版本 | 主要改动 |
|-----|---------|---------|---------|
| jlog | 0.2.1 | 0.3.0 | +search +stats +tags |
| dr | 0.3.3 | 0.4.0 | +stats +tags |
| think | 0.2.0 | 0.3.0 | +tags |
| dida | 0.2.3 | 0.3.0 | +tags |

---

## 8. 兼容性说明

- **向后兼容**：新增字段有默认值，旧数据不受影响
- **迁移脚本**：提供自动迁移脚本，无需手动操作
- **降级安全**：如果降级版本，tags 字段会被忽略但不报错

---

## 9. 总结

### 改造前
- AI 只能遍历所有数据
- 无法快速定位信息
- 无法了解数据全貌

### 改造后
- AI 可以搜索定位
- AI 可以获取统计概览
- AI 可以按标签筛选
- 所有 CLI 保持一致的 AI 友好接口

---

**文档版本**：v1.0
**创建时间**：2026-03-19
**作者**：小牛牛 🐮💻
