"""
测试数据库连接 - Test Database Connection
用于验证 MySQL 数据库配置是否正确
"""
import mysql.connector
from config.database_config import DB_CONFIG

def test_connection():

    """测试数据库连接"""
    print("=" * 60)
    print("正在测试 MySQL 数据库连接...")
    print("=" * 60)
    print(f"\n配置信息:")
    print(f"  主机: {DB_CONFIG['host']}")
    print(f"  端口: {DB_CONFIG['port']}")
    print(f"  用户: {DB_CONFIG['user']}")
    print(f"  数据库: {DB_CONFIG['database']}")
    print(f"  密码: {'*' * len(str(DB_CONFIG['password']))}")
    
    try:
        # 尝试连接
        print("\n正在连接...")
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        
        if conn.is_connected():
            print("✅ 成功连接到 MySQL 服务器！")
            
            cursor = conn.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"✅ MySQL 版本: {version[0]}")
            
            # 检查数据库是否存在
            cursor.execute("SHOW DATABASES LIKE %s", (DB_CONFIG['database'],))
            db_exists = cursor.fetchone()
            
            if db_exists:
                print(f"✅ 数据库 '{DB_CONFIG['database']}' 已存在")
                
                # 连接到数据库
                conn.database = DB_CONFIG['database']
                
                # 检查表是否存在
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                
                if tables:
                    print(f"✅ 数据库中有 {len(tables)} 个表:")
                    for table in tables:
                        print(f"   - {table[0]}")
                else:
                    print(f"⚠️  数据库 '{DB_CONFIG['database']}' 存在，但没有表")
                    print("   请运行: python scripts/init_database.py 来创建表")
            else:
                print(f"⚠️  数据库 '{DB_CONFIG['database']}' 不存在")
                print("   请运行: python scripts/init_database.py 来创建数据库和表")
            
            cursor.close()
            conn.close()
            print("\n" + "=" * 60)
            print("✅ 数据库连接测试完成！")
            print("=" * 60)
            return True
            
    except mysql.connector.Error as e:
        print(f"\n❌ 连接失败: {e}")
        print("\n可能的原因:")
        print("  1. MySQL 服务未启动")
        print("  2. 用户名或密码错误")
        print("  3. 主机地址或端口错误")
        print("  4. 用户权限不足")
        print("\n请检查 config/database_config.py 中的配置")
        print("=" * 60)
        return False
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        print("=" * 60)
        return False

if __name__ == "__main__":
    test_connection()
    input("\n按回车键退出...")

