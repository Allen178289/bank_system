"""
数据迁移脚本
将JSON文件数据迁移到MySQL数据库
"""
import sys
import os
import json

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.database_manager import DatabaseManager


def load_json_data():
    """加载JSON文件数据"""
    users_file = 'data/users.json'
    accounts_file = 'data/accounts.json'
    
    users = {}
    accounts = {}
    
    if os.path.exists(users_file):
        with open(users_file, 'r', encoding='utf-8') as f:
            try:
                users = json.load(f)
            except json.JSONDecodeError:
                users = {}
    
    if os.path.exists(accounts_file):
        with open(accounts_file, 'r', encoding='utf-8') as f:
            try:
                accounts = json.load(f)
            except json.JSONDecodeError:
                accounts = {}
    
    return users, accounts


def migrate_data():
    """迁移数据"""
    print("开始数据迁移...")
    print()
    
    # 加载JSON数据
    print("1. 读取JSON文件...")
    users, accounts = load_json_data()
    print(f"   找到 {len(users)} 个用户")
    print(f"   找到 {len(accounts)} 个账户")
    print()
    
    if not users and not accounts:
        print("⚠️ 没有找到需要迁移的数据。")
        return False
    
    # 初始化数据库管理器
    print("2. 连接数据库...")
    try:
        db = DatabaseManager()
        print("   ✓ 数据库连接成功")
    except Exception as e:
        print(f"   ✗ 数据库连接失败: {e}")
        return False
    print()
    
    # 迁移用户数据
    print("3. 迁移用户数据...")
    success_users = 0
    failed_users = 0
    
    for username, user_data in users.items():
        try:
            # 检查用户是否已存在
            if db.user_exists(username):
                print(f"   ⊙ 用户 {username} 已存在，跳过")
                continue
            
            db.add_user(user_data)
            success_users += 1
            print(f"   ✓ 用户 {username} 迁移成功")
        except Exception as e:
            failed_users += 1
            print(f"   ✗ 用户 {username} 迁移失败: {e}")
    
    print(f"   用户迁移完成: 成功 {success_users}, 失败 {failed_users}")
    print()
    
    # 迁移账户数据
    print("4. 迁移账户数据...")
    success_accounts = 0
    failed_accounts = 0
    
    for card_number, account_data in accounts.items():
        try:
            # 检查账户是否已存在
            if db.get_account(card_number):
                print(f"   ⊙ 账户 {card_number} 已存在，跳过")
                continue
            
            db.add_account(account_data)
            success_accounts += 1
            print(f"   ✓ 账户 {card_number} 迁移成功")
        except Exception as e:
            failed_accounts += 1
            print(f"   ✗ 账户 {card_number} 迁移失败: {e}")
    
    print(f"   账户迁移完成: 成功 {success_accounts}, 失败 {failed_accounts}")
    print()
    
    # 总结
    print("=" * 60)
    if failed_users == 0 and failed_accounts == 0:
        print("✅ 数据迁移全部成功！")
    else:
        print("⚠️ 数据迁移完成，但有部分失败。")
    print(f"用户: {success_users} 成功, {failed_users} 失败")
    print(f"账户: {success_accounts} 成功, {failed_accounts} 失败")
    print("=" * 60)
    
    return True


if __name__ == '__main__':
    print("=" * 60)
    print("银行卡管理系统 - 数据迁移工具")
    print("从JSON文件迁移到MySQL数据库")
    print("=" * 60)
    print()
    
    print("⚠️ 注意事项:")
    print("1. 请确保已经执行过数据库初始化脚本")
    print("2. 请确保config/database_config.py中的数据库配置正确")
    print("3. 如果数据库中已有相同的用户或账户，将会跳过")
    print()
    
    confirm = input("确认要开始迁移吗？(输入 yes 继续): ")
    if confirm.lower() == 'yes':
        migrate_data()
    else:
        print("已取消操作。")

