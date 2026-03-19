# TOOLS.md - 工具箱

我的核心工具是 `dong-pass` CLI。

## 安装

```bash
pipx install dong-pass
```

## 命令列表

### 初始化

```bash
dong-pass init
```

### 添加账号

```bash
# 添加 GitHub 账号
dong-pass add github --account gudongtongxue --password "Gudong123!@#" --category "个人"

# 添加阿里云账号
dong-pass add aliyun --account gudong@aliyun.com --password "Aliyun456$" --category "工作"

# 添加微博账号
dong-pass add weibo --account gudongtongxue --password "Weibo789#" --category "社交"
```

### 查询账号

```bash
dong-pass get github

# 输出：
# 网站：github.com
# 账号：gudongtongxue
# 密码：Gudong123!@#
# 分类：个人
```

### 列出所有

```bash
# 列出所有
dong-pass list

# 列出工作类
dong-pass list --category 工作
```

### 删除账号

```bash
# 删除账号（需要确认）
dong-pass delete --site github
```

### 统计信息

```bash
dong-pass stats
```

## 数据库

数据存储在 `~/.dong/accounts.db`

---

*🔒 安全存储，随时访问*
