# dong-pass 设计文档

> 密码管理 CLI - 帮你存储账号密码

---

## 1. 需求场景

| 场景 | 痛点 |
|------|------|
| **账号太多** | 记不住、找不到 |
| **密码复杂** | 账号本子翻半天 |
| **分类管理** | 工作/个人/金融账号混在一起 |
| **快速访问** | 需要时立即拿到 |

---

## 2. 核心需求

1. **存储账号密码**：网站、账号、密码
2. **分类管理**：工作/个人/金融/社交
3. **快速查询**：按网站名快速找到
4. **加密存储**：可选加密，主密码保护
5. **统计信息**：查看有多少账号

---

## 3. 数据结构

```sql
CREATE TABLE accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    site TEXT NOT NULL,           -- 网站名称
    account TEXT NOT NULL,        -- 账号
    password TEXT NOT NULL,       -- 密码（加密或明文）
    nickname TEXT,                -- 昵称
    category TEXT,                -- 分类
    note TEXT,                    -- 备注
    encrypted BOOLEAN DEFAULT 0,  -- 是否加密
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    last_used_at TEXT             -- 最后使用时间
);
```

---

## 4. 命令设计

### 4.1 初始化

```bash
dong-pass init [--master-password "xxx"]
```

**参数**：
- `--master-password`：主密码（用于加密）

**示例**：
```bash
# 明文存储
dong-pass init

# 加密存储
dong-pass init --master-password "MySecretKey"
```

---

### 4.2 添加账号

```bash
dong-pass add <网站> --account <账号> --password <密码> [选项]
```

**参数**：
- `<网站>`：网站名称
- `--account`：账号
- `--password`：密码

**选项**：
- `--nickname`：昵称
- `--category`：分类（工作/个人/金融/社交/其他）
- `--note`：备注
- `--encrypt`：加密存储

**示例**：
```bash
# 添加 GitHub 账号
dong-pass add github --account gudongtongxue --password "Gudong123!@#" --category "个人"

# 添加阿里云账号（加密）
dong-pass add aliyun --account gudong@aliyun.com --password "Aliyun456$" --category "工作" --encrypt

# 添加微博账号（带备注）
dong-pass add weibo --account gudongtongxue --password "Weibo789#" --nickname "工作微博" --category "社交"
```

---

### 4.3 查询账号

```bash
dong-pass get <网站>
```

**示例**：
```bash
dong-pass get github

# 输出：
# 网站：github.com
# 账号：gudongtongxue
# 密码：Gudong123!@#
# 分类：个人
# 最后使用：2026-03-19
```

---

### 4.4 列出所有

```bash
dong-pass list [选项]
```

**选项**：
- `--category <分类>`：按分类筛选
- `--limit <数量>`：限制数量

**示例**：
```bash
# 列出所有
dong-pass list

# 列出工作类
dong-pass list --category 工作
```

---

### 4.5 搜索

```bash
dong-pass search <关键词>
```

**示例**：
```bash
# 搜索包含 "aliyun" 的账号
dong-pass search aliyun

# 搜索所有个人类账号
dong-pass search --category 个人
```

---

### 4.6 更新账号

```bash
dong-pass update <网站> [选项]
```

**选项**：
- `--account`：更新账号
- `--password`：更新密码
- `--nickname`：更新昵称
- `--category`：更新分类
- `--note`：更新备注

**示例**：
```bash
# 更新密码
dong-pass update github --password "NewPassword123!"

# 更新分类
dong-pass update weibo --category "个人"
```

---

### 4.7 删除账号

```bash
dong-pass delete <网站> [--force]
```

**示例**：
```bash
# 删除账号（需要确认）
dong-pass delete github

# 强制删除（不确认）
dong-pass delete github --force
```

---

### 4.8 统计信息

```bash
dong-pass stats
```

**输出**：
```
账号统计：
- 总数：12
- 工作：5
- 个人：4
- 金融：2
- 社交：1
```

---

### 4.9 导出/导入

```bash
# 导出为 JSON
dong-pass export --output accounts.json

# 从 JSON 导入
dong-pass import --input accounts.json
```

---

### 4.10 加密相关

```bash
# 设置主密码（首次设置）
dong-pass set-master

# 更改主密码
dong-pass change-master

# 移除加密（明文化）
dong-pass remove-encrypt
```

---

## 5. 加密机制

### 方式 1：明文存储（默认）

```bash
# 不设置主密码
dong-pass init

# 添加时密码明文存储
dong-pass add github --account gudong --password "123456"
```

### 方式 2：加密存储

```bash
# 设置主密码
dong-pass init --master-password "MySecretKey"

# 添加时加密
dong-pass add github --account gudong --password "123456" --encrypt

# 查询时需要输入主密码
dong-pass get github
# 输入主密码: MySecretKey
# 显示密码: 123456
```

---

## 6. AI 友好设计

所有命令支持 JSON 输出：

```bash
dong-pass get github
# {"success": true, "data": {"site": "github", "account": "gudong", ...}}

dong-pass list --category 工作
# {"success": true, "data": {"items": [...], "total": 5}}
```

---

## 7. 数据库位置

```
~/.dong/accounts.db
```

---

## 8. 版本规划

| 版本 | 功能 |
|------|------|
| v0.1.0 | 基础 CRUD、分类管理 |
| v0.2.0 | 加密存储 |
| v0.3.0 | 导出/导入 |

---

**文档版本**：v1.0
**创建时间**：2026-03-19
**作者**：小牛牛 🐮💻
