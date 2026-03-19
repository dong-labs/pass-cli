#!/usr/bin/env python3
"""迁移脚本：为所有咚咚家族 CLI 添加 tags 字段"""

import sqlite3
import os


def migrate_db(db_path, table_name):
    """为指定数据库的表添加 tags 字段"""
    if not os.path.exists(db_path):
        print(f"⚠️  {db_path} 不存在，跳过")
        return

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # 检查是否已有 tags 列
    cur.execute(f"PRAGMA table_info({table_name})")
    columns = [row[1] for row in cur.fetchall()]

    if 'tags' in columns:
        print(f"✅ {db_path} 的 {table_name} 表已有 tags 列")
        conn.close()
        return

    # 添加 tags 列
    try:
        cur.execute(f"ALTER TABLE {table_name} ADD COLUMN tags TEXT DEFAULT ''")
        conn.commit()
        print(f"✅ {db_path} 的 {table_name} 表已添加 tags 列")

        # 创建索引
        cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_tags ON {table_name}(tags)")
        conn.commit()
        print(f"✅ {db_path} 已创建 idx_{table_name}_tags 索引")

    except Exception as e:
        print(f"❌ {db_path} 迁移失败: {e}")
    finally:
        conn.close()


def main():
    """迁移所有咚咚家族数据库"""
    databases = [
        ("~/.read/read.db", "items"),
        ("~/.dida/dida.db", "todos"),
        ("~/.log/log.db", "logs"),
        ("~/.think/think.db", "thoughts"),
    ]

    print("🔄 开始迁移...")
    for db_path, table_name in databases:
        db_path = os.path.expanduser(db_path)
        migrate_db(db_path, table_name)

    print("\n✨ 迁移完成！")


if __name__ == "__main__":
    main()
