# -*- coding: utf-8 -*-
import requests
import re
import sys
import urllib3
from rich.console import Console
delete_warning = urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

__author__ = "K0uSAOF"
console = Console()

'''
/ispirit/login_code.php  --> codeuid : A6C30487-3FA8-5171-26BA-29FB06E3EB69
'''
head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0","Connection": "close"}
proxies = {'http:':'http://127.0.0.1:33210','https':'http://127.0.0.1:33210'}

def check(url):
    '''
    检测存在漏洞的版本号
    '''
    target = url + "/inc/expired.php"

    try:
        res = requests.post(target,headers=head,timeout=5,verify=False)
        res.encoding = 'gb2312'
        # print(res.status_code)

        if res.status_code == 200:
            try:
                com_o = re.compile(r"<title>(?P<title>.*?)</title>",re.S)
                com_t = re.compile(r"[0-9]{4}")
                title = com_o.search(res.text).group("title")
                version = com_t.search(title).group()

                if version == "2017":
                    console.log("[green][+] Version : %s" %version)
                    with open('2017_version_urls.txt','a') as f:
                        f.write(target + "\n")
                elif version != '':
                    console.log("[green][+] Version : %s" %version)
            except:
                console.log("[red][!] Version info not found!")

    except Exception as e:
        console.log("[red][!] Error!")

def main():
    with open('urls.txt','r') as f:
        urls = f.readlines()
        with console.status("[bold green]Check...") as status:
            for url in urls:
                url = url.replace("\n","")
                console.log("[yellow][+] start check --> %s" %url)
                check(url)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.log(f"[yellow][!] Bye!")
