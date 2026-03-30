# MEMORY.md - 小牛牛的长期记忆

这里记录重要的技术经验，随时可查。

---

## 关于咕咚

- 微博 Android 工程师
- 独立开发者
- 产品：inBox 笔记、WeiMD、SlideNote、inBox Card
- 首选框架：Flutter
- 本地优先（Local-First）理念

---

## 🤖 GitHub Issue 自动化工作流

### 角色分工

| 智能体 | 角色 | 职责 |
|--------|------|------|
| **小黑牛** (@dongdongjun_bot) | 指挥官 | 每小时检查 GitHub Issue，分析并派发 |
| **小码牛** (coder) | 开发者 | 接收派发，处理 Issue，开发 + 提交 PR |

### 工作流程

```
用户创建 Issue
      ↓
小黑牛 (每小时心跳)
      ↓
检查新 Issue → 分析标签 → 派发给小码牛
      ↓
小码牛收到派发
      ↓
1. /analyze-issue <url>  → 分析 Issue，2. 【等待咕咚确认】
   - 纳入哪个版本？
   - 要不要创建任务？
   - 优先级是否调整？
3. 咕咚确认后 → /new-task 创建分支
4. 开发/修复代码
5. 本地验证
6. 提交 PR 到 develop
      ↓
Review → Merge → 关闭 Issue
```

**核心原则**：每一步都要人工确认，不做全自动

### 仓库映射

| Issue 标签 | 仓库 | 路径 |
|------------|------|------|
| `inBox App` / `app` | ThinkPlus | `repos/ThinkPlus/` |
| `inBox PC版` / `pc` | thinkflutter | `repos/thinkflutter/` |
| `dong-labs` / `cli` | dong-labs/* | `repos/dong-labs/xxx-cli/` |

### 标签体系

**类型标签**：`bug` / `feat` / `refactor` / `docs` / `chore` / `perf`

**平台标签**：`inBox App` / `inBox PC版` / `cli`

**优先级标签**：`P0`(紧急) / `P1`(高) / `P2`(正常) / `P3`(低)

**状态标签**：`Todo` / `In Progress` / `Done`

### 可用 Skills

| Skill | 触发词 | 用途 |
|-------|--------|------|
| `analyze-issue` | `/analyze-issue <url>` | 分析 GitHub Issue |
| `new-task` | `/new-task` | 创建任务 + 分支 |
| `start-version` | `/start-version` | 开始新版本规划 |
| `pre-release-scan` | `/pre-release-scan` | 发布前检查 |

### 处理 Issue 示例

```
小黑牛派发：
"新 Issue #12: PC端是否可以直接通过复制粘贴的方式上传图片
类型: feat
平台: inBox PC版
优先级: P2
链接: https://github.com/maoruibin/ThinkPlus/issues/12"

小码牛执行：
1. cd repos/thinkflutter  # 切换到对应仓库
2. /analyze-issue 12      # 分析 Issue

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Issue #12 分析报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
类型: feat
相关文件: [xxx.dart, yyy.dart]
建议: ...

3. 【等待咕咚确认】
   - 纳入哪个版本？
   - 要不要创建任务？
   - 优先级是否调整？

4. 咕咚确认后：
   /new-task feat clipboard-paste  # 创建分支

5. 开发代码...

6. git push && gh pr create
```

---

## 常见坑 (更新中)

<!-- 记录遇到过的问题和解决方案 -->

## 技术债务

<!-- 需要重构/优化的地方 -->

---

*让我看看代码...*
