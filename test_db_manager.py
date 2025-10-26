"""
测试 DatabaseManager 初始化
"""
import sys
import traceback

print("=" * 60)
print("测试 DatabaseManager 初始化...")
print("=" * 60)

try:
    print("\n步骤 1: 导入 DatabaseManager...")
    from utils.database_manager import DatabaseManager
    print("OK - DatabaseManager 导入成功")
    
    print("\n步骤 2: 创建 DatabaseManager 实例...")
    db = DatabaseManager()
    print("OK - DatabaseManager 实例创建成功")
    
    print("\n步骤 3: 测试 user_exists 方法...")
    exists = db.user_exists('test_user')
    print(f"OK - user_exists 测试成功，结果: {exists}")
    
    print("\n" + "=" * 60)
    print("测试成功！DatabaseManager 工作正常")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ 错误: {e}")
    print("\n完整错误信息:")
    traceback.print_exc()
    print("=" * 60)

input("\n按回车键退出...")

