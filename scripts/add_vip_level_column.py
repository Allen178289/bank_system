"""
添加vip_level字段到users表
"""
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.database_manager import DatabaseManager
from config.database_config import DB_CONFIG, POOL_CONFIG


def add_vip_level_column():
    """为users表添加vip_level列"""
    config = {**DB_CONFIG, **POOL_CONFIG}
    db = DatabaseManager(config)
    
    try:
        # 检查vip_level列是否存在
        check_query = """
        SELECT COUNT(*) as count
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = %s
        AND TABLE_NAME = 'users'
        AND COLUMN_NAME = 'vip_level'
        """
        result = db.execute_query(check_query, (DB_CONFIG['database'],))
        
        if result and result.get('count', 0) == 0:
            # 添加vip_level列
            alter_query = """
            ALTER TABLE users 
            ADD COLUMN vip_level INT DEFAULT 0 COMMENT 'VIP等级(0-5)'
            """
            db.execute_query(alter_query)
            print("[OK] vip_level字段添加成功")
            
            # 为已有的VIP用户设置默认等级
            update_query = """
            UPDATE users 
            SET vip_level = 1 
            WHERE role = 'vip' AND vip_level = 0
            """
            db.execute_query(update_query)
            print("[OK] 已为现有VIP用户设置默认等级")
        else:
            print("[INFO] vip_level字段已存在，无需添加")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] 添加vip_level字段失败：{str(e)}")
        return False


if __name__ == "__main__":
    print("="*80)
    print("                    添加VIP等级字段到数据库")
    print("="*80)
    print()
    
    if add_vip_level_column():
        print("\n[OK] 数据库更新完成！现在可以正常使用VIP功能了。")
    else:
        print("\n[ERROR] 数据库更新失败，请检查错误信息。")

