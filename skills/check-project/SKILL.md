---
name: check-project
description: 检查项目状态。在任何 Issue 操作前调用，确保项目状态正常。当用户说"检查项目"、"check-project"、"项目状态"时触发。
---

# 检查项目状态

在任何 Issue 相关操作前调用此技能，确保项目状态正常。

---

## 执行流程

### 1. 根据 Issue 标签确定仓库

| Issue 标签 | 仓库 | 路径 |
|------------|------|------|
| `inBox App` / `app` | ThinkPlus | `repos/ThinkPlus/` |
| `inBox PC版` / `pc` | thinkflutter | `repos/thinkflutter/` |

### 2. 检查项目状态

```bash
# 进入项目目录
cd ~/.openclaw/workspace-coder/repos/<repo_name>

# 检查 Git 状态
git status

# 检查当前分支
git branch --show-current

# 检查是否有未推送的提交
git log origin/develop..HEAD --oneline

# 检查 develop 分支是否最新
git fetch origin
git log HEAD..origin/develop --oneline
```

### 3. 检查结果

| 检查项 | 正常 | 异常处理 |
|--------|------|----------|
| Git 状态 | 干净 | 报告未提交的文件 |
| 当前分支 | develop | 提示切换到 develop |
| 未推送提交 | 无 | 提示先推送或处理 |
| develop 落后 | 无 | 执行 `git pull` |

### 4. 输出格式

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 项目状态检查: ThinkPlus
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

仓库: ThinkPlus
路径: ~/.openclaw/workspace-coder/repos/ThinkPlus/

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 检查结果
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Git 状态:     ✅ 干净
当前分支:     ✅ develop
未推送提交:   ✅ 无
develop 同步: ✅ 最新

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 可以继续
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

项目状态正常，可以继续处理 Issue。
```

---

## 异常报告格式

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ 项目状态异常: ThinkPlus
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ Git 状态: 有未提交更改
   - M  app/src/main/AndroidManifest.xml
   - M  app/build.gradle

❌ 当前分支: feat/test
   应该在: develop

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 建议操作
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 处理未提交更改:
   git stash  # 暂存
   或
   git add . && git commit -m "xxx"  # 提交

2. 切换分支:
   git checkout develop
```

---

## 使用方式

在 `analyze-issue` 或其他 Issue 操作前自动调用：

```
用户: /analyze-issue 123
AI: 
  1. 先执行 /check-project 检查状态
  2. 状态正常 → 继续 analyze-issue
  3. 状态异常 → 报告异常，等待用户处理
```

---

## 集成到 analyze-issue

在 `analyze-issue` 开头添加：

```markdown
## 前置检查

1. **检查项目状态**：
   - 根据 Issue 标签确定仓库
   - 执行 /check-project
   - 状态异常则停止，等待用户处理

2. **状态正常后继续分析**：
   - 获取 Issue 信息
   - 搜索相关代码
   - 生成报告
```
