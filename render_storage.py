import json

from get_data_from_csv_xls import Item
from send_requests import StorageApi
from PIL import Image, ImageDraw, ImageColor, ImageFont


class Cell:
    def __init__(self, name, lvl, merged, group_of_merge=0, merged_with=[], size_width=None, size_height=None, size_depth=1, busy=False):
        self.name = name
        self.lvl = lvl
        self.merged = merged
        self.group_of_merge = group_of_merge
        self.merged_with = merged_with
        self.size_width = size_width
        self.size_height = size_height
        self.size_depth = size_depth
        self.busy = busy
        #for render merged cells
        self.rendered=False

        self.contained_item=None

    def _make_free(self):
        self.busy = False
    def _make_busy(self):
        self.busy = True

    def put_to_cell(self, item: Item):
        self.contained_item = item
        self._make_busy()

    def get_from_item(self):
        self.contained_item = None
        self._make_free()
    def make_rendered(self):
        self.rendered = True
    def make_not_rendered(self):
        self.rendered = False


class RenderStorage(StorageApi):
    def __init__(self, host, port):
        super().__init__(host, port)
        _ = json.loads(super(RenderStorage, self).get_schema_api())
        self.num_to_coords = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I', 10: 'J', 11: 'K',
                              12: 'L', 13: 'M', 14: 'N', 15: 'O', 16: 'P', 17: 'Q', 18: 'R', 19: 'S', 20: 'T', 21: 'U',
                              22: 'V', 23: 'W', 24: 'X', 25: 'Y', 26: 'Z'}
        self.depth = 1
        self.directions = {}
        if _["size"]["size_x"] == 1:
            self.directions["depth"] = "x"

            __resp = json.loads(
                super(RenderStorage, self) \
                    .position_api(
                    {"destination": [self.num_to_coords[_["size"]["size_y"]] + str(_["size"]["size_z"])]}))

            if __resp["status"] == "position is empty":
                self.directions["width"] = "z"
                self.width = _["size"]["size_z"]

                self.directions["height"] = "y"
                self.height = _["size"]["size_y"]

            else:
                self.directions["width"] = "y"
                self.width = _["size"]["size_y"]

                self.directions["height"] = "z"
                self.height = _["size"]["size_z"]



        elif _["size"]["size_y"] == 1:
            self.directions["depth"] = "y"

            __resp = json.loads(
                super(RenderStorage, self) \
                    .position_api(
                    {"destination": [self.num_to_coords[_["size"]["size_x"]] + str(_["size"]["size_z"])]}))

            if __resp["status"] == "position is empty":
                self.directions["width"] = "z"
                self.width = _["size"]["size_z"]

                self.directions["height"] = "x"
                self.height = _["size"]["size_x"]

            else:
                self.directions["width"] = "x"
                self.width = _["size"]["size_x"]

                self.directions["height"] = "z"
                self.height = _["size"]["size_z"]


        elif _["size"]["size_z"] == 1:
            self.directions["depth"] = "z"

            __resp = json.loads(
                super(RenderStorage, self) \
                    .position_api(
                    {"destination": [self.num_to_coords[_["size"]["size_x"]] + str(_["size"]["size_y"])]}))

            if __resp["status"] == "position is empty":
                self.directions["width"] = "y"
                self.width = _["size"]["size_y"]

                self.directions["height"] = "x"
                self.height = _["size"]["size_x"]

            else:
                self.directions["width"] = "x"
                self.width = _["size"]["size_x"]

                self.directions["height"] = "y"
                self.height = _["size"]["size_y"]

        self.merged = _["merged"]
        self.cells = []

        self.group_of_merge = {}
        self.merged_from_group = {}
        self._determine_group_of_merge()
        self.easy_find_cell_by_name={}
        for w in range(self.height):
            _c_to_add = []
            for h in range(self.width):
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

            for _block in self.cells:
                for _cell in _block:
                    self.easy_find_cell_by_name[_cell.name] = _cell

    def _check_merged(self, cell):
        for m in self.merged:
            if cell in m:
                return True
        return False

    def _determine_group_of_merge(self):
        self.merged_from_group[0] = []
        for group_num in range(len(self.merged)):
            for cell in self.merged[group_num]:
                self.group_of_merge[cell] = group_num + 1
                if group_num + 1 in self.merged_from_group:
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

    def render(self):
        #preparation for rendering
        for _ in list(self.easy_find_cell_by_name.values()):
            _.rendered=False

        _width = (self.width + 2) * 100
        _height = (self.height + 2) * 100
        image = Image.new("RGB", (_width, _height), (255, 255, 255))
        draw = ImageDraw.Draw(image)

        for w in range(self.width + 1):
            for h in range(self.height + 1):
                draw.line(
                    (100 + (w * 100), _height - ((self.height + 1) * 100), 100 + (w * 100), (self.height + 1) * 100),
                    fill=ImageColor.getrgb("black"))
                draw.line(((w * 100) + 100, 100 + (h * 100), 100, 100 + (h * 100)),
                          fill=ImageColor.getrgb("black"))
        font = ImageFont.truetype("Arial.ttf", 16)
        for block_num in range(self.height):
            for cell_num in range(self.width):
                _cell = self.cells[block_num][cell_num]
                if _cell.merged == True:
                    try:
                        if self.cells[block_num][cell_num + 1].merged == True and _cell.group_of_merge == \
                                self.cells[block_num][cell_num + 1].group_of_merge:
                            draw.line((100 + ((cell_num + 1) * 100), 100 + (block_num * 100),
                                       (100 + ((cell_num + 1) * 100)), 200 + (block_num * 100)),
                                      fill=ImageColor.getrgb("white"))
                    except IndexError as e:
                        pass

                    try:
                        if self.cells[block_num + 1][cell_num].merged == True and _cell.group_of_merge == \
                                self.cells[block_num + 1][cell_num].group_of_merge:
                            draw.line((100 + (cell_num * 100), 100 + ((block_num + 1) * 100),
                                       (200 + (cell_num * 100)), 100 + ((block_num + 1) * 100)),
                                      fill=ImageColor.getrgb("white"))
                    except IndexError as e:
                        pass

                if _cell.busy and not _cell.rendered:
                    if _cell.merged == False:
                        _cell.rendered = True
                        draw.line((100 + ((cell_num) * 100), 100 + (block_num * 100),
                                   (200 + ((cell_num) * 100)), 200 + (block_num * 100)),
                                  fill=ImageColor.getrgb("red"))
                        draw.line((200 + ((cell_num) * 100), 100 + (block_num * 100),
                                   (100 + ((cell_num) * 100)), 200 + (block_num * 100)),
                                  fill=ImageColor.getrgb("red"))
                    else:
                        if len(_cell.merged_with) == 2:
                            draw.line((100 + ((cell_num) * 100), 100 + (block_num * 100),
                                       (200 + ((cell_num+1) * 100)), 200 + (block_num * 100)),
                                      fill=ImageColor.getrgb("red"))
                            draw.line((200 + ((cell_num+1) * 100), 100 + (block_num * 100),
                                       (100 + ((cell_num) * 100)), 200 + (block_num * 100)),
                                      fill=ImageColor.getrgb("red"))
                        else:
                            draw.line((100 + ((cell_num) * 100), 100 + (block_num * 100),
                                       (200 + ((cell_num+1) * 100)), 200 + ((block_num+1) * 100)),
                                      fill=ImageColor.getrgb("red"))
                            draw.line((200 + ((cell_num+1) * 100), 100 + (block_num * 100),
                                       (100 + ((cell_num) * 100)), 200 + ((block_num+1) * 100)),
                                      fill=ImageColor.getrgb("red"))
                        for _merged_cell in _cell.merged_with:
                            self.easy_find_cell_by_name[_merged_cell].rendered = True

                if not _cell.busy and _cell.rendered:
                    if _cell.merged == False:
                        _cell.rendered = False
                        draw.line((100 + ((cell_num) * 100), 100 + (block_num * 100),
                                   (200 + ((cell_num) * 100)), 200 + (block_num * 100)),
                                  fill=ImageColor.getrgb("white"))
                        draw.line((200 + ((cell_num) * 100), 100 + (block_num * 100),
                                   (100 + ((cell_num) * 100)), 200 + (block_num * 100)),
                                  fill=ImageColor.getrgb("white"))
                    else:

                        if len(_cell.merged_with) == 2:
                            draw.line((100 + ((cell_num) * 100), 100 + (block_num * 100),
                                       (200 + ((cell_num+1) * 100)), 200 + (block_num * 100)),
                                      fill=ImageColor.getrgb("white"))
                            draw.line((200 + ((cell_num+1) * 100), 100 + (block_num * 100),
                                       (100 + ((cell_num) * 100)), 200 + (block_num * 100)),
                                      fill=ImageColor.getrgb("white"))
                        else:
                            draw.line((100 + ((cell_num) * 100), 100 + (block_num * 100),
                                       (200 + ((cell_num+1) * 100)), 200 + ((block_num+1) * 100)),
                                      fill=ImageColor.getrgb("white"))
                            draw.line((200 + ((cell_num+1) * 100), 100 + (block_num * 100),
                                       (100 + ((cell_num) * 100)), 200 + ((block_num+1) * 100)),
                                      fill=ImageColor.getrgb("white"))
                        for _merged_cell in _cell.merged_with:
                            self.easy_find_cell_by_name[_merged_cell].rendered = False




                draw.text((((cell_num + 1) * 100) + 50, ((block_num + 1) * 100) + 50), text=_cell.name,
                          fill=ImageColor.getrgb("black"), font=font)

        del draw
        image.save("test.png", "PNG")
