import json
from send_requests import StorageApi


class Cell:
    def __init__(self, name, lvl, merged, group_of_merge=0, merged_with=[], size_width=None, size_height=None):
        self.name = name
        self.lvl = lvl
        self.merged = merged
        self.group_of_merge = group_of_merge
        self.merged_with = merged_with
        self.size_width = size_width
        self.size_height = size_height


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

        self.merged = _["merged"]
        self.cells = []

        self.group_of_merge = {}
        self.merged_from_group = {}
        self._determine_group_of_merge()

        for w in range(self.width):
            _c_to_add = []
            for h in range(self.height):
                _cell = self.num_to_coords[w + 1] + str(h + 1)
                _width_height = self._determine_width_height_in_merged(_cell)
                _group_of_merge = self.group_of_merge.get(_cell, 0)
                _c_to_add.append(
                    Cell(
                        name=_cell,
                        lvl=w + 1,
                        merged=self._check_merged(_cell),
                        group_of_merge=_group_of_merge,
                        merged_with=self.merged_from_group[_group_of_merge],
                        size_width=_width_height[0],
                        size_height=_width_height[1]
                    )
                )
            self.cells.append(_c_to_add)

    def _check_merged(self, cell):
        for m in self.merged:
            if cell in m:
                return True
        return False

    def _determine_group_of_merge(self):
        self.merged_from_group[0] = []
        for group_num in range(len(self.merged)):
            for cell in self.merged[group_num]:
                self.group_of_merge[cell] = group_num+1
                if group_num+1 in self.merged_from_group:
                    self.merged_from_group[group_num + 1].append(cell)
                else:
                    self.merged_from_group[group_num + 1] = [cell]

    def _determine_width_height_in_merged(self, cell):
        if cell not in self.group_of_merge:
            return (1, 1)
        _values = list(self.group_of_merge.values())
        if _values.count(self.group_of_merge[cell]) == 2:
            return (2, 1)
        else:
            return (2, 2)


tr = RenderStorage("127.0.0.1", "5000")

print(tr.height)
print(tr.get_schema())
print(tr.width)

for i in tr.cells:
    for j in i:
        print(j.group_of_merge, end=" ")
    print()
