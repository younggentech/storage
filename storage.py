from render_storage import RenderStorage
from get_data_from_csv_xls import Item, WayBill


class Storage(RenderStorage):
    def __init__(self, host, port):
        super().__init__(host, port)

    def put(self, way_bill: WayBill):
        data = way_bill.create_item_list()
        self.solve_how_to_put(data)

    def solve_how_to_put(self, items):
        for block in range(self.height-1, -1,-1):
            for cell in range(self.width-1, -1,-1):
                print(self.cells[block][cell].name, end=" ")
            print()



tr = Storage("127.0.0.1", "5000")

print(tr.height)
print(tr.get_schema())
print(tr.width)

for i in tr.cells:
    for j in i:
        print(j.name, end=" ")
    print()
print()
tr.render()
wb = WayBill("/Users/ovsannikovaleksandr/Desktop/предпроф/for_test.xlsx")
for i in wb.create_item_list():
    print(i.__dict__)

print()
tr.put(wb)
