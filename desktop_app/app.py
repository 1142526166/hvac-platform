# -*- coding: utf-8 -*-
"""
冰水群控平台 - 桌面壳
- 启动本地静态服务器（随机端口），serve 打包进 exe 的 index.html
- 用系统 WebView（Windows: Edge WebView2）打开窗口
- 不弹控制台
"""
import os, sys, threading, http.server, socketserver, random, time

def resource_dir():
    # PyInstaller 打包后资源在 sys._MEIPASS；源码运行时在脚本同目录
    if hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

def start_server():
    root = resource_dir()
    os.chdir(root)
    port = random.randint(18000, 25000)
    handler = lambda *a: http.server.SimpleHTTPRequestHandler(*a)
    httpd = socketserver.TCPServer(("127.0.0.1", port), handler)
    # 让单线程服务器在后台线程跑
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    # 等待服务器就绪
    for _ in range(50):
        try:
            import urllib.request
            urllib.request.urlopen("http://127.0.0.1:%d/index.html" % port, timeout=0.3)
            break
        except Exception:
            time.sleep(0.1)
    return port

def main():
    port = start_server()
    import webview
    window = webview.create_window(
        "冰水系统能耗预测与参数化运行优化平台",
        "http://127.0.0.1:%d/index.html" % port,
        width=1440, height=900, min_size=(1100, 700),
    )
    webview.start()

if __name__ == "__main__":
    main()
