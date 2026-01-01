# features/video_watcher.py
import time

def check_video_status(page):
    """检测视频播放状态"""
    return page.run_js('''
        var v = document.querySelector("video");
        if (!v) return null;
        return {
            ended: v.ended,
            is_almost_done: (v.duration > 0 && v.currentTime > v.duration - 1)
        };
    ''')

def handle_jump_logic(page):
    """
    执行跳转下一集的逻辑
    返回 True 表示执行了跳转（主循环需要 continue）
    返回 False 表示无动作
    """
    print(f"[{time.strftime('%H:%M:%S')}] 视频结束，正在定位下一集...")
    
    target_to_click = None

    # --- 方案：广域搜索 (不再依赖 .video 类名) ---
    # 1. 直接锁定右侧容器
    right_box = page.ele('.box-right', timeout=2)
    
    if right_box:
        # 2. 抓取容器内所有 li 标签 (不管它叫什么class)
        all_lis = right_box.eles('tag:li')
        print(f">>> 调试：在列表中发现了 {len(all_lis)} 个条目")

        current_index = -1
        
        # 3. 遍历寻找“当前播放”标记
        for i, li in enumerate(all_lis):
            if 'current_play' in str(li.attr('class')):
                current_index = i
                print(f">>> 找到当前集，位于索引 [{i}]")
                break
        
        # 4. 计算下一集
        if current_index != -1:
            for j in range(current_index + 1, len(all_lis)):
                candidate = all_lis[j]
                if candidate.ele('.catalogue_title', timeout=0.1) or candidate.ele('.time_ico', timeout=0.1):
                    target_to_click = candidate
                    print(f">>> 锁定下一集目标：索引 [{j}]")
                    break
    
    # --- 执行点击 ---
    if target_to_click:
        try:
            page.run_js('arguments[0].scrollIntoView({block: "center"});', target_to_click)
            time.sleep(0.5)
            target_to_click.click()
            print(">>> 已点击列表跳转，等待加载...")
            time.sleep(12)
            return True # 通知主程序 continue
        except Exception as e:
            print(f">>> 点击报错: {e}")

    # --- 兜底方案 ---
    print(">>> 列表定位未成功，尝试底部按钮...")
    next_btn = page.ele('#nextBtn')
    if next_btn and 'disable' not in next_btn.attr('class'):
        next_btn.click()
        time.sleep(12)
        return True # 通知主程序 continue
    else:
        print(">>> 未找到下一集，课程可能已全部完成。")
        return False # 实际上这里意味着结束，但在原逻辑中是 break，这里返回 False 交给主程序处理

def protect_playback(page):
    """播放守护逻辑"""
    try:
        page.run_js('document.querySelector("video").muted = true')  #静音
        if page.run_js('return document.querySelector("video").paused'):
            page.run_js('document.querySelector("video").play()')
    except: 
        pass