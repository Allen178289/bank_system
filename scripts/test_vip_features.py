"""
VIP功能测试脚本 - Test VIP Features
快速创建VIP测试账户和数据
"""
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.database_manager import DatabaseManager
from config.database_config import DATABASE_CONFIG
from models.user import User
from models.account import Account


def create_vip_test_user():
    """创建VIP测试用户"""
    db = DatabaseManager(DATABASE_CONFIG)
    
    try:
        # VIP测试用户信息
        vip_username = 'vip_test'
        
        # 检查用户是否已存在
        existing_user = db.get_user(vip_username)
        if existing_user:
            print(f"[INFO] VIP测试用户 '{vip_username}' 已存在，跳过创建")
            return vip_username
        
        # 创建VIP用户
        vip_user = User(
            username=vip_username,
            password='123456',  # 测试密码
            real_name='VIP测试用户',
            id_card='110101199001019999',
            phone='13800139999',
            email='vip@test.com',
            role='vip'
        )
        
        user_dict = vip_user.to_dict()
        user_dict['vip_level'] = 3  # VIP 3级
        
        db.add_user(user_dict)
        
        print(f"[OK] VIP测试用户创建成功")
        print(f"   用户名: {vip_username}")
        print(f"   密码: 123456")
        print(f"   VIP等级: 3")
        
        return vip_username
        
    except Exception as e:
        print(f"[ERROR] 创建VIP测试用户失败：{str(e)}")
        return None


def create_test_accounts(username, count=3):
    """为用户创建测试账户"""
    db = DatabaseManager(DATABASE_CONFIG)
    
    try:
        # 检查是否已有账户
        existing_accounts = db.get_accounts_by_username(username)
        if existing_accounts and len(existing_accounts) >= count:
            print(f"[INFO] 用户已有 {len(existing_accounts)} 个账户，跳过创建")
            return
        
        # 创建测试账户
        import random
        for i in range(count):
            card_number = ''.join([str(random.randint(0, 9)) for _ in range(16)])
            balance = random.randint(10000, 100000)
            
            account = Account(
                card_number=card_number,
                username=username,
                balance=balance,
                account_type='储蓄卡'
            )
            
            db.add_account(account.to_dict())
            
            print(f"[OK] 创建账户 {i+1}: 卡号 {card_number}, 余额 ¥{balance:,.2f}")
        
        # 为账户添加一些测试交易记录
        accounts = db.get_accounts_by_username(username)
        if accounts:
            for account in accounts[:2]:  # 为前两个账户添加交易记录
                card_number = account.get('card_number')
                add_test_transactions(db, card_number)
        
    except Exception as e:
        print(f"[ERROR] 创建测试账户失败：{str(e)}")


def add_test_transactions(db, card_number):
    """为账户添加测试交易记录"""
    try:
        from datetime import datetime, timedelta
        import random
        
        account = db.get_account(card_number)
        if not account:
            return
        
        current_balance = float(account.get('balance', 0))
        
        # 创建一些历史交易
        transaction_types = ['deposit', 'withdraw', 'deposit', 'deposit']
        
        for i in range(5):
            trans_type = random.choice(transaction_types)
            amount = random.randint(100, 5000)
            
            if trans_type == 'deposit':
                current_balance += amount
                description = f"存款 - 测试交易{i+1}"
            else:
                if current_balance >= amount:
                    current_balance -= amount
                    description = f"取款 - 测试交易{i+1}"
                else:
                    continue
            
            # 设置交易时间（过去几天）
            days_ago = random.randint(1, 30)
            trans_time = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d %H:%M:%S")
            
            query = """
            INSERT INTO transactions 
            (card_number, transaction_type, amount, balance_after, transaction_time, description)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            db.execute_query(query, (card_number, trans_type, amount, current_balance, trans_time, description))
        
        print(f"   为账户 {card_number} 添加了 5 笔测试交易")
        
    except Exception as e:
        print(f"[ERROR] 添加测试交易失败：{str(e)}")


def main():
    """主函数"""
    print("="*80)
    print("                       VIP功能测试数据生成器")
    print("="*80)
    print()
    
    print("正在创建VIP测试环境...\n")
    
    # 1. 创建VIP测试用户
    print("步骤 1: 创建VIP测试用户")
    print("-" * 80)
    vip_username = create_vip_test_user()
    
    if not vip_username:
        print("[ERROR] 创建VIP测试用户失败，退出")
        return
    
    print()
    
    # 2. 创建测试账户
    print("步骤 2: 创建测试账户")
    print("-" * 80)
    create_test_accounts(vip_username, count=3)
    
    print()
    print("="*80)
    print("VIP测试环境创建完成！")
    print("="*80)
    print()
    print("🎉 现在可以使用以下账号登录测试VIP功能：")
    print()
    print(f"   用户名: vip_test")
    print(f"   密码: 123456")
    print()
    print("VIP专属功能包括：")
    print("  👑 VIP专区按钮 - 在主界面功能菜单中")
    print("  📊 财务统计 - 查看详细的收支分析")
    print("  📄 账单导出 - 导出Excel/PDF/CSV格式账单")
    print("  ⚡ 快速转账 - 管理常用收款人")
    print("  💎 VIP特权 - 查看等级特权说明")
    print("  💰 更高限额 - 单笔转账限额¥50,000")
    print()


if __name__ == "__main__":
    main()

