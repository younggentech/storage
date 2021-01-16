import os.path


class Item:
    def __init__(self, uuid, name, width, height, depth, mass):
        self.uuid = uuid
        self.name = name
        self.width = width
        self.height = height
        self.depth = depth
        self.mass = mass


class WayBill:
    def __init__(self, fileway):
        if os.path.exists(fileway):
            self.fileway = fileway
        else:
            raise FileNotFoundError
