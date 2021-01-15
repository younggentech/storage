import requests

class storage_api:
    def __init__(self, host, port):
        self.host=host
        self.port = port

    def get_schema(self):
        answer = requests.get("http://"+self.host+":"+self.port+"/scheme")
        return answer.text

    def put_item(self,data):
        try:
            answer = requests.post(url="http://"+self.host+":"+self.port,
                                   json=data)
            return answer.text
        except Exception as e:
            print(e)


# a = storage_api("127.0.0.1", "5000")
# a.put_item([{"uuid": "67568fb7f2c1d06d40450a478863bab1", "destination":["A1"]}])