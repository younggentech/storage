from flask import Flask, render_template

from storage import StorageMaker

application = Flask(__name__)


@application.route('/')
def hello_world():
    return render_template("index.html", storage=storage_maker.storage)


if __name__ == '__main__':
    storage_maker = StorageMaker(port=5000, host="127.0.0.1")

    application.run(host="192.168.0.109", port=3000)
