"""
主视图 - Main View
负责主菜单和用户交互界面
"""
import os


class MainView:
    """主视图类"""
    
    @staticmethod
    def clear_screen():
        """清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def print_header(title):
        """打印标题"""
        print("\n" + "=" * 60)
        print(f"{title:^60}")
        print("=" * 60)
    
    @staticmethod
    def print_divider():
        """打印分隔线"""
        print("-" * 60)
    
    @staticmethod
    def show_welcome():
        """显示欢迎界面"""
        MainView.clear_screen()
        MainView.print_header("欢迎使用银行卡管理系统 v1.0")
        print()
    
    @staticmethod
    def show_main_menu():
        """显示主菜单（未登录）"""
        MainView.print_divider()
        print("【主菜单】")
        print("1. 用户注册")
        print("2. 用户登录")
        print("0. 退出系统")
        MainView.print_divider()
    
    @staticmethod
    def show_user_menu(username):
        """显示用户菜单（已登录）"""
        MainView.print_divider()
        print(f"【用户：{username}】")
        print("1. 用户管理")
        print("2. 存取款管理")
        print("3. 账户管理")
        print("9. 退出登录")
        print("0. 退出系统")
        MainView.print_divider()
    
    @staticmethod
    def show_user_management_menu():
        """显示用户管理菜单"""
        MainView.print_divider()
        print("【用户管理】")
        print("1. 查看个人信息")
        print("2. 修改个人信息")
        print("3. 修改密码")
        print("0. 返回上级")
        MainView.print_divider()
    
    @staticmethod
    def show_transaction_menu():
        """显示存取款管理菜单"""
        MainView.print_divider()
        print("【存取款管理】")
        print("1. 开户")
        print("2. 存款")
        print("3. 取款")
        print("4. 查询余额")
        print("5. 查看交易记录")
        print("6. 我的所有账户")
        print("0. 返回上级")
        MainView.print_divider()
    
    @staticmethod
    def show_account_management_menu():
        """显示账户管理菜单"""
        MainView.print_divider()
        print("【账户管理】")
        print("1. 挂失")
        print("2. 解除挂失")
        print("3. 冻结账户")
        print("4. 解冻账户")
        print("5. 销户")
        print("0. 返回上级")
        MainView.print_divider()
    
    @staticmethod
    def get_input(prompt):
        """获取用户输入"""
        return input(f"{prompt}").strip()
    
    @staticmethod
    def show_message(message, message_type="info"):
        """显示消息"""
        if message_type == "success":
            print(f"\n✓ {message}")
        elif message_type == "error":
            print(f"\n✗ {message}")
        elif message_type == "warning":
            print(f"\n⚠ {message}")
        else:
            print(f"\nℹ {message}")
    
    @staticmethod
    def pause():
        """暂停，等待用户按键"""
        input("\n按回车键继续...")
    
    @staticmethod
    def confirm(prompt):
        """确认对话框"""
        choice = input(f"\n{prompt} (y/n): ").strip().lower()
        return choice == 'y' or choice == 'yes'
    
    @staticmethod
    def show_user_info(user_info):
        """显示用户信息"""
        MainView.print_divider()
        print("【个人信息】")
        for key, value in user_info.items():
            print(f"{key}: {value}")
        MainView.print_divider()
    
    @staticmethod
    def show_accounts(accounts):
        """显示账户列表"""
        if not accounts:
            MainView.show_message("您还没有开户", "warning")
            return
        
        MainView.print_divider()
        print("【我的账户】")
        print(f"{'卡号':<20} {'余额':<15} {'状态':<10} {'开户时间'}")
        MainView.print_divider()
        for acc in accounts:
            print(f"{acc.card_number:<20} {acc.balance:<15.2f} {acc.status:<10} {acc.created_at}")
        MainView.print_divider()
    
    @staticmethod
    def show_transaction_history(transactions):
        """显示交易记录"""
        if not transactions:
            MainView.show_message("暂无交易记录", "warning")
            return
        
        MainView.print_divider()
        print("【交易记录】")
        print(f"{'时间':<20} {'类型':<10} {'金额':<15} {'余额'}")
        MainView.print_divider()
        for trans in transactions:
            print(f"{trans['time']:<20} {trans['type']:<10} {trans['amount']:<15.2f} {trans['balance_after']:.2f}")
        MainView.print_divider()

