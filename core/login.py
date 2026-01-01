import time
from core.account_manager import save_account_to_pool

def execute_login_process(page, account, password):
    """
    执行登录流程，包含输入、点击和验证
    """
    while True:
        try:
            if not account:
                print("\n--- 请输入登录信息 ---")
                account = input("账号/手机号: ").strip()
                password = input("密码: ").strip()

            print(f">>> 正在尝试登录：{account}")
            page.get('https://passport.zhihuishu.com/login')
            
            if page.ele('text:密码登录', timeout=2):
                page.ele('text:密码登录').click()
                time.sleep(0.5)

            page.ele('@placeholder:手机', timeout=2).input(account)
            page.ele('@placeholder:密码', timeout=2).input(password)
            
            if page.ele('.wall-sub-btn', timeout=2):
                page.ele('.wall-sub-btn').click()
            
            print(">>> 等待登录验证 (如出现滑块请手动完成)...")
            
            login_success = False
            while True:
                if "login" not in page.url:
                    print(">>> 登录成功。")
                    save_account_to_pool(account, password)
                    login_success = True
                    break
                    
                if page.ele('text:账号或密码错误', timeout=0.5):
                    print(">>> 登录失败：账号或密码错误。")
                    account, password = None, None # 重置以便下次手动输入
                    break
                time.sleep(1)
            
            if login_success: 
                return # 登录完成，退出函数
                
        except Exception as e:
            print(f">>> 运行异常: {e}")
            time.sleep(2)