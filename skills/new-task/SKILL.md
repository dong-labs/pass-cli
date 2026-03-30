# 创建新任务并启动开发

根据用户输入的任务描述，自动创建 issue 文件并切换到对应分支。

> **工作流规范**：详见 [docs/branch-model.md](docs/branch-model.md)

## 执行流程

1. **检查当前分支**：
   - 如果不在 `develop` 分支，先切换到 `develop`
   - 确保本地 `develop` 与远程同步

2. **询问类型**：fix / feat / refactor / chore / docs / perf / style

3. **询问描述**：用户用中文描述任务

4. **自动处理**：
   - 翻译描述成英文分支名（kebab-case）
   - 扫描 `issues/` 目录获取下一个编号
   - 创建 issue 文件到 `issues/当前版本/`
   - **从 develop 创建并切换到对应分支**

5. **输出提醒**：后续步骤清单

## 分支命名规则

| 类型 | 前缀 | 示例 |
|------|------|------|
| fix | `fix/` | `fix/login-crash` |
| feat | `feat/` | `feat/dark-mode` |
| refactor | `refactor/` | `refactor/simplify-sync` |
| chore | `chore/` | `chore/update-copy` |
| docs | `docs/` | `docs/api-guide` |
| perf | `perf/` | `perf/reduce-memory` |
| style | `style/` | `style/code-format` |

## 编号规则

- 扫描 `issues/` 下所有 `*-###-*.md` 文件
- 取最大编号 +1 作为新编号
- 格式：`{类型}-{编号:03d}-{描述}`

## Issue 模板

```markdown
# {类型}-{编号:03d}-{英文描述}

> **类型**: {类型}
> **优先级**: P2
> **状态**: Todo
> **创建时间**: {日期}
> **目标版本**: {当前版本}

---

## 任务描述

{用户输入的中文描述}

---

## ✅ 完成清单

- [ ] 完成任务
- [ ] 本地验证
- [ ] 更新 issue 状态为 Done
- [ ] 提交 PR 到 develop
```

## 分支名转换规则

- 中文 → 英文翻译
- 空格 → 连字符
- 全小写
- 移除特殊字符

示例：
- `修复登录崩溃` → `fix/login-crash`
- `添加暗黑模式` → `feat/dark-mode`
- `优化同步逻辑` → `refactor/sync-optimization`
- `更新文案` → `chore/update-copy`

## 后续步骤提醒

```
✅ 已创建 issue: issues/230/fix-001-login-crash.md
✅ 已从 develop 创建分支: fix/login-crash

📝 后续步骤:
1. 进行开发/修复
2. 本地验证
3. 更新 issue 状态为 Done
4. 提交代码: git add . && git commit -m "fix: resolve login crash"
5. 推送分支: git push -u origin fix/login-crash
6. 创建 PR: gh pr create --title "fix: resolve login crash" --body "修复登录崩溃问题"
   (PR 目标: develop)
7. CI 通过后合并 PR
8. 删除本地分支: git branch -d fix/login-crash
```

## 获取当前版本

从 `app/build.gradle` 读取 `versionName`，格式如 `2.3.0` → 目录 `230`

---

## ⚠️ 分支模型要点

```
main ←── develop ←── feat/xxx / fix/xxx
(生产)   (开发集成分支)     (临时分支)
```

**核心规则**：
- 所有临时分支（feat/、fix/等）**必须从 develop 创建**
- 完成后 PR **合并回 develop**
- 发版时 develop 合并到 main 并打 tag
- **禁止**直接从 main 创建功能分支（hotfix/ 除外）
