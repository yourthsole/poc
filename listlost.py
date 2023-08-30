# -*- coding: utf-8 -*-
import requests
import json
import argparse

def banner():
    print("""

.____    .__          __    .__                  __   
|    |   |__| _______/  |_  |  |   ____  _______/  |_ 
|    |   |  |/  ___/\   __\ |  |  /  _ \/  ___/\   __/
|    |___|  |\___ \  |  |   |  |_(  <_> )___ \  |  |  
|_______ \__/____  > |__|   |____/\____/____  > |__|  
        \/       \/                         \/        


    tag: This is a script that verifies a directory disclosure vulnerability
    @author: zxy
    @version: 1.0.0
    """)

def main():
    parser = argparse.ArgumentParser(description="Directory Disclosure Vulnerability Checker")

    # 添加命令行参数选项，并通过设置dest参数来重命名选项名称
    parser.add_argument("-u", "--url", dest="url", help="Example: http://www.example.com")
    parser.add_argument("-f", "--file", dest="file", help="urls.txt")
    parser.add_argument("--hh", action="store_true", help="显示帮助信息")

    args = parser.parse_args()

    if args.hh:
        parser.print_help()
        return

    if args.url:
        check_url(args.url)
    elif args.file:
        check_urls_from_file(args.file)
    else:
        print("请使用 -hh 选项查看帮助信息。")

def check_url(url):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            with open("result.txt", "w", encoding="utf-8") as file:
                formatted_data = json.dumps(data, indent=4, ensure_ascii=False)
                file.write(formatted_data)
                print("内容已保存到result.txt文件中")
        else:
            print(f"请求失败，状态码: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"请求发生异常: {str(e)}")

    except Exception as e:
        print(f"发生了其他异常: {str(e)}")

def check_urls_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            urls = file.read().splitlines()

        for url in urls:
            check_url(url)

    except FileNotFoundError:
        print(f"文件 '{file_path}' 未找到。")

if __name__ == "__main__":
    banner()
    main()
