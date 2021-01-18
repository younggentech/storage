import requests


class StorageApi:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def get_schema_api(self):
        answer = requests.get("http://"+self.host+":"+self.port+"/scheme")
        return answer.text

    def put_item_api(self, data):
        try:
            answer = requests.post(url="http://"+self.host+":"+self.port,
                                   json=data)
            return answer.text
        except Exception as e:
            print(e)

    def position_api(self, destination):
        try:
            answer = requests.get(url="http://"+self.host+":"+self.port+"/position",
                                  params=destination)
            return answer.text
        except Exception as e:
            print(e)
