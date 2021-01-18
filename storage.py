import json

from render_storage import RenderStorage
from get_data_from_csv_xls import Item, WayBill


class TalkToDB:
    def __init__(self):
        pass

    def send_to_db(self, item, cell):
        pass

    def get_from_db(self, key):
        pass

    def send_to_remote_db(self, data):
        pass


class Storage(RenderStorage):
    def __init__(self, host, port):
        super().__init__(host, port)
        self.items_dict = {}
        self.database_sender = TalkToDB()

    def put(self, way_bill: WayBill):
        """START PROCESS OF PUTTING"""
        data = way_bill.create_item_list()
        return self._solve_how_to_put(data)

    def _solve_how_to_put(self, items):
        """SOLVE HOW TO PUT ITEM TO DB"""
        _data_to_send_to_api = []

        for _item_num in range(len(items) - 1, -1, -1):
            _item_was_put = False
            for _block_num in range(self.height - 1, -1, -1):
                for _cell_num in range(self.width - 1, -1, -1):
                    _cell = self.cells[_block_num][_cell_num]
                    _item = items[_item_num]
                    _gab = self._check_gabarits(_item, _cell)
                    if not _cell.busy:
                        if _gab:
                            if _cell.size_height + _cell.size_width + _cell.size_depth == _gab:
                                _cell.put_to_cell(_item)
                                self.items_dict.update({_item.uuid: _item})

                                if _cell.merged:
                                    for _merged_cell in _cell.merged_with:
                                        self.easy_find_cell_by_name[_merged_cell].put_to_cell(_item)

                                _data_to_send_to_api.append({"uuid": _item.uuid,
                                                             "destination": [
                                                                 _cell.name] if not _cell.merged else _cell.merged_with})
                                self.database_sender.send_to_db(_item, _cell)

                                _item_was_put = True
                                break
                        else:
                            self.database_sender.send_to_remote_db(_item)
                if _item_was_put:
                    break
        resp = json.loads(self.put_item_api(_data_to_send_to_api))
        if resp["status"] == "ok":
            super(Storage, self).render()
            return "OK"
        else:
            return "Error"

    def _check_gabarits(self, _item: Item, _cell):
        """CHECK SIZE OF ITEM"""
        if ((_item.height + _item.width + _item.depth) > 5) or _item.height > 2 or _item.width > 2 or _item.depth > 2:
            return 0
        elif _item.height == 1 and _item.width == 1 and _item.depth == 1:
            return 3
        elif ((_item.height == 2 and _item.depth == 1 and _item.width == 1) or (
                _item.height == 1 and _item.depth == 2 and _item.width == 1) or (
                      _item.height == 1 and _item.depth == 1 and _item.width == 2)):
            return 4
        else:
            return 5

    def get(self, uuid: str):
        """GET POSITION FROM STORAGE"""
        pass


tr = Storage("127.0.0.1", "5000")
print(tr.get_schema_api())
print()
for i in tr.cells:
    for j in i:
        print(j.busy, end=" ")
    print()
print()
tr.render()
wb = WayBill("/Users/ovsannikovaleksandr/Desktop/предпроф/for_test.xlsx")
for i in wb.create_item_list():
    print(i.__dict__)

print()
print(tr.put(wb))
print(tr.items_dict)
print()

for i in tr.cells:
    for j in i:
        print(j.busy, end=" ")
    print()
print()
