import requests


class StorageApi:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def get_schema(self):
        answer = requests.get("http://"+self.host+":"+self.port+"/scheme")
        return answer.text

    def put_item(self, data):
        try:
            answer = requests.post(url="http://"+self.host+":"+self.port,
                                   json=data)
            return answer.text
        except Exception as e:
            print(e)

    def position(self, destination):
        try:
            answer = requests.get(url="http://"+self.host+":"+self.port+"/position",
                                  params=destination)
            return answer.text
        except Exception as e:
            print(e)
