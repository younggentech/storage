import json
import os
import pickle
import base64
from flask import Flask, render_template, request, redirect, url_for

from get_data_from_csv_xls import WayBill
from remote_data_storage import PDFMaker
from storage import StorageMaker

application = Flask(__name__)
storage_maker = StorageMaker(port=5000, host="127.0.0.1")


@application.route('/')
def hello_world():
    return render_template("index.html", storage=storage_maker.storage)


@application.route('/remote')
def remote_storage():
    if os.path.exists(os.getcwdb().decode() + "/remote_storage_data"):
        with open("remote_storage_data", "rb") as f:
            remote_items = pickle.load(f)
            return render_template("remote.html", items=remote_items, len_of_array=len(remote_items), report=0)
    else:
        with open("remote_storage_data", "wb"):
            return ""


@application.route("/report")
def report(items=[], cells=[]):
    data = render_template("remote.html", items=items,
                           cells=cells, len_of_array=len(items),
                           report=1)
    return data


# routes for bot->

@application.route("/test_conn")
def ok():
    return "OK"


# @application.route("/get_list_of_all_json")
# def get_list_of_all_json():
#     return json.dumps(storage_maker.storage.get_json_data_unique_cells())

# @application.route("/get_remote_json")
# def get_remote_json():
#     final = []
#     with open("remote_storage_data", "rb") as f:
#         __data_from_remote = pickle.load(f)
#     for item in __data_from_remote:
#         final.append(item.__dict__)
#     return json.dumps(final)

@application.route("/get_remote_pickle")
def get_remote_pickle():
    if os.path.exists(os.getcwdb().decode() + "/remote_storage_data"):
        with open("remote_storage_data", "rb") as f:
            remote_items = f.read()
        return base64.b64encode(remote_items)
    else:
        return base64.b64encode(b"")


@application.route("/get_storage_scheme")
def api_scheme():
    storage_maker.storage.render()
    return redirect(url_for('static', filename='img/scheme.png'))


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
    resp = storage_maker.storage.put(way_bill=wb)
    temp_data_from_storage = storage_maker.storage.database_sender.temp_data_storage.get_pair()
    temp_remote_data_from_storage = storage_maker.storage.database_sender.remote_temp_data_storage.get_items()

    _pdf_main = 0
    _pdf_remote = 0
    if temp_data_from_storage:
        _pdf_main = 1
        temp_data_for_report = report(items=temp_data_from_storage[0], cells=temp_data_from_storage[1])
        _pdf_for_main = PDFMaker(name_output="report storage.pdf", html=temp_data_for_report)
        _pdf_for_main.make_pdf()
        os.rename("/Users/ovsannikovaleksandr/Desktop/предпроф/back/report storage.pdf",
                  "/Users/ovsannikovaleksandr/Desktop/предпроф/back/static/pdf/report storage.pdf")
    if temp_remote_data_from_storage:
        _pdf_remote = 1
        temp_remote_data_for_report = report(items=temp_remote_data_from_storage)
        _pdf_for_remote = PDFMaker(name_output="report remote storage.pdf", html=temp_remote_data_for_report)
        _pdf_for_remote.make_pdf()
        os.rename("/Users/ovsannikovaleksandr/Desktop/предпроф/back/report remote storage.pdf",
                  "/Users/ovsannikovaleksandr/Desktop/предпроф/back/static/pdf/report remote storage.pdf")

    storage_maker.save()
    return resp + "." + str(_pdf_main) + "." + str(_pdf_remote)


@application.route("/get_pdf_main")
def api_main_pdf():
    return redirect(url_for('static', filename="pdf/report storage.pdf"))


@application.route("/get_pdf_remote")
def api_remote_pdf():
    return redirect(url_for('static', filename="pdf/report remote storage.pdf"))


if __name__ == '__main__':
    application.run(host="192.168.0.109", port=3000)
