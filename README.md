# 密码咚（dong-pass）

账号密码管理 CLI - 帮你安全存储和管理账号密码

## 安装

```bash
pipx install dong-pass
```

## 快速开始

```bash
# 初始化
dong-pass init

# 添加账号
dong-pass add github --account gudongtongxue --password "Gudong123!@#" --category "个人"

# 查询账号
dong-pass get github

# 列出所有
dong-pass list

# 统计
dong-pass stats
```

## 命令

| 命令 | 说明 |
|------|------|
| `init` | 初始化数据库 |
| `add` | 添加账号 |
| `get` | 获取账号 |
| `list` | 列出所有 |
| `delete` | 删除账号 |
| `stats` | 统计信息 |

## License

MIT
