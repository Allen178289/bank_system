"""
升级用户为VIP - Upgrade User to VIP
用于将指定用户升级为VIP用户
"""
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.database_manager import DatabaseManager
from config.database_config import DATABASE_CONFIG


def upgrade_user_to_vip(username, vip_level=1):
    """
    将用户升级为VIP
    
    :param username: 用户名
    :param vip_level: VIP等级 (1-5)
    :return: 成功返回 True，失败返回 False
    """
    db = DatabaseManager(DATABASE_CONFIG)
    
    try:
        # 检查用户是否存在
        user = db.get_user(username)
        if not user:
            print(f"[ERROR] 用户 '{username}' 不存在")
            return False
        
        # 更新用户角色为VIP
        query = """
        UPDATE users 
        SET role = 'vip', vip_level = %s
        WHERE username = %s
        """
        db.execute_query(query, ('vip', vip_level, username))
        
        print(f"[OK] 用户 '{username}' 已成功升级为 VIP {vip_level} 级")
        print(f"[INFO] 用户信息：")
        print(f"   - 用户名: {user.get('username')}")
        print(f"   - 真实姓名: {user.get('real_name')}")
        print(f"   - 角色: VIP")
        print(f"   - VIP等级: {vip_level}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] 升级用户失败：{str(e)}")
        return False


def list_all_users():
    """列出所有用户"""
    db = DatabaseManager(DATABASE_CONFIG)
    
    try:
        query = "SELECT username, real_name, role, vip_level FROM users ORDER BY created_time DESC"
        users = db.execute_query(query, fetch_all=True)
        
        if not users:
            print("[INFO] 系统中没有注册用户")
            return
        
        print("\n" + "="*80)
        print(f"{'用户名':<15} {'真实姓名':<15} {'角色':<10} {'VIP等级':<10}")
        print("="*80)
        
        for user in users:
            username = user.get('username', '')
            real_name = user.get('real_name', '')
            role = user.get('role', 'normal')
            vip_level = user.get('vip_level', 0)
            
            # 角色显示
            if role == 'admin':
                role_display = '管理员 🔧'
            elif role == 'vip':
                role_display = f'VIP 👑'
            else:
                role_display = '普通用户'
            
            # VIP等级显示
            vip_display = f"VIP {vip_level}" if role == 'vip' else '-'
            
            print(f"{username:<15} {real_name:<15} {role_display:<15} {vip_display:<10}")
        
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"[ERROR] 获取用户列表失败：{str(e)}")


def main():
    """主函数"""
    print("="*80)
    print("                   升级用户为VIP - Upgrade User to VIP")
    print("="*80)
    print()
    
    # 显示当前所有用户
    print("当前系统用户列表：")
    list_all_users()
    
    # 获取要升级的用户名
    username = input("请输入要升级为VIP的用户名（直接回车查看用户列表）: ").strip()
    
    if not username:
        list_all_users()
        return
    
    # 获取VIP等级
    try:
        vip_level_input = input("请输入VIP等级 (1-5，默认为1): ").strip()
        vip_level = int(vip_level_input) if vip_level_input else 1
        
        if vip_level < 1 or vip_level > 5:
            print("[ERROR] VIP等级必须在1-5之间")
            return
    except ValueError:
        print("[ERROR] VIP等级必须是数字")
        return
    
    # 确认升级
    confirm = input(f"\n确认将用户 '{username}' 升级为 VIP {vip_level} 级？(y/n): ").strip().lower()
    
    if confirm == 'y':
        success = upgrade_user_to_vip(username, vip_level)
        
        if success:
            print("\n[OK] 升级成功！用户现在可以登录系统体验VIP专属功能。")
            print("\nVIP专属功能包括：")
            print("  📊 财务统计 - 查看详细的收支统计和趋势分析")
            print("  📄 账单导出 - 支持导出Excel、PDF、CSV格式账单")
            print("  ⚡ 快速转账 - 收藏常用收款人，一键快速转账")
            print("  💰 更高限额 - 单笔转账限额¥50,000（普通用户仅¥10,000）")
            print("  💎 VIP特权 - 根据等级享有不同的专属功能")
    else:
        print("[INFO] 操作已取消")


if __name__ == "__main__":
    main()

