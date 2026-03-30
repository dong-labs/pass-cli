---
name: pre-release-scan
description: Android 应用发布前代码扫描工具。检查发布前必须确认的代码问题。当用户说"发布前扫描"、"release检查"时触发。
---

# 发布前代码扫描

发布 Release 版本前，逐一检查以下项目。

---

## 检查项

### 1. isDebugMode() 返回 false

**文件**: `app/src/main/java/name/gudong/think/utils/ThinkUtils.kt` (line 533-536)

**正确**:
```kotlin
fun isDebugMode(): Boolean {
    return false
}
```

**错误**: `return BuildConfig.DEBUG`

---

### 2. 日志开关关闭

**文件**: `arch/base/src/main/java/name/gudong/base/tools/JavaUtils.java` (line 31-34)

**正确**: `return false;`

**错误**: `return true;` (日志一直输出)

---

### 3. AI 功能开启

**文件**: `app/src/main/java/name/gudong/think/utils/ThinkConfig.kt` (line 29)

**正确**:
```kotlin
val CloseAi = false
```

**错误**: `val CloseAi = true` (AI 功能关闭)

---

### 4. Release 混淆开启

**文件**: `app/build.gradle` (line 73-87)

**检查**: `minifyEnabled true` (混淆必须开启)

**其他**:
- `zipAlignEnabled true` (压缩对齐)
- `shrinkResources true` (移除无用资源)

---

## 使用方式

触发关键词: "发布前扫描"、"release检查"、"pre-release scan"

扫描完成后，逐项报告结果：✅ 通过 或 ❌ 失败
