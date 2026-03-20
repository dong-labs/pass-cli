# XBot 产品规格

> 版本：1.0
> 更新时间：2026-03-17
> 设计风格：Telegram Bot 风格

---

## 1. 产品概述

### 1.1 核心定位

**XBot = 国内版 Telegram Bot 平台，专注 AI Agent 渠道**

### 1.2 核心价值

| 用户价值 | 说明 |
|----------|------|
| **极简创建** | 命令创建，秒级完成 |
| **即时可用** | Token 立即生成，扫码即用 |
| **无需审核** | 创建即上线 |
| **AI 原生** | 内置 OpenClaw Agent |

### 1.3 MVP 范围

| 功能 | 优先级 | 说明 |
|------|--------|------|
| 命令创建 Bot | P0 | /newbot |
| Bot 管理 | P0 | /mybots, /token |
| 微信接入 | P0 | 小程序扫码 |
| OpenClaw 集成 | P0 | 预置 Agent |

---

## 2. App 设计

### 2.1 信息架构

```
App
├── 首页（XBot Admin 对话）
│   ├── 命令输入
│   ├── 消息列表
│   └── 快捷按钮（可选）
│
├── Bot 详情（对话中展示）
│   ├── Bot 信息
│   ├── Token 显示
│   └── 小程序码
│
└── 设置（可选）
    ├── 账号信息
    └── 关于
```

### 2.2 首页设计

#### 布局

```
┌─────────────────────────────────────┐
│ 状态栏                              │
├─────────────────────────────────────┤
│ XBot                    [设置图标] │
├─────────────────────────────────────┤
│                                     │
│                                     │
│         消息/对话区域               │
│                                     │
│                                     │
│                                     │
│                                     │
├─────────────────────────────────────┤
│ [命令输入框]               [发送]  │
├─────────────────────────────────────┤
│ 快捷命令（可选）                    │
│ [/newbot] [/mybots] [/help]        │
└─────────────────────────────────────┘
```

#### 首次打开

```
┌─────────────────────────────────────┐
│ XBot                                │
├─────────────────────────────────────┤
│                                     │
│  🤖 XBot Admin                      │
│                                     │
│  👋 你好！我是 XBot Admin           │
│                                     │
│  🎉 欢迎使用 XBot！                 │
│                                     │
│  XBot 让你轻松创建 AI Bot，         │
│  并在微信里使用。                   │
│                                     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━          │
│  快速开始：                         │
│  1. 输入 /newbot 创建 Bot           │
│  2. 获取 Token 并扫码接入           │
│  3. 开始对话！                      │
│  ━━━━━━━━━━━━━━━━━━━━━━━━          │
│                                     │
│  💡 输入 /help 查看所有命令         │
│                                     │
├─────────────────────────────────────┤
│ [输入命令或消息]            [发送]  │
└─────────────────────────────────────┘
```

#### /newbot 流程

```
Step 1:
┌─────────────────────────────────────┐
│ 你：/newbot                         │
│                                     │
│ 🤖 XBot Admin：                     │
│ 好的，创建一个新 Bot！              │
│                                     │
│ 第一步：给 Bot 起个名字             │
│ （显示名称，如：我的助手）          │
└─────────────────────────────────────┘

Step 2:
┌─────────────────────────────────────┐
│ 你：我的财务助手                    │
│                                     │
│ 🤖 XBot Admin：                     │
│ ✅ 名称设置成功！                   │
│                                     │
│ 第二步：选择 AI Agent               │
│ 回复数字选择：                      │
│                                     │
│ 1️⃣ 仓咚咚（财务管理）              │
│ 2️⃣ 阅咚咚（阅读管理）              │
│ 3️⃣ 思咚咚（灵感管理）              │
│ 4️⃣ 事咚咚（待办管理）              │
│ 5️⃣ 自定义 Agent                    │
└─────────────────────────────────────┘

Step 3:
┌─────────────────────────────────────┐
│ 你：1                               │
│                                     │
│ 🤖 XBot Admin：                     │
│ 🎉 Bot 创建成功！                   │
│                                     │
│ ━━━━━━━━━━━━━━━━━━━━━━━━           │
│ 🤖 Bot 名称：我的财务助手           │
│ 🤖 Bot Agent：仓咚咚                │
│ 🤖 Bot Token：                      │
│    xbot_abc123def456ghi789          │
│ ━━━━━━━━━━━━━━━━━━━━━━━━           │
│                                     │
│ 📱 微信扫码接入：                   │
│                                     │
│    ┌────────────┐                  │
│    │            │                  │
│    │  [小程序码] │                  │
│    │            │                  │
│    └────────────┘                  │
│                                     │
│ 💾 长按保存 Token                   │
└─────────────────────────────────────┘
```

#### /mybots 流程

```
┌─────────────────────────────────────┐
│ 你：/mybots                         │
│                                     │
│ 🤖 XBot Admin：                     │
│ 📋 你有 2 个 Bot：                  │
│                                     │
│ 1️⃣ 我的财务助手                     │
│    Agent：仓咚咚                    │
│    Token：xbot_abc123...            │
│    状态：✅ 已接入微信               │
│    今日：23 次对话                  │
│                                     │
│ 2️⃣ 工作助手                        │
│    Agent：事咚咚                    │
│    Token：xbot_def456...            │
│    状态：⏳ 未接入                   │
│                                     │
│ ━━━━━━━━━━━━━━━━━━━━━━━━           │
│ 💡 回复数字选择 Bot                 │
│ 💡 /newbot 创建新 Bot               │
└─────────────────────────────────────┘

选择后：
┌─────────────────────────────────────┐
│ 你：1                               │
│                                     │
│ 🤖 XBot Admin：                     │
│ ✅ 已选择：我的财务助手             │
│                                     │
│ 可用操作：                          │
│ /token - 查看 Token                 │
│ /stats - 查看统计                   │
│ /setname - 修改名称                 │
│ /revoke - 重置 Token                │
│ /delete - 删除 Bot                  │
│                                     │
│ 💡 /cancel 返回                     │
└─────────────────────────────────────┘
```

### 2.3 交互细节

#### 消息类型

| 类型 | 说明 |
|------|------|
| **文本消息** | 用户输入，Bot 回复 |
| **命令消息** | 以 `/` 开头 |
| **卡片消息** | Bot 信息、Token 展示 |
| **图片消息** | 小程序码 |

#### 命令输入

```
输入框行为：
1. 输入 / → 显示命令补全
2. 选择命令 → 自动填入
3. 回车/点击发送 → 发送命令
```

#### 命令补全

```
┌─────────────────────────────────────┐
│ [/newb                 ]   [发送]  │
├─────────────────────────────────────┤
│ /newbot ← 创建新 Bot                │
└─────────────────────────────────────┘
```

---

## 3. 小程序设计

### 3.1 信息架构

```
小程序
├── 对话页（主页面）
│   ├── 顶部：Bot 信息
│   ├── 中间：消息列表
│   └── 底部：输入框
│
├── 绑定页（首次进入）
│   ├── Token 输入
│   └── Bot 信息确认
│
└── 错误页
    ├── Token 无效
    └── Bot 已删除
```

### 3.2 对话页设计

```
┌─────────────────────────────────────┐
│ 状态栏                              │
├─────────────────────────────────────┤
│ ←  我的财务助手 🤖                  │
│     仓咚咚                          │
├─────────────────────────────────────┤
│                                     │
│  [用户头像] 今天花了50元吃饭        │
│                                     │
│         [Bot头像]                   │
│         收到！吱~                   │
│         已记入餐饮支出              │
│         今日累计：50元              │
│                                     │
│  [用户头像] 这周花了多少？          │
│                                     │
│         [Bot头像]                   │
│         让我看看...吱！             │
│         本周共支出 520 元           │
│         比上周多 15%                │
│                                     │
├─────────────────────────────────────┤
│ [输入消息]                 [发送]  │
└─────────────────────────────────────┘
```

### 3.3 绑定页设计

```
场景：扫码进入，URL 带 Token

自动绑定流程：
┌─────────────────────────────────────┐
│                                     │
│         ⏳ 正在连接...              │
│                                     │
└─────────────────────────────────────┘

成功后直接跳转对话页
```

```
场景：手动输入 Token

┌─────────────────────────────────────┐
│                                     │
│         连接 Bot                    │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ 输入 Token                  │   │
│  │ xbot_abc123...              │   │
│  └─────────────────────────────┘   │
│                                     │
│         [连接 Bot]                  │
│                                     │
│  💡 Token 从 XBot App 获取          │
│                                     │
└─────────────────────────────────────┘
```

### 3.4 错误页设计

```
Token 无效：
┌─────────────────────────────────────┐
│                                     │
│            ❌                       │
│                                     │
│      Bot Token 无效                 │
│                                     │
│  可能原因：                         │
│  • Token 输入错误                   │
│  • Token 已被重置                   │
│  • Bot 已被删除                     │
│                                     │
│      [重新输入 Token]               │
│                                     │
└─────────────────────────────────────┘
```

---

## 4. 数据模型

### 4.1 用户（User）

```typescript
interface User {
  id: string;              // 用户 ID
  phone?: string;          // 手机号
  wechat_openid?: string;  // 微信 OpenID
  nickname?: string;       // 昵称
  avatar?: string;         // 头像
  created_at: Date;        // 创建时间
  updated_at: Date;        // 更新时间
}
```

### 4.2 Bot

```typescript
interface Bot {
  id: string;              // Bot ID
  user_id: string;         // 所有者 ID
  name: string;            // Bot 名称
  token: string;           // Bot Token
  agent_type: string;      // Agent 类型（openclaw/chatgpt/custom）
  agent_id?: string;       // Agent ID（如果选 OpenClaw）
  api_key?: string;        // API Key（如果选 ChatGPT/自定义）
  api_url?: string;        // API URL（如果自定义）
  status: 'active' | 'disabled';  // 状态
  created_at: Date;        // 创建时间
  updated_at: Date;        // 更新时间
}
```

### 4.3 对话（Conversation）

```typescript
interface Conversation {
  id: string;              // 对话 ID
  bot_id: string;          // Bot ID
  channel: string;         // 渠道（wechat_miniprogram）
  channel_user_id: string; // 渠道用户 ID
  created_at: Date;        // 创建时间
  updated_at: Date;        // 更新时间
}
```

### 4.4 消息（Message）

```typescript
interface Message {
  id: string;              // 消息 ID
  conversation_id: string; // 对话 ID
  role: 'user' | 'assistant';  // 角色
  content: string;         // 内容
  created_at: Date;        // 创建时间
}
```

### 4.5 统计（Stats）

```typescript
interface BotStats {
  bot_id: string;          // Bot ID
  date: Date;              // 日期
  message_count: number;   // 消息数
  user_count: number;      // 活跃用户数
  token_used?: number;     // Token 消耗
}
```

---

## 5. 功能清单

### 5.1 MVP 功能（P0）

#### App 端

| 功能 | 说明 | 状态 |
|------|------|------|
| 命令创建 Bot | /newbot | ✅ |
| Bot 列表 | /mybots | ✅ |
| 查看 Token | /token | ✅ |
| Bot 统计 | /stats | ✅ |
| 删除 Bot | /delete | ✅ |
| 帮助 | /help | ✅ |

#### 后端

| 功能 | 说明 | 状态 |
|------|------|------|
| 用户注册/登录 | 手机号/微信 | ✅ |
| Bot CRUD | 创建/查询/更新/删除 | ✅ |
| Token 生成 | 随机生成 32 位 | ✅ |
| Agent 集成 | OpenClaw API | ✅ |
| 消息转发 | 用户→Agent→用户 | ✅ |

#### 小程序

| 功能 | 说明 | 状态 |
|------|------|------|
| Token 绑定 | 扫码/手动 | ✅ |
| 对话界面 | 消息列表 + 输入 | ✅ |
| 消息发送/接收 | 实时对话 | ✅ |

### 5.2 扩展功能（P1）

| 功能 | 说明 | 优先级 |
|------|------|--------|
| 修改名称 | /setname | P1 |
| 修改 Agent | /setagent | P1 |
| 重置 Token | /revoke | P1 |
| 企业微信接入 | 新渠道 | P1 |
| 飞书接入 | 新渠道 | P1 |

### 5.3 未来功能（P2）

| 功能 | 说明 | 优先级 |
|------|------|--------|
| Webhook 配置 | /setwebhook | P2 |
| 自定义提示词 | /setprompt | P2 |
| 群聊支持 | 多人对话 | P2 |
| Bot 分享 | /share | P2 |
| API 开放 | 开发者 API | P2 |

---

## 6. Agent 集成

### 6.1 OpenClaw Agent（MVP）

#### 预置 Agent 列表

| ID | 名称 | 说明 |
|----|------|------|
| cang | 仓咚咚 | 财务管理 |
| yue | 阅咚咚 | 阅读管理 |
| think | 思咚咚 | 灵感管理 |
| todo | 事咚咚 | 待办管理 |

#### 集成方式

```typescript
// 调用 OpenClaw Agent API
const response = await fetch('https://api.openclaw.ai/agent/chat', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${OPENCLAW_API_KEY}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    agent_id: bot.agent_id,
    message: userMessage,
    conversation_id: conversationId,
  }),
});
```

### 6.2 ChatGPT（未来）

```typescript
// 用户配置 API Key
interface ChatGPTConfig {
  api_key: string;  // 用户的 API Key
  model: string;    // gpt-4, gpt-3.5-turbo
}
```

### 6.3 自定义 Agent（未来）

```typescript
// 用户自定义 API
interface CustomAgentConfig {
  api_url: string;   // API 地址
  api_key?: string;  // API Key
}
```

---

## 7. 接口设计（简要）

### 7.1 用户接口

```
POST /api/auth/register     # 注册
POST /api/auth/login        # 登录
GET  /api/user/profile      # 获取用户信息
```

### 7.2 Bot 接口

```
POST /api/bots              # 创建 Bot
GET  /api/bots              # Bot 列表
GET  /api/bots/:id          # Bot 详情
PUT  /api/bots/:id          # 更新 Bot
DELETE /api/bots/:id        # 删除 Bot
POST /api/bots/:id/revoke   # 重置 Token
```

### 7.3 对话接口

```
POST /api/chat              # 发送消息
GET  /api/chat/history      # 历史消息
```

### 7.4 小程序接口

```
POST /api/mp/bind           # 绑定 Bot（通过 Token）
GET  /api/mp/bot/info       # Bot 信息
POST /api/mp/chat           # 发送消息
GET  /api/mp/chat/history   # 历史消息
```

---

## 8. 技术要求

### 8.1 性能要求

| 指标 | 要求 |
|------|------|
| Bot 创建 | < 500ms |
| Token 生成 | < 100ms |
| 消息响应 | < 3s（含 Agent 响应）|
| 小程序加载 | < 2s |

### 8.2 安全要求

| 项目 | 要求 |
|------|------|
| Token 长度 | 32 位随机字符串 |
| Token 存储 | 加密存储 |
| 传输加密 | HTTPS |
| API 认证 | JWT Token |

### 8.3 可用性要求

| 指标 | 要求 |
|------|------|
| 可用性 | > 99.5% |
| 故障恢复 | < 5min |

---

## 9. 验收标准

### 9.1 MVP 验收

- [ ] App 可以注册/登录
- [ ] App 可以创建 Bot
- [ ] App 可以查看 Bot 列表
- [ ] App 可以查看 Token
- [ ] 小程序可以绑定 Bot
- [ ] 小程序可以和 Bot 对话
- [ ] 对话可以正确响应

### 9.2 功能验收

```
测试流程：
1. 用户注册 → ✅ 成功
2. 创建 Bot → ✅ Token 生成
3. 扫码接入 → ✅ 小程序绑定
4. 发送消息 → ✅ Bot 响应
5. 多轮对话 → ✅ 上下文正确
6. 查看统计 → ✅ 数据正确
```

---

## 10. 总结

### 核心设计

| 设计点 | 决策 |
|--------|------|
| **交互风格** | Telegram 命令式 |
| **创建方式** | 对话式创建 |
| **Token** | 立即生成，扫码即用 |
| **渠道** | 微信小程序优先 |

### MVP 范围

- App：命令创建 + 管理
- 小程序：扫码绑定 + 对话
- 后端：Bot 管理 + Agent 集成

### 下一步

- [ ] 技术选型文档
- [ ] 架构设计文档
- [ ] API 详细设计
- [ ] 数据库设计

---

**最后更新：** 2026-03-17
