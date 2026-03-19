# XBot Server

> XBot 后端 - OpenClaw Bot 平台

---

## 快速开始

### 1. 安装依赖

```bash
npm install
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件
```

### 3. 初始化数据库

```bash
npm run db:push
```

### 4. 启动服务

```bash
npm run dev
```

---

## API

### WebSocket 端点

```
ws://localhost:3001?device_id=<device_id>
```

### 方法

| 方法 | 说明 |
|------|------|
| `create_bot` | 创建 Bot |
| `list_bots` | Bot 列表 |
| `get_bot` | Bot 详情 |
| `delete_bot` | 删除 Bot |
| `send_message` | 发送消息 |
| `get_history` | 历史消息 |

---

## 部署

### Docker

```bash
docker-compose up -d
```

---

## 开发

```bash
# 开发模式（自动重启）
npm run dev

# 数据库管理
npm run db:studio
```

---

## 配置

| 变量 | 说明 |
|------|------|
| `PORT` | HTTP 端口（默认 3000）|
| `WS_PORT` | WebSocket 端口（默认 3001）|
| `DATABASE_URL` | PostgreSQL 连接串 |
| `OPENCLAW_GATEWAY_URL` | OpenClaw Gateway 地址 |
| `OPENCLAW_GATEWAY_TOKEN` | OpenClaw Gateway Token |
