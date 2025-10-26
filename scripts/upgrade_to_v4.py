"""
数据库升级脚本 - v3.0 到 v4.0
添加用户角色(role)字段
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database_config import DB_CONFIG
import mysql.connector


def upgrade_database():
    """升级数据库到v4.0"""
    print("=" * 60)
    print("数据库升级脚本 - v3.0 到 v4.0")
    print("=" * 60)
    
    try:
        # 连接数据库
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database']
        )
        cursor = conn.cursor()
        
        print("\n[OK] 成功连接到数据库")
        
        # 1. 检查role列是否已存在
        print("\n>> 检查 users 表是否已有 role 列...")
        cursor.execute("""
            SELECT COUNT(*) FROM information_schema.COLUMNS 
            WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'users' AND COLUMN_NAME = 'role'
        """, (DB_CONFIG['database'],))
        role_exists = cursor.fetchone()[0] > 0
        
        if role_exists:
            print("   [SKIP] role 列已存在，跳过添加")
        else:
            # 添加role列
            print("   >> 添加 role 列...")
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN role VARCHAR(20) NOT NULL DEFAULT 'normal' COMMENT '用户角色'
                AFTER email
            """)
            print("   [OK] 成功添加 role 列")
        
        # 2. 添加role索引（如果不存在）
        print("\n>> 检查 users 表的 role 索引...")
        cursor.execute("""
            SELECT COUNT(*) FROM information_schema.STATISTICS 
            WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'users' AND INDEX_NAME = 'idx_role'
        """, (DB_CONFIG['database'],))
        index_exists = cursor.fetchone()[0] > 0
        
        if index_exists:
            print("   [SKIP] idx_role 索引已存在，跳过添加")
        else:
            print("   >> 添加 idx_role 索引...")
            cursor.execute("CREATE INDEX idx_role ON users(role)")
            print("   [OK] 成功添加 idx_role 索引")
        
        # 3. 创建或更新默认管理员账户（如果不存在）
        print("\n>> 检查默认管理员账户...")
        cursor.execute("SELECT role FROM users WHERE username = 'admin'")
        admin_result = cursor.fetchone()
        
        if admin_result:
            if admin_result[0] != 'admin':
                print("   >> 更新 admin 用户的角色为管理员...")
                cursor.execute("UPDATE users SET role = 'admin' WHERE username = 'admin'")
                print("   [OK] 成功更新 admin 用户角色")
            else:
                print("   [SKIP] admin 用户已是管理员角色")
        else:
            print("   [WARN] admin 用户不存在，请手动创建管理员账户")
        
        # 提交更改
        conn.commit()
        
        print("\n" + "=" * 60)
        print("[SUCCESS] 数据库升级完成！")
        print("=" * 60)
        print("\n升级内容：")
        print("1. 添加 users.role 列（用户角色）")
        print("2. 添加 idx_role 索引")
        print("3. 更新/检查管理员账户")
        print("\n用户角色说明：")
        print("- normal: 普通用户（默认）")
        print("- vip: VIP用户")
        print("- admin: 管理员")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"\n[ERROR] 数据库错误: {err}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] 未知错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    upgrade_database()

