"""
账户控制器 - Account Controller
负责银行账户相关业务逻辑的处理
"""
from models.account import Account
from utils.data_manager import DataManager


class AccountController:
    """账户控制器类"""
    
    def __init__(self, user_controller):
        """
        初始化账户控制器
        :param user_controller: 用户控制器实例
        """
        self.data_manager = DataManager()
        self.user_controller = user_controller
    
    def create_account(self, initial_balance=0.0):
        """
        开户
        :param initial_balance: 初始存款
        :return: (成功标志, 消息, 卡号)
        """
        # 检查是否已登录
        if not self.user_controller.is_logged_in():
            return False, "请先登录", None
        
        # 验证初始余额
        if initial_balance < 0:
            return False, "初始余额不能为负数", None
        
        # 获取当前用户
        current_user = self.user_controller.get_current_user()
        
        # 创建账户
        account = Account(current_user.username, initial_balance)
        
        # 保存到数据库
        self.data_manager.add_account(account.to_dict())
        
        return True, f"开户成功！您的卡号是：{account.card_number}", account.card_number
    
    def get_my_accounts(self):
        """
        获取当前用户的所有账户
        :return: 账户列表
        """
        if not self.user_controller.is_logged_in():
            return []
        
        current_user = self.user_controller.get_current_user()
        accounts_data = self.data_manager.get_accounts_by_username(current_user.username)
        
        return [Account.from_dict(acc_data) for acc_data in accounts_data]
    
    def get_account_by_card(self, card_number):
        """
        根据卡号获取账户
        :return: Account对象或None
        """
        account_data = self.data_manager.get_account(card_number)
        if not account_data:
            return None
        
        # 检查账户是否属于当前用户
        if self.user_controller.is_logged_in():
            current_user = self.user_controller.get_current_user()
            if account_data['username'] == current_user.username:
                return Account.from_dict(account_data)
        
        return None
    
    def deposit(self, card_number, amount):
        """
        存款
        :return: (成功标志, 消息)
        """
        if not self.user_controller.is_logged_in():
            return False, "请先登录"
        
        # 获取账户
        account = self.get_account_by_card(card_number)
        if not account:
            return False, "账户不存在或不属于您"
        
        # 执行存款
        success, message = account.deposit(amount)
        
        # 保存更新
        if success:
            self.data_manager.update_account(card_number, account.to_dict())
        
        return success, message
    
    def withdraw(self, card_number, amount):
        """
        取款
        :return: (成功标志, 消息)
        """
        if not self.user_controller.is_logged_in():
            return False, "请先登录"
        
        # 获取账户
        account = self.get_account_by_card(card_number)
        if not account:
            return False, "账户不存在或不属于您"
        
        # 执行取款
        success, message = account.withdraw(amount)
        
        # 保存更新
        if success:
            self.data_manager.update_account(card_number, account.to_dict())
        
        return success, message
    
    def check_balance(self, card_number):
        """
        查询余额
        :return: (成功标志, 余额)
        """
        if not self.user_controller.is_logged_in():
            return False, 0
        
        # 获取账户
        account = self.get_account_by_card(card_number)
        if not account:
            return False, 0
        
        return True, account.get_balance()
    
    def freeze_account(self, card_number):
        """
        冻结账户
        :return: (成功标志, 消息)
        """
        if not self.user_controller.is_logged_in():
            return False, "请先登录"
        
        # 获取账户
        account = self.get_account_by_card(card_number)
        if not account:
            return False, "账户不存在或不属于您"
        
        # 执行冻结
        success, message = account.freeze()
        
        # 保存更新
        if success:
            self.data_manager.update_account(card_number, account.to_dict())
        
        return success, message
    
    def unfreeze_account(self, card_number):
        """
        解冻账户
        :return: (成功标志, 消息)
        """
        if not self.user_controller.is_logged_in():
            return False, "请先登录"
        
        # 获取账户
        account = self.get_account_by_card(card_number)
        if not account:
            return False, "账户不存在或不属于您"
        
        # 执行解冻
        success, message = account.unfreeze()
        
        # 保存更新
        if success:
            self.data_manager.update_account(card_number, account.to_dict())
        
        return success, message
    
    def report_loss(self, card_number):
        """
        挂失
        :return: (成功标志, 消息)
        """
        if not self.user_controller.is_logged_in():
            return False, "请先登录"
        
        # 获取账户
        account = self.get_account_by_card(card_number)
        if not account:
            return False, "账户不存在或不属于您"
        
        # 执行挂失
        success, message = account.report_loss()
        
        # 保存更新
        if success:
            self.data_manager.update_account(card_number, account.to_dict())
        
        return success, message
    
    def cancel_loss(self, card_number):
        """
        解除挂失
        :return: (成功标志, 消息)
        """
        if not self.user_controller.is_logged_in():
            return False, "请先登录"
        
        # 获取账户
        account = self.get_account_by_card(card_number)
        if not account:
            return False, "账户不存在或不属于您"
        
        # 执行解除挂失
        success, message = account.cancel_loss()
        
        # 保存更新
        if success:
            self.data_manager.update_account(card_number, account.to_dict())
        
        return success, message
    
    def close_account(self, card_number):
        """
        销户
        :return: (成功标志, 消息)
        """
        if not self.user_controller.is_logged_in():
            return False, "请先登录"
        
        # 获取账户
        account = self.get_account_by_card(card_number)
        if not account:
            return False, "账户不存在或不属于您"
        
        # 执行销户
        success, message = account.close_account()
        
        # 保存更新（标记为已关闭）
        if success:
            self.data_manager.update_account(card_number, account.to_dict())
        
        return success, message
    
    def get_transaction_history(self, card_number):
        """
        获取交易历史
        :return: (成功标志, 交易记录列表)
        """
        if not self.user_controller.is_logged_in():
            return False, []
        
        # 获取账户
        account = self.get_account_by_card(card_number)
        if not account:
            return False, []
        
        return True, account.get_transaction_history()

