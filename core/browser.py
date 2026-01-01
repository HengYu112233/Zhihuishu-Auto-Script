from DrissionPage import ChromiumPage, ChromiumOptions
import subprocess
import sys

def init_browser():
    print(">>> 正在启动 Chrome 浏览器...")
    try:
        co = ChromiumOptions()
        # 核心修改：禁用后台降速和冻结策略
        co.set_argument('--disable-background-timer-throttling')
        co.set_argument('--disable-backgrounding-occluded-windows')
        co.set_argument('--disable-renderer-backgrounding')
        
        return ChromiumPage(co)
    except Exception:
        print("\n>>> 错误：系统未安装 Chrome，脚本无法运行。")
        if input(">>> 按 [回车] 打开下载页，或按其他键退出: ") == "":
            subprocess.Popen("explorer https://www.google.cn/chrome/index.html")
        sys.exit()