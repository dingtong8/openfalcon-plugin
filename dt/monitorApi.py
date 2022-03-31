import requests
import time
import json
import re


class URLooker:
    """
    接口监控
    """

    def __init__(self):
        self.urls = {
            # '被监控链接':'页面关键词'
            'https://dycharts.com/vis/dychart/v2/chartscenetopsearch/?type=c': 'word',
            'https://dycharts.com/vis/share/chart_publish/99fd5559d6540a236c30bba52b0bb4e9': 'projectId'
        }

    def pushData(self, payload):
        r = requests.post("http://192.168.31.222:1988/v1/push", data=json.dumps(payload))
        print(r.text)

    def monitorApi(self):
        for i in self.urls:
            url = i
            keyword = self.urls.get(i)
            ret = requests.get(url)
            if keyword:
                if str(keyword) in ret.text:
                    value = ret.status_code
                else:
                    value = 0
            else:
                value = ret.status_code
            ts = int(time.time())
            #url = re.sub('(:)|(/)|(\?)|(\.)|(=)', '_', url)
            payload = [
                {
                    "endpoint": "Api",
                    "metric": "{0}".format(url),
                    "timestamp": ts,
                    "step": 1800,
                    "value": int(value),
                    "counterType": "GAUGE",
                    "tags": "{0}".format("web=dycharts"),
                }
            ]
            self.pushData(payload)


urlooker = URLooker()
urlooker.monitorApi()


