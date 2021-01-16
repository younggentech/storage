import os.path
import uuid
from pandas import read_excel




class Item(object):


    def __init__(self, name, height, width, depth, mass):
        self.name = name
        self.height = height
        self.width = width
        self.depth = depth
        self.mass = mass
        self.uuid = uuid.uuid4().hex

    def __eq__(self, other) -> bool:
        if isinstance(other, Item):
            return self.mass == other.mass

        return NotImplemented

    def __ne__(self, other) -> bool:
        if isinstance(other, Item):
            return self.mass != other.mass

        return NotImplemented

    def __lt__(self, other) -> bool:
        if isinstance(other, Item):
            return self.mass < other.mass

        return NotImplemented

    def __le__(self, other) -> bool:
        if isinstance(other, Item):
            return self.mass <= other.mass

        return NotImplemented

    def __gt__(self, other) -> bool:
        if isinstance(other, Item):
            return self.mass > other.mass

        return NotImplemented

    def __ge__(self, other) -> bool:
        if isinstance(other, Item):
            return self.mass >= other.mass

        return NotImplemented



class WayBill:
    def __init__(self, fileway):
        if os.path.exists(fileway):
            self.fileway = fileway
        else:
            raise FileNotFoundError

    def create_item_list(self):
        items = []
        data = read_excel(self.fileway).values.tolist()

        for raw in data:
            _size = raw[2].split("*")
            items.append(Item(
                name=raw[1],
                height=_size[0],
                width=_size[1],
                depth=_size[2],
                mass=raw[-1]
            ))
        return items


wb = WayBill("/Users/ovsannikovaleksandr/Desktop/предпроф/for_test.xlsx")
itms = wb.create_item_list()
for i in itms:
    print(i.mass)