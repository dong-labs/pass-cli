# XBot 技术选型

> 版本：1.0
> 更新时间：2026-03-17
> 设计原则：极简、快速验证

---

## 1. 架构设计

### 1.1 整体架构

```
┌─────────────────────────────────────────────┐
│          Flutter App（iOS + Android）       │
│  • XBot Admin 对话界面                      │
│  • 创建 Bot / Bot 列表                      │
│  • 对话界面（模仿 Telegram）                │
└──────────────────┬──────────────────────────┘
                   │ WebSocket
                   ▼
┌─────────────────────────────────────────────┐
│          XBot 后端（Node.js）               │
│  • WebSocket 服务（给 App）                 │
│  • Bot 管理（创建/查询/列表）               │
│  • 消息路由（用户 ↔ Agent）                 │
│  • Token 生成                               │
└──────────────────┬──────────────────────────┘
                   │ WebSocket
                   ▼
┌─────────────────────────────────────────────┐
│          OpenClaw Gateway                    │
│  • Agent 对话（仓咚咚、阅咚咚...）          │
│  • 地址：ws://127.0.0.1:18789               │
└─────────────────────────────────────────────┘
```

### 1.2 数据流

```
用户发消息：
App → XBot 后端 → OpenClaw Gateway → Agent 响应 → XBot 后端 → App

创建 Bot：
App → XBot 后端（生成 Token）→ App（显示 Token）
```

---

## 2. 技术栈

### 2.1 App 端（Flutter）

| 组件 | 技术 | 理由 |
|------|------|------|
| **框架** | Flutter 3.x | 跨平台、你熟悉 |
| **语言** | Dart | Flutter 原生 |
| **状态管理** | Provider / Riverpod | 简单够用 |
| **网络** | web_socket_channel | WebSocket 支持 |
| **UI** | Material Design | 模仿 Telegram |

### 2.2 后端（Node.js）

| 组件 | 技术 | 理由 |
|------|------|------|
| **运行时** | Node.js 20+ | 成熟、生态好 |
| **框架** | Express / Fastify | 轻量、快速 |
| **WebSocket** | ws / socket.io | 长连接 |
| **数据库** | PostgreSQL | 稳定、功能强 |
| **ORM** | Prisma | 类型安全 |
| **认证** | 无（设备 ID）| 极简 |

### 2.3 部署

| 组件 | 技术 | 说明 |
|------|------|------|
| **容器** | Docker | 标准化 |
| **服务器** | 阿里云 ECS | 你已有 |
| **反向代理** | Nginx | SSL、负载均衡 |
| **域名** | 待定 | 你后续提供 |

---

## 3. 数据模型

### 3.1 Bot 表

```sql
CREATE TABLE bots (
  id SERIAL PRIMARY KEY,
  device_id VARCHAR(255) NOT NULL,        -- 设备 ID（识别用户）
  name VARCHAR(255) NOT NULL,             -- Bot 名称
  token VARCHAR(64) UNIQUE NOT NULL,      -- Bot Token
  agent_id VARCHAR(255),                  -- Agent ID（仓咚咚、阅咚咚...）
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### 3.2 Message 表

```sql
CREATE TABLE messages (
  id SERIAL PRIMARY KEY,
  bot_id INTEGER REFERENCES bots(id),
  role VARCHAR(20) NOT NULL,              -- user / assistant
  content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### 3.3 Conversation 表（可选）

```sql
CREATE TABLE conversations (
  id SERIAL PRIMARY KEY,
  bot_id INTEGER REFERENCES bots(id),
  device_id VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

---

## 4. API 设计

### 4.1 WebSocket 协议（App ↔ 后端）

#### 连接

```
ws://xbot.yourdomain.com/ws?device_id=<device_id>
```

#### 消息格式

**请求：**
```json
{
  "type": "req",
  "id": "uuid",
  "method": "create_bot",
  "params": {
    "name": "我的助手",
    "agent_id": "cang"
  }
}
```

**响应：**
```json
{
  "type": "res",
  "id": "uuid",
  "ok": true,
  "payload": {
    "bot": {
      "id": 1,
      "name": "我的助手",
      "token": "xbot_abc123...",
      "agent_id": "cang"
    }
  }
}
```

**事件：**
```json
{
  "type": "event",
  "event": "message",
  "payload": {
    "bot_id": 1,
    "role": "assistant",
    "content": "收到！吱~"
  }
}
```

#### 方法列表

| 方法 | 说明 |
|------|------|
| `create_bot` | 创建 Bot |
| `list_bots` | Bot 列表 |
| `get_bot` | Bot 详情 |
| `delete_bot` | 删除 Bot |
| `send_message` | 发送消息 |

### 4.2 后端 ↔ OpenClaw Gateway

#### 连接

```
ws://127.0.0.1:18789
```

#### 握手

```json
{
  "type": "req",
  "id": "1",
  "method": "connect",
  "params": {
    "minProtocol": 1,
    "maxProtocol": 1,
    "client": {
      "id": "xbot",
      "displayName": "XBot",
      "version": "1.0.0"
    },
    "auth": {
      "token": "<gateway_token>"
    }
  }
}
```

#### 发送消息

```json
{
  "type": "req",
  "id": "2",
  "method": "chat",
  "params": {
    "agent_id": "cang",
    "message": "今天花了50元"
  }
}
```

---

## 5. 项目结构

### 5.1 后端结构

```
xbot-server/
├── package.json
├── prisma/
│   └── schema.prisma
├── src/
│   ├── index.js              # 入口
│   ├── websocket/
│   │   ├── server.js         # WebSocket 服务
│   │   └── handlers.js       # 消息处理
│   ├── services/
│   │   ├── bot.js            # Bot 服务
│   │   ├── message.js        # 消息服务
│   │   └── openclaw.js       # OpenClaw 集成
│   ├── utils/
│   │   └── token.js          # Token 生成
│   └── config/
│       └── index.js          # 配置
├── Dockerfile
└── docker-compose.yml
```

### 5.2 App 结构

```
xbot-app/
├── lib/
│   ├── main.dart
│   ├── app.dart
│   ├── screens/
│   │   ├── home/
│   │   │   └── home_screen.dart
│   │   ├── chat/
│   │   │   └── chat_screen.dart
│   │   └── create_bot/
│   │       └── create_bot_screen.dart
│   ├── services/
│   │   ├── websocket.dart
│   │   └── bot.dart
│   ├── providers/
│   │   ├── bots.dart
│   │   └── messages.dart
│   └── models/
│       ├── bot.dart
│       └── message.dart
├── pubspec.yaml
└── ...
```

---

## 6. 开发计划

### 6.1 Week 1：核心功能

| 天数 | 后端任务 | 前端任务 |
|------|----------|----------|
| 1 | 项目初始化 + Prisma | Flutter 项目初始化 |
| 2 | WebSocket 服务 + Bot API | 首页布局 |
| 3 | OpenClaw Gateway 集成 | 创建 Bot 页面 |
| 4 | 消息路由 | Bot 列表 |
| 5 | 测试 + 修复 | 对话界面 |

### 6.2 Week 2：完善 + 部署

| 天数 | 任务 |
|------|------|
| 6 | 联调 App + 后端 |
| 7 | 联调后端 + OpenClaw |
| 8 | UI 优化 + Bug 修复 |
| 9 | Docker 化 |
| 10 | 部署到阿里云 |

---

## 7. 配置

### 7.1 环境变量（后端）

```bash
# 服务配置
PORT=3000
WS_PORT=3001

# 数据库
DATABASE_URL=postgresql://user:pass@localhost:5432/xbot

# OpenClaw Gateway
OPENCLAW_GATEWAY_URL=ws://127.0.0.1:18789
OPENCLAW_GATEWAY_TOKEN=<your_token>
```

### 7.2 配置文件（App）

```dart
// lib/config.dart
class Config {
  static const String wsUrl = 'ws://xbot.yourdomain.com/ws';
}
```

---

## 8. 技术风险

| 风险 | 说明 | 应对 |
|------|------|------|
| **WebSocket 断线** | 网络不稳定 | 自动重连机制 |
| **OpenClaw Gateway 断线** | Gateway 服务重启 | 重连 + 错误提示 |
| **Token 冲突** | 随机生成可能重复 | 使用 UUID + 检查 |
| **并发问题** | 多用户同时访问 | 使用连接池 |

---

## 9. 后续优化

### 9.1 性能优化

- Redis 缓存（Bot 列表）
- 消息压缩
- WebSocket 心跳

### 9.2 功能扩展

- 多 Agent 选择
- 对话历史
- 消息搜索
- Bot 分享

---

## 10. 总结

### 核心技术

| 层级 | 技术 |
|------|------|
| **App** | Flutter + WebSocket |
| **后端** | Node.js + Express + Prisma + PostgreSQL |
| **连接** | WebSocket（双向） |
| **部署** | Docker + 阿里云 |

### MVP 范围

- ✅ App 首页（XBot Admin）
- ✅ 创建 Bot（生成 Token）
- ✅ Bot 列表
- ✅ 对话界面
- ✅ OpenClaw Agent 集成
- ✅ 部署到阿里云

---

**下一步：创建项目骨架**
