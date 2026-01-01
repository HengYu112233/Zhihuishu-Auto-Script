# ==========================================
# 智慧树全自动挂机脚本
# ==========================================

import time
import ctypes 
from core.browser import init_browser
from core.account_manager import start_up_check
from core.login import execute_login_process
from features import quiz_solver, video_watcher

# 1. 启动检查与账号获取
my_account, my_password = start_up_check()

# 2. 初始化浏览器
page = init_browser()

# 3. 执行登录
execute_login_process(page, my_account, my_password)

# ==========================================
# 挂机注意事项提示
# ==========================================
print("\n" + "="*66)
print("【 重要提示：请务必遵守以下操作规范以防卡顿 】")
print("1.可以随意操作电脑,脚本不受影响。")
print("2. Chrome 浏览器可以最小化了！")
print("3. Chrome 浏览器可以放在其他虚拟桌面了！")
print("4. Chrome 浏览器「不要把窗口缩得太小」，确保视频和目录区域可见！")
print("如果发现其他bug，请及时向我反馈，你们都是我最好的测试员")
print("\n提示：若发现卡住，只需把浏览器窗口点出来停留几秒，即可恢复运行。")
print("="*66 + "\n")

# ==========================================
#  第四部分：挂机守护循环
# ==========================================
print("\n[ 提示：请在浏览器中手动点击进入视频播放页面 ]")
input(">>> 确认进入视频页后，请在该页面按 [回车键] 开启自动刷课...") 

try:
    ctypes.windll.kernel32.SetThreadExecutionState(0x80000001 | 0x00000002)
    print(">>> 已激活防休眠模式：挂机期间电脑将保持常亮。")
except:
    pass

print(">>> 挂机守护中：正在监测答题弹窗与播放进度...")
print(">>> Ctrl+C 关闭脚本")

while True:
    try:
        # 1. 弹窗处理
        quiz_solver.handle_quiz(page)

        # 2. 获取视频状态
        video_status = video_watcher.check_video_status(page)

        # 3. 跳转逻辑
        if video_status and (video_status['ended'] or video_status['is_almost_done']):
            jump_success = video_watcher.handle_jump_logic(page)
            if jump_success:
                continue 
            else:
                break 
        
        # 4. 播放守护逻辑
        else:
            video_watcher.protect_playback(page)
        
        time.sleep(2) 
        
    except Exception as e:
        time.sleep(3)