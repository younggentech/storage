import pickle
import base64
from flask import Flask, render_template, request

from get_data_from_csv_xls import WayBill
from storage import StorageMaker

application = Flask(__name__)


@application.route('/')
def hello_world():
    return render_template("index.html", storage=storage_maker.storage)

@application.route('/remote')
def remote_storage():
    with open("remote_storage_data", "rb") as f:
        remote_items = pickle.load(f)
    return render_template("remote.html", items=remote_items, len_of_array = len(remote_items))

@application.route("/report")
def report(items=[], cells = []):
    data = render_template("remote.html", items=items,
                           cells = cells, len_of_array = len(items))
    print(data)
    return  data

#routes for bot->

@application.route("/get_storage")
def get_storage():
    return storage_maker.storage

@application.route("/get_list_of_all", methods=["GET"])
def get_list_of_all():
    pickled = pickle.dumps(storage_maker.storage.unique_cells)
    return base64.b64encode(pickled)

@application.route("/get_scheme", methods=["GET"])
def get_scheme():
    storage_maker.storage.render()
    return "OK"

@application.route("/get_cell", methods=["GET"])
def get_cell():
    _cn = request.args.getlist("cell_name")[0]
    try:
        pickled = pickle.dumps(storage_maker.storage.easy_find_cell_by_name[_cn])
    except KeyError:
        pickled = "Not".encode()

    return base64.b64encode(pickled)

@application.route("/get_data_from_item_search", methods=["GET"])
def get_data_from_item_search():
    _uuid = request.args.getlist("uuid")[0]
    try:
        _cell_name = storage_maker.storage.item_uuid_cell_name_dict[_uuid]
        pickled = pickle.dumps(storage_maker.storage.easy_find_cell_by_name[_cell_name])
    except KeyError:
        pickled = "Not".encode()

    return base64.b64encode(pickled)

@application.route("/get_item_from_storage", methods=["GET"])
def get_item_from_storage():
    uuid = None
    cell_name = None

    try:
        uuid = request.args.getlist("uuid")[0]

    except:
        cell_name = request.args.getlist("cell_name")[0]

    if uuid:
        res = storage_maker.storage.get(uuid=uuid, type_of_work=0)
    else:
        res = storage_maker.storage.get(cell_name=cell_name, type_of_work=1)
    storage_maker.save()
    return res

@application.route("/put_items_to_storage", methods=["POST"])
def put_items_to_storage():
    unbased = base64.b64decode(request.get_data())

    try:
        with open('waybill.xlsx', 'wb') as f:
            f.write(unbased)
    except:
        return "CANNOT BE OPENED"

    wb = WayBill('waybill.xlsx')
    resp = storage_maker.storage.put(way_bill = wb)
    temp_data_from_storage = storage_maker.storage.database_sender.temp_data_storage.get_pair()
    temp_remote_data_from_storage = storage_maker.storage.database_sender.remote_temp_data_storage.get_items()

    print(temp_data_from_storage)
    print(temp_remote_data_from_storage)
    storage_maker.save()
    return resp

if __name__ == '__main__':
    storage_maker = StorageMaker(port=5000, host="127.0.0.1")

    application.run(host="192.168.0.109", port=3000)

    storage_maker.save()