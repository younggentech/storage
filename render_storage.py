import json
from send_requests import StorageApi


class RenderStorage(StorageApi):

    def __init__(self, host, port):
        super().__init__(host, port)
        _ = json.loads(super(RenderStorage, self).get_schema())
        self.num_to_coords = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I', 10: 'J', 11: 'K',
                              12: 'L', 13: 'M', 14: 'N', 15: 'O', 16: 'P', 17: 'Q', 18: 'R', 19: 'S', 20: 'T', 21: 'U',
                              22: 'V', 23: 'W', 24: 'X', 25: 'Y', 26: 'Z'}
        self.depth = 1
        self.directions = {}
        if _["size"]["size_x"] == 1:
            self.directions["depth"] = "x"

            __resp = json.loads(
                super(RenderStorage, self) \
                    .position(
                    {"destination": [self.num_to_coords[_["size"]["size_y"]] + str(_["size"]["size_z"])]}
                ))

            if __resp["status"] == "position is empty":
                self.directions["width"] = "y"
                self.width = _["size"]["size_y"]

                self.directions["height"] = "z"
                self.height = _["size"]["size_z"]

            else:
                self.directions["width"] = "z"
                self.width = _["size"]["size_z"]

                self.directions["height"] = "y"
                self.height = _["size"]["size_y"]



        elif _["size"]["size_y"] == 1:
            self.directions["depth"] = "y"

            __resp = json.loads(
                super(RenderStorage, self) \
                    .position(
                    {"destination": [self.num_to_coords[_["size"]["size_x"]] + str(_["size"]["size_z"])]}
                ))

            if __resp["status"] == "position is empty":
                self.directions["width"] = "x"
                self.width = _["size"]["size_x"]

                self.directions["height"] = "z"
                self.height = _["size"]["size_z"]

            else:
                self.directions["width"] = "z"
                self.width = _["size"]["size_z"]

                self.directions["height"] = "x"
                self.height = _["size"]["size_x"]


        elif _["size"]["size_z"] == 1:
            self.directions["depth"] = "z"

            __resp = json.loads(
                super(RenderStorage, self) \
                    .position(
                    {"destination": [self.num_to_coords[_["size"]["size_x"]] + str(_["size"]["size_y"])]}
                ))

            if __resp["status"] == "position is empty":
                self.directions["width"] = "x"
                self.width = _["size"]["size_x"]

                self.directions["height"] = "y"
                self.height = _["size"]["size_y"]

            else:
                self.directions["width"] = "y"
                self.width = _["size"]["size_y"]

                self.directions["height"] = "x"
                self.height = _["size"]["size_x"]

# tr =RenderStorage("127.0.0.1", "5000")
#
# print(tr.height)
# print(tr.width)
