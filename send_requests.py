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

# ниже пример использования класса:
# a = StorageApi("127.0.0.1", "5000")
# print((a.get_schema()))
# print(a.position({"destination":["A1"]}))
# print(a.put_item([{"uuid": "67568fb7f2c1d06d40450a478863bab1", "destination":["A1"]}]))
# print(a.position({"destination":["A1"]}))
# print(a.put_item([{"uuid": "67568fb7f2c1d06d40450a478863bab1", "destination":["A1"]}]))
