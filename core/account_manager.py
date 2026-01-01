import winreg
import json
import msvcrt
import time
from config import REG_PATH

def get_account_pool():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_READ)
        data, _ = winreg.QueryValueEx(key, "AccountPool")
        winreg.CloseKey(key)
        return json.loads(data)
    except:
        return []

def save_account_to_pool(user, pwd):
    pool = get_account_pool()
    pool = [acc for acc in pool if acc['user'] != user]
    pool.insert(0, {"user": user, "pwd": pwd})
    pool = pool[:9]
    try:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
        winreg.SetValueEx(key, "AccountPool", 0, winreg.REG_SZ, json.dumps(pool))
        winreg.SetValueEx(key, "LastUser", 0, winreg.REG_SZ, user)
        winreg.CloseKey(key)
        print(f">>> 账号 {user} 已成功同步至本地库。")
    except Exception as e:
        print(f">>> 错误：保存账号信息失败: {e}")

def select_account_from_pool():
    pool = get_account_pool()
    print("\n--- 账号切换列表 ---")
    if not pool:
        print("记录为空，请选择 [0] 登录新账号。")
    else:
        for i, acc in enumerate(pool, 1):
            print(f"[{i}] {acc['user']}")
    print("[0] 登录其他新账号")
    print("--------------------")
    
    while True:
        print("请按数字键选择：", end="", flush=True)
        ch = msvcrt.getch().decode('utf-8')
        print(ch)
        if ch == '0':
            return None, None
        if ch.isdigit() and 1 <= int(ch) <= len(pool):
            target = pool[int(ch)-1]
            print(f">>> 已选择账号：{target['user']}")
            return target['user'], target['pwd']
        print("输入无效，请重新按数字键选择。")

def account_management_mode():
    while True:
        pool = get_account_pool()
        default_user = pool[0]['user'] if pool else "无"
        
        print("\n--- 账号管理页面 ---")
        print(f"当前默认账号: {default_user}")
        print("--------------------")
        print("[1] 删除当前默认账号")
        print("[2] 删除所有保存的账号")
        print("[回车] 返回继续登录")
        print("--------------------")
        
        choice = input("请选择管理指令: ").strip()

        if not choice:
            print(">>> 正在返回...")
            break

        if choice == '1':
            if default_user == "无":
                print(">>> 提示：当前没有可删除的账号。")
                continue
            
            confirm = input(f"确认删除账号 {default_user} 吗？(y/n): ").lower()
            if confirm == 'y':
                new_pool = [acc for acc in pool if acc['user'] != default_user]
                try:
                    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
                    winreg.SetValueEx(key, "AccountPool", 0, winreg.REG_SZ, json.dumps(new_pool))
                    if not new_pool:
                        try: winreg.DeleteValue(key, "LastUser")
                        except: pass
                    else:
                        winreg.SetValueEx(key, "LastUser", 0, winreg.REG_SZ, new_pool[0]['user'])
                    winreg.CloseKey(key)
                    print(f">>> 账号 {default_user} 已成功删除。")
                except Exception as e:
                    print(f">>> 错误：操作失败 {e}")
            else:
                print(">>> 操作已取消。")

        elif choice == '2':
            confirm = input("确认清空所有已保存的账号记录吗？此操作不可撤销。(y/n): ").lower()
            if confirm == 'y':
                try:
                    winreg.DeleteKey(winreg.HKEY_CURRENT_USER, REG_PATH)
                    print(">>> 账号库已彻底清空。")
                except:
                    print(">>> 提示：库已经是空的。")
            else:
                print(">>> 操作已取消。")
        else:
            print(">>> 输入无效。")

def start_up_check():
    print("----------------------------------------")
    print("   智慧树自动刷课脚本2.0  ")
    print("----------------------------------------")
    pool = get_account_pool()
    default_acc = pool[0] if pool else None
    
    if default_acc:
        print(f"当前默认账号: {default_acc['user']}")
        print("提示：3秒内按 [C] 清空记录 | 按 [V] 切换账号")
        print("提示：使用英文输入法")
        for i in range(3, 0, -1):
            print(f"等待响应... {i}", end="\r")
            time.sleep(1)
            if msvcrt.kbhit():
                key = msvcrt.getch().lower()
                if key == b'c':
                    account_management_mode()
                    return start_up_check()
                elif key == b'v':
                    return select_account_from_pool()
        print("\n>>> 执行自动登录...")
        return default_acc['user'], default_acc['pwd']
    
    print("未检测到存档账号，请手动输入。")
    return None, None