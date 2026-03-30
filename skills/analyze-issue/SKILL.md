# 分析 GitHub Issue

根据 GitHub Issue URL，分析问题类型、搜索相关代码，**只做分析，不做自动创建任务**。

## 前置检查（必须）

1. **检查项目状态**：
   - 根据 Issue 标签确定仓库（inBox App → ThinkPlus, inBox PC版 → thinkflutter）
   - 执行 `cd repos/<repo_name> && git status && git branch`
   - 状态异常（未提交更改、不在 develop 分支）则停止，报告异常

2. **状态正常后继续分析**

---

## 执行流程

1. **获取 Issue 信息**：
   - 从 GitHub API 读取 Issue 标题、内容、标签
   - 提取关键信息（类型、优先级、模块）

2. **分析问题类型**：
   - 根据标题/内容/标签推断：fix / feat / refactor / chore / docs / perf / style
   - 标签 `bug` → `fix`
   - 标签 `enhancement` / `feature` → `feat`
   - 标签 `documentation` → `docs`

3. **搜索相关代码**：
   - 根据关键词搜索项目中的相关文件
   - 定位可能需要修改的代码位置

4. **生成分析报告**：
   - 展示分析结果
   - 列出相关文件
   - 给出建议

5. **【停止，等待确认】**：
   - 报告给咕咚
   - 等待咕咚决定：
     - 纳入哪个版本？
     - 要不要创建任务？
     - 优先级是否调整？

## 标签 → 仓库映射

| Issue 标签 | 仓库 | 路径 |
|------------|------|------|
| `inBox App` / `app` | ThinkPlus | `repos/ThinkPlus/` |
| `inBox PC版` / `pc` | thinkflutter | `repos/thinkflutter/` |

---

## 使用方式

```
/analyze-issue https://github.com/maoruibin/ThinkPlus/issues/123
```

或简化：

```
/analyze-issue 123
```

## 核心原则

**只分析，不执行**：
- ✅ 分析 Issue
- ✅ 搜索代码
- ✅ 生成报告
- ❌ 不自动创建分支
- ❌ 不自动创建任务文件

**必须等咕咚确认后，才能继续下一步。**

## AI 分析能力

**自由分析，参考以下角度**：

| 角度 | 思考点 |
|------|--------|
| **问题本质** | 是 bug 还是需求？表面现象 vs 根本原因？ |
| **影响范围** | 哪些模块/功能会受影响？ |
| **代码定位** | 需要修改哪些文件？已有相关代码吗？ |
| **技术方案** | 有哪些实现方式？优劣如何？ |
| **风险评估** | 可能引入什么问题？依赖关系？ |
| **工作量** | 复杂度如何？预估工时？ |
| **优先级** | 紧急程度？影响用户范围？ |

**分析时可以**：
- 搜索代码库找到相关文件
- 查看历史类似修改
- 理解项目架构和设计模式
- 考虑边界情况和异常处理

**输出时应该**：
- 给出明确的类型建议 (fix/feat/refactor/chore/docs/perf/style)
- 列出相关文件和具体位置
- 说明理由和依据
- 提供可行的建议

## 输出格式

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Issue #123 分析报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

标题: 添加图片文件夹功能
标签: enhancement, good first issue

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 AI 分析
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

类型: feat (新功能)
模块: Media / Gallery
分支: feat/media-folder

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📁 相关文件
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ app/src/main/java/name/gudong/think/medialibrary/MediaLibraryActivity.kt
  - 已存在媒体库功能，可在此扩展

✓ app/src/main/res/layout/fragment_home.xml
  - 可能需要添加入口按钮

✓ app/src/main/java/name/gudong/think/main/home/HomeFragment.kt
  - 首页，可能需要添加导航

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 建议
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• 基于现有 MediaLibraryActivity 扩展，不需要从零开始
• 预估工时: 2-3 天
• 优先级: P2 (正常)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

是否确认创建任务？

[1] 确认 - 创建 feat/media-folder
[2] 修改 - 调整类型或描述
[3] 取消
```

## 仓库配置

**根据 Issue 标签自动判断**：

| 标签 | 仓库 | 路径 |
|------|------|------|
| `inBox App` / `app` | ThinkPlus | `repos/ThinkPlus/` |
| `inBox PC版` / `pc` | thinkflutter | `repos/thinkflutter/` |

## 工作流集成

```
小黑牛心跳 → 发现新 Issue → 派发给小码牛
                              ↓
                     /analyze-issue <url>
                              ↓
                     1. 检查项目状态 ← 必须先做！
                        - Git 干净？
                        - 在 develop 分支？
                        - develop 最新？
                              ↓
                     2. 状态异常 → 报告，等待用户处理
                     3. 状态正常 → 继续分析 Issue
                              ↓
                     生成分析报告
                              ↓
                     【等待咕咚确认】
                              ↓
                     确认后 → /new-task
```

## 错误处理

- Issue 不存在 → 提示检查 URL
- API 限流 → 稍后重试
- 无法确定类型 → 询问用户
