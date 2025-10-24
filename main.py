"""
银行卡管理系统主程序
版本: 1.0
架构: MVC (Model-View-Controller)
"""
from controllers.user_controller import UserController
from controllers.account_controller import AccountController
from views.main_view import MainView


class BankSystem:
    """银行卡管理系统主类"""
    
    def __init__(self):
        """初始化系统"""
        self.user_controller = UserController()
        self.account_controller = AccountController(self.user_controller)
        self.view = MainView()
        self.running = True
    
    def run(self):
        """运行系统"""
        self.view.show_welcome()
        
        while self.running:
            if not self.user_controller.is_logged_in():
                self.show_main_menu()
            else:
                self.show_user_menu()
    
    def show_main_menu(self):
        """显示主菜单（未登录状态）"""
        self.view.show_main_menu()
        choice = self.view.get_input("请选择操作: ")
        
        if choice == '1':
            self.register()
        elif choice == '2':
            self.login()
        elif choice == '0':
            self.exit_system()
        else:
            self.view.show_message("无效的选择，请重新输入", "error")
            self.view.pause()
    
    def show_user_menu(self):
        """显示用户菜单（已登录状态）"""
        current_user = self.user_controller.get_current_user()
        self.view.show_user_menu(current_user.username)
        choice = self.view.get_input("请选择操作: ")
        
        if choice == '1':
            self.user_management()
        elif choice == '2':
            self.transaction_management()
        elif choice == '3':
            self.account_management()
        elif choice == '9':
            self.logout()
        elif choice == '0':
            self.exit_system()
        else:
            self.view.show_message("无效的选择，请重新输入", "error")
            self.view.pause()
    
    def register(self):
        """用户注册"""
        self.view.print_header("用户注册")
        
        username = self.view.get_input("请输入用户名 (至少3个字符): ")
        password = self.view.get_input("请输入密码 (至少6个字符): ")
        confirm_pwd = self.view.get_input("请确认密码: ")
        
        if password != confirm_pwd:
            self.view.show_message("两次密码输入不一致", "error")
            self.view.pause()
            return
        
        real_name = self.view.get_input("请输入真实姓名: ")
        id_card = self.view.get_input("请输入身份证号 (18位): ")
        phone = self.view.get_input("请输入手机号 (11位): ")
        email = self.view.get_input("请输入邮箱 (可选): ")
        
        success, message = self.user_controller.register(
            username, password, real_name, id_card, phone, email
        )
        
        if success:
            self.view.show_message(message, "success")
        else:
            self.view.show_message(message, "error")
        
        self.view.pause()
    
    def login(self):
        """用户登录"""
        self.view.print_header("用户登录")
        
        username = self.view.get_input("请输入用户名: ")
        password = self.view.get_input("请输入密码: ")
        
        success, message = self.user_controller.login(username, password)
        
        if success:
            self.view.show_message(message, "success")
        else:
            self.view.show_message(message, "error")
        
        self.view.pause()
    
    def logout(self):
        """用户登出"""
        if self.view.confirm("确定要退出登录吗？"):
            success, message = self.user_controller.logout()
            self.view.show_message(message, "success" if success else "error")
            self.view.pause()
    
    def user_management(self):
        """用户管理"""
        while True:
            self.view.show_user_management_menu()
            choice = self.view.get_input("请选择操作: ")
            
            if choice == '1':
                self.view_user_info()
            elif choice == '2':
                self.update_user_info()
            elif choice == '3':
                self.change_password()
            elif choice == '0':
                break
            else:
                self.view.show_message("无效的选择，请重新输入", "error")
                self.view.pause()
    
    def view_user_info(self):
        """查看用户信息"""
        self.view.print_header("个人信息")
        user_info = self.user_controller.get_user_info()
        if user_info:
            self.view.show_user_info(user_info)
        self.view.pause()
    
    def update_user_info(self):
        """更新用户信息"""
        self.view.print_header("修改个人信息")
        
        phone = self.view.get_input("请输入新手机号 (直接回车跳过): ")
        email = self.view.get_input("请输入新邮箱 (直接回车跳过): ")
        
        if not phone and not email:
            self.view.show_message("没有任何修改", "warning")
            self.view.pause()
            return
        
        success, message = self.user_controller.update_user_info(
            phone if phone else None,
            email if email else None
        )
        
        if success:
            self.view.show_message(message, "success")
        else:
            self.view.show_message(message, "error")
        
        self.view.pause()
    
    def change_password(self):
        """修改密码"""
        self.view.print_header("修改密码")
        
        old_password = self.view.get_input("请输入旧密码: ")
        new_password = self.view.get_input("请输入新密码: ")
        confirm_pwd = self.view.get_input("请确认新密码: ")
        
        if new_password != confirm_pwd:
            self.view.show_message("两次密码输入不一致", "error")
            self.view.pause()
            return
        
        success, message = self.user_controller.change_password(old_password, new_password)
        
        if success:
            self.view.show_message(message, "success")
        else:
            self.view.show_message(message, "error")
        
        self.view.pause()
    
    def transaction_management(self):
        """存取款管理"""
        while True:
            self.view.show_transaction_menu()
            choice = self.view.get_input("请选择操作: ")
            
            if choice == '1':
                self.create_account()
            elif choice == '2':
                self.deposit()
            elif choice == '3':
                self.withdraw()
            elif choice == '4':
                self.check_balance()
            elif choice == '5':
                self.view_transaction_history()
            elif choice == '6':
                self.view_my_accounts()
            elif choice == '0':
                break
            else:
                self.view.show_message("无效的选择，请重新输入", "error")
                self.view.pause()
    
    def create_account(self):
        """开户"""
        self.view.print_header("开户")
        
        initial_balance_str = self.view.get_input("请输入初始存款金额 (默认0): ")
        
        try:
            initial_balance = float(initial_balance_str) if initial_balance_str else 0.0
        except ValueError:
            self.view.show_message("金额格式错误", "error")
            self.view.pause()
            return
        
        success, message, card_number = self.account_controller.create_account(initial_balance)
        
        if success:
            self.view.show_message(message, "success")
        else:
            self.view.show_message(message, "error")
        
        self.view.pause()
    
    def deposit(self):
        """存款"""
        self.view.print_header("存款")
        
        # 先显示账户列表
        accounts = self.account_controller.get_my_accounts()
        self.view.show_accounts(accounts)
        
        if not accounts:
            self.view.pause()
            return
        
        card_number = self.view.get_input("请输入卡号: ")
        amount_str = self.view.get_input("请输入存款金额: ")
        
        try:
            amount = float(amount_str)
        except ValueError:
            self.view.show_message("金额格式错误", "error")
            self.view.pause()
            return
        
        success, message = self.account_controller.deposit(card_number, amount)
        
        if success:
            self.view.show_message(message, "success")
        else:
            self.view.show_message(message, "error")
        
        self.view.pause()
    
    def withdraw(self):
        """取款"""
        self.view.print_header("取款")
        
        # 先显示账户列表
        accounts = self.account_controller.get_my_accounts()
        self.view.show_accounts(accounts)
        
        if not accounts:
            self.view.pause()
            return
        
        card_number = self.view.get_input("请输入卡号: ")
        amount_str = self.view.get_input("请输入取款金额: ")
        
        try:
            amount = float(amount_str)
        except ValueError:
            self.view.show_message("金额格式错误", "error")
            self.view.pause()
            return
        
        success, message = self.account_controller.withdraw(card_number, amount)
        
        if success:
            self.view.show_message(message, "success")
        else:
            self.view.show_message(message, "error")
        
        self.view.pause()
    
    def check_balance(self):
        """查询余额"""
        self.view.print_header("查询余额")
        
        # 先显示账户列表
        accounts = self.account_controller.get_my_accounts()
        self.view.show_accounts(accounts)
        
        if not accounts:
            self.view.pause()
            return
        
        card_number = self.view.get_input("请输入卡号: ")
        
        success, balance = self.account_controller.check_balance(card_number)
        
        if success:
            self.view.show_message(f"当前余额：{balance:.2f} 元", "success")
        else:
            self.view.show_message("查询失败", "error")
        
        self.view.pause()
    
    def view_transaction_history(self):
        """查看交易记录"""
        self.view.print_header("交易记录")
        
        # 先显示账户列表
        accounts = self.account_controller.get_my_accounts()
        self.view.show_accounts(accounts)
        
        if not accounts:
            self.view.pause()
            return
        
        card_number = self.view.get_input("请输入卡号: ")
        
        success, transactions = self.account_controller.get_transaction_history(card_number)
        
        if success:
            self.view.show_transaction_history(transactions)
        else:
            self.view.show_message("查询失败", "error")
        
        self.view.pause()
    
    def view_my_accounts(self):
        """查看我的所有账户"""
        self.view.print_header("我的所有账户")
        
        accounts = self.account_controller.get_my_accounts()
        self.view.show_accounts(accounts)
        
        self.view.pause()
    
    def account_management(self):
        """账户管理"""
        while True:
            self.view.show_account_management_menu()
            choice = self.view.get_input("请选择操作: ")
            
            if choice == '1':
                self.report_loss()
            elif choice == '2':
                self.cancel_loss()
            elif choice == '3':
                self.freeze_account()
            elif choice == '4':
                self.unfreeze_account()
            elif choice == '5':
                self.close_account()
            elif choice == '0':
                break
            else:
                self.view.show_message("无效的选择，请重新输入", "error")
                self.view.pause()
    
    def report_loss(self):
        """挂失"""
        self.view.print_header("挂失")
        
        # 先显示账户列表
        accounts = self.account_controller.get_my_accounts()
        self.view.show_accounts(accounts)
        
        if not accounts:
            self.view.pause()
            return
        
        card_number = self.view.get_input("请输入要挂失的卡号: ")
        
        if not self.view.confirm("确定要挂失该账户吗？"):
            self.view.show_message("操作已取消", "warning")
            self.view.pause()
            return
        
        success, message = self.account_controller.report_loss(card_number)
        
        if success:
            self.view.show_message(message, "success")
        else:
            self.view.show_message(message, "error")
        
        self.view.pause()
    
    def cancel_loss(self):
        """解除挂失"""
        self.view.print_header("解除挂失")
        
        # 先显示账户列表
        accounts = self.account_controller.get_my_accounts()
        self.view.show_accounts(accounts)
        
        if not accounts:
            self.view.pause()
            return
        
        card_number = self.view.get_input("请输入要解除挂失的卡号: ")
        
        success, message = self.account_controller.cancel_loss(card_number)
        
        if success:
            self.view.show_message(message, "success")
        else:
            self.view.show_message(message, "error")
        
        self.view.pause()
    
    def freeze_account(self):
        """冻结账户"""
        self.view.print_header("冻结账户")
        
        # 先显示账户列表
        accounts = self.account_controller.get_my_accounts()
        self.view.show_accounts(accounts)
        
        if not accounts:
            self.view.pause()
            return
        
        card_number = self.view.get_input("请输入要冻结的卡号: ")
        
        if not self.view.confirm("确定要冻结该账户吗？"):
            self.view.show_message("操作已取消", "warning")
            self.view.pause()
            return
        
        success, message = self.account_controller.freeze_account(card_number)
        
        if success:
            self.view.show_message(message, "success")
        else:
            self.view.show_message(message, "error")
        
        self.view.pause()
    
    def unfreeze_account(self):
        """解冻账户"""
        self.view.print_header("解冻账户")
        
        # 先显示账户列表
        accounts = self.account_controller.get_my_accounts()
        self.view.show_accounts(accounts)
        
        if not accounts:
            self.view.pause()
            return
        
        card_number = self.view.get_input("请输入要解冻的卡号: ")
        
        success, message = self.account_controller.unfreeze_account(card_number)
        
        if success:
            self.view.show_message(message, "success")
        else:
            self.view.show_message(message, "error")
        
        self.view.pause()
    
    def close_account(self):
        """销户"""
        self.view.print_header("销户")
        
        # 先显示账户列表
        accounts = self.account_controller.get_my_accounts()
        self.view.show_accounts(accounts)
        
        if not accounts:
            self.view.pause()
            return
        
        card_number = self.view.get_input("请输入要销户的卡号: ")
        
        if not self.view.confirm("确定要销户吗？此操作不可恢复！"):
            self.view.show_message("操作已取消", "warning")
            self.view.pause()
            return
        
        success, message = self.account_controller.close_account(card_number)
        
        if success:
            self.view.show_message(message, "success")
        else:
            self.view.show_message(message, "error")
        
        self.view.pause()
    
    def exit_system(self):
        """退出系统"""
        if self.view.confirm("确定要退出系统吗？"):
            self.view.show_message("感谢使用银行卡管理系统，再见！", "success")
            self.running = False


def main():
    """主函数"""
    system = BankSystem()
    system.run()


if __name__ == "__main__":
    main()

