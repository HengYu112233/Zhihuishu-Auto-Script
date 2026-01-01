# features/quiz_solver.py
import time

def handle_quiz(page):
    """
    处理课中弹窗测验
    """
    if page.ele('.topic-item', timeout=0.1): 
        try:
            page.ele('.topic-item').click() 
            time.sleep(0.5)
            if page.ele('text:关闭'): 
                page.ele('text:关闭').click()
                print(f"[{time.strftime('%H:%M:%S')}] 已自动关闭视频弹窗。")
        except: 
            pass