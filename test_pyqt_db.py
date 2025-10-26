"""
测试 PyQt + DatabaseManager 组合
"""
import sys
import traceback

print("=" * 60)
print("测试 PyQt + DatabaseManager 组合...")
print("=" * 60)

try:
    print("\n步骤 1: 导入 PyQt5...")
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import Qt
    print("OK - PyQt5 导入成功")
    
    print("\n步骤 2: 设置高DPI属性...")
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    print("OK - 高DPI属性设置成功")
    
    print("\n步骤 3: 创建 QApplication...")
    app = QApplication(sys.argv)
    print("OK - QApplication 创建成功")
    
    print("\n步骤 4: 导入 DatabaseManager...")
    from utils.database_manager import DatabaseManager
    print("OK - DatabaseManager 导入成功")
    
    print("\n步骤 5: 创建 DatabaseManager 实例...")
    db = DatabaseManager()
    print("OK - DatabaseManager 实例创建成功")
    
    print("\n步骤 6: 测试数据库操作...")
    exists = db.user_exists('test_user')
    print(f"OK - user_exists 测试成功，结果: {exists}")
    
    print("\n步骤 7: 导入控制器...")
    from controllers.user_controller import UserController
    from controllers.account_controller import AccountController
    print("OK - 控制器导入成功")
    
    print("\n步骤 8: 创建控制器实例...")
    user_controller = UserController()
    account_controller = AccountController(user_controller)
    print("OK - 控制器实例创建成功")
    
    print("\n" + "=" * 60)
    print("测试成功！PyQt + DatabaseManager 组合工作正常")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ 错误发生在某个步骤: {e}")
    print("\n完整错误信息:")
    traceback.print_exc()
    print("=" * 60)

input("\n按回车键退出...")

