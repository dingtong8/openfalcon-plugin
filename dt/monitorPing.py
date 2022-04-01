import json
import socket
import subprocess
import time
import requests


class Ping:
    """
    接口监控
    """

    def __init__(self):
        self.ip = {
            # 被ping的ip
            'dyclub_route': '192.168.31.1',
            'dyclub_gw': '192.168.1.1'
        }

    def pushData(self, payload):
        r = requests.post("http://192.168.31.222:1988/v1/push", data=json.dumps(payload))
        print(r.text)

    def ping_start(self):
        payload = []
        for key, value in self.ip.items():
            cmd = "ping -c1 %s | awk -F' |=' '/(time=)/{print $(NF-1)}'" % value
            output = subprocess.check_output("{0}".format(cmd), shell=True)
            out = output.decode(encoding='UTF-8').strip()
            ts = int(time.time())
            payload.append(
                {
                    "endpoint": socket.gethostname(),
                    "metric": "ping",
                    "timestamp": ts,
                    "step": 60,
                    "value": float(out),
                    "counterType": "GAUGE",
                    "tags": 'ip={},name={}'.format(value, key),
                }
            )
        self.pushData(payload)


ping = Ping()
ping.ping_start()
