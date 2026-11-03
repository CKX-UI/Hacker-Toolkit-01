import requests
import concurrent.futures
import time

# 目标网址
base_url = "http://www.sdsoft.org.cn/"
if not base_url.endswith("/"):
    base_url += "/"

# 伪装请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}

# 内置更丰富的路径字典
test_paths = [
    "index.php", "config/", "vul/", "robots.txt", "admin/", 
    "login.php", "phpinfo.php", "www.zip", ".git/config",
    "upload/", "backup/", "test/", "db/", "install/",
    "admin.php", "api/", "upload.php", "info.php", "flag.txt"
]

def scan_path(path):
    target_url = base_url + path
    try:
        # 发送请求，allow_redirects=False 防止 302 自动跳转
        response = requests.get(target_url, headers=headers, timeout=3, allow_redirects=False)
        status = response.status_code
        
        # 状态码判断
        if status == 200:
            msg = f"[+] 发现 (200 OK): {target_url}"
            print(msg)
            save_result(msg)
        elif status == 403:
            msg = f"[!] 权限拒绝 (403): {target_url}"
            print(msg)
            save_result(msg)
        elif status in [301, 302]:
            msg = f"[*] 重定向 ({status}): {target_url}"
            print(msg)
            save_result(msg)
        else:
            # 为了屏幕干净，404就不打印了
            pass
            
    except Exception:
        pass

def save_result(msg):
    # 把发现的结果追加写入到 result.txt
    with open("result.txt", "a", encoding="utf-8") as f:
        f.write(msg + "\n")

def main():
    print(f"[*] 开始扫描目标: {base_url}")
    print(f"[*] 加载内置字典，共 {len(test_paths)} 条路径")
    
    # 每次运行前，清空上次的 result.txt
    open("result.txt", "w").close()
    
    start_time = time.time()
    
    # 开启 10 个线程并发扫描
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.map(scan_path, test_paths)
        
    print(f"\n[*] 扫描完成，总耗时: {time.time() - start_time:.2f} 秒")
    print(f"[*] 战利品已保存到当前目录下的 result.txt 中")

if __name__ == "__main__":
    main()
