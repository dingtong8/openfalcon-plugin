# 脚本描述：机房服务器温度监控
import json
import time
import socket
import paramiko
import requests
import subprocess

from src.settings import HOST_CONFIG


################### WIN ###################
class Temp:
    """
    服务器温度监控
    """
    def __init__(self):

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(HOST_CONFIG['host'], HOST_CONFIG['port'], HOST_CONFIG['user'], HOST_CONFIG['password'])
        self.cmd_cpu = "sensors | grep 'Core' | awk -F'°C' '{print $1}' | tr -d ' ' | tr -s ':+' ','"
        self.cmd_disk = "/usr/sbin/smartctl -H %s | grep -i 'health' | awk '{print $NF}'"

    def pushData(self, payload):
        r = requests.post("http://192.168.31.222:1988/v1/push", data=json.dumps(payload))
        print(r.text)

    def temp_cpu(self):
        """
        监控服务器CPU温度
        linux服务器安装 yum install lm_sensors -y
        $ sensors
        :return:
        """
        sensorsstdin, sensorsstdout, sensorsstderr = self.ssh.exec_command(self.cmd_cpu)
        sensorsout = str(sensorsstdout.read(), encoding='utf-8')
        payload = []
        ts = int(time.time())
        for i in sensorsout.split():
            core = i.split(',')[0]
            temp = i.split(',')[1]
            payload.append(
                {
                    "endpoint": socket.gethostname(),
                    "metric": "temp",
                    "timestamp": ts,
                    "step": 60,
                    "value": float(temp),
                    "counterType": "GAUGE",
                    "tags": 'core={}'.format(core),
                }
            )
        print(payload)
        # self.pushData(payload)

    def temp_disk(self):
        """
        监控服务器硬盘健康状况
        linux服务器安装 yum search hddtemp -y
        $ smartctl -H /dev/sda -d megaraid,0 | grep -i 'health'
        $ smartctl -H /dev/sda | grep -i 'health'
        :return:
        """
        sensorsstdin, sensorsstdout, sensorsstderr = self.ssh.exec_command("lsblk -d | grep -v 'NAME' | awk '{print $1}'")
        sensorsout = str(sensorsstdout.read(), encoding='utf-8')
        payload = []
        ts = int(time.time())
        for i in sensorsout.split():
            disk = '/dev/{}'.format(i)
            sensorsstdin, sensorsstdout, sensorsstderr = self.ssh.exec_command(self.cmd_disk % disk)
            sensorsout = str(sensorsstdout.read(), encoding='utf-8')
            ret = sensorsout.strip()
            if ret == 'PASSED' or ret == 'OK':
                value = 1
            else:
                value = 0
            payload.append(
                {
                    "endpoint": socket.gethostname(),
                    "metric": "temp",
                    "timestamp": ts,
                    "step": 60,
                    "value": float(value),
                    "counterType": "GAUGE",
                    "tags": 'disk={}'.format(disk),
                }
            )
        print(payload)
        # self.pushData(payload)

    def ssh_close(self):
        self.ssh.close()


temp = Temp()
temp.temp_cpu()
temp.temp_disk()
temp.ssh_close()


################### LINUX ###################
class Temp:
    """
    服务器温度监控
    """
    def __init__(self):

        # self.ssh = paramiko.SSHClient()
        # self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # self.ssh.connect(HOST_CONFIG['host'], HOST_CONFIG['port'], HOST_CONFIG['user'], HOST_CONFIG['password'])
        self.cmd_cpu = "sensors | grep 'Core' | awk -F'°C' '{print $1}' | tr -d ' ' | tr -s ':+' ','"
        self.cmd_disk = "/usr/sbin/smartctl -H %s | grep -i 'health' | awk '{print $NF}'"

    def pushData(self, payload):
        r = requests.post("http://192.168.31.222:1988/v1/push", data=json.dumps(payload))
        print(r.text)

    def temp_cpu(self):
        """
        监控服务器CPU温度
        linux服务器安装 yum install lm_sensors -y
        $ sensors
        :return:
        """
        output = subprocess.check_output(self.cmd_cpu, shell=True)
        out = output.decode(encoding='utf-8').strip()
        payload = []
        ts = int(time.time())
        for i in out.split():
            core = i.split(',')[0]
            temp = i.split(',')[1]
            payload.append(
                {
                    "endpoint": socket.gethostname(),
                    "metric": "temp",
                    "timestamp": ts,
                    "step": 60,
                    "value": float(temp),
                    "counterType": "GAUGE",
                    "tags": 'core={}'.format(core),
                }
            )
        print(payload)
        self.pushData(payload)

    def temp_disk(self):
        """
        监控服务器硬盘健康状况
        linux服务器安装 yum search hddtemp -y
        $ smartctl -H /dev/sda -d megaraid,0 | grep -i 'health'
        $ smartctl -H /dev/sda | grep -i 'health'
        :return:
        """
        output = subprocess.check_output("lsblk -d | grep -v 'NAME' | awk '{print $1}'", shell=True)
        out = output.decode(encoding='utf-8').strip()
        payload = []
        ts = int(time.time())
        for i in out.split():
            disk = '/dev/{}'.format(i)
            output = subprocess.check_output(self.cmd_disk % disk, shell=True)
            out = output.decode(encoding='utf-8').strip()
            ret = out.strip()
            if ret == 'PASSED' or ret == 'OK':
                value = 1
            else:
                value = 0
            payload.append(
                {
                    "endpoint": socket.gethostname(),
                    "metric": "temp",
                    "timestamp": ts,
                    "step": 60,
                    "value": float(value),
                    "counterType": "GAUGE",
                    "tags": 'disk={}'.format(disk),
                }
            )
        print(payload)
        self.pushData(payload)

    def ssh_close(self):
        self.ssh.close()


temp = Temp()
temp.temp_cpu()
temp.temp_disk()

