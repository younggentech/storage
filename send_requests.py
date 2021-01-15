import requests

class storage_api:
    def __init__(self, host, port):
        self.host=host
        self.port = port

    def get_schema(self):
        answer = requests.get("http://"+self.host+":"+self.port+"/scheme")
        return answer.text
