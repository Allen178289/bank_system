"""
银行卡管理系统 - PyQt5 GUI版本
版本: 2.0
架构: MVC (Model-View-Controller) + PyQt5 GUI
"""
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from controllers.user_controller import UserController
from controllers.account_controller import AccountController
from views.login_window import LoginWindow
from views.register_window import RegisterWindow
from views.main_window import MainWindow


class BankSystemGUI:
    """银行卡管理系统GUI主类"""
    
    def __init__(self):
        """初始化系统"""
        # 创建QApplication实例
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("银行卡管理系统")
        
        # 设置全局字体
        font = QFont("Microsoft YaHei UI", 10)  # 使用微软雅黑字体
        self.app.setFont(font)
        
        # 设置高DPI支持
        self.app.setAttribute(Qt.AA_EnableHighDpiScaling)
        self.app.setAttribute(Qt.AA_UseHighDpiPixmaps)
        
        # 初始化控制器
        self.user_controller = UserController()
        self.account_controller = AccountController(self.user_controller)
        
        # 窗口实例
        self.login_window = None
        self.register_window = None
        self.main_window = None
    
    def run(self):
        """运行系统"""
        self.show_login_window()
        sys.exit(self.app.exec_())
    
    def show_login_window(self):
        """显示登录窗口"""
        self.login_window = LoginWindow(self.user_controller)
        
        # 连接信号
        self.login_window.login_success.connect(self.on_login_success)
        self.login_window.open_register.connect(self.show_register_window)
        
        self.login_window.show()
    
    def show_register_window(self):
        """显示注册窗口"""
        self.register_window = RegisterWindow(self.user_controller)
        
        # 连接信号
        self.register_window.register_success.connect(self.on_register_success)
        
        self.register_window.exec_()
    
    def on_register_success(self):
        """注册成功后的处理"""
        # 清空登录窗口的输入
        if self.login_window:
            self.login_window.clear_inputs()
    
    def on_login_success(self):
        """登录成功后的处理"""
        # 显示主窗口
        self.show_main_window()
    
    def show_main_window(self):
        """显示主窗口"""
        self.main_window = MainWindow(self.user_controller, self.account_controller)
        
        # 连接信号
        self.main_window.logout_signal.connect(self.on_logout)
        
        self.main_window.show()
    
    def on_logout(self):
        """退出登录后的处理"""
        # 重新显示登录窗口
        self.show_login_window()


def main():
    """主函数"""
    try:
        system = BankSystemGUI()
        system.run()
    except Exception as e:
        print(f"程序运行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

