from get_data_from_csv_xls import Item


class TempStorage:
    def __int__(self):
        self.items = []

    def add_item(self, item: Item):
        self.items.append(item)

    def get_items(self):
        return self.items
