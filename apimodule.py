# This is a sample Python script.

import logging
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from typing import TypeVar

import jproperties as jproperties
from flask import Flask, jsonify
import testmodule
from dbmodule import Task
from daomodule import Dao

app = Flask(__name__)
offers = [
    {
        'id': 1,
        'name': 'offer 1'
    },
    {
        'id': 2,
        'name': 'offer 2'
    }
]

# logging to file
logging.basicConfig(filename='tutorial.log', format='%(asctime)s %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# properties configuration aplication
config = jproperties.Properties()
with open('app-config.properties', 'rb') as config_file:
    config.load(config_file)
    logging.info("app-config.properties loaded")


# API (flask,jprop,docs) data-> wlasciwosc properties w celu pobrania wartosci data
@app.route(config.get('api-path').data + '/offers', methods=['GET'])
def get_offers():
    logging.info("get_offers invoked")
    return jsonify({'offers': offers})


@app.route(config.get('api-path').data + '/fake-create', methods=['GET'])
def get_fake_create():
    logging.info("fake-create invoked")
    dao = Dao[Task]()
    # dao.create(Task(id=50))
    dao.update(Task(id=50, population_processed_failed=1))
    return jsonify({'offers': offers})


@app.route(config.get('api-path').data + '/ext-loader', methods=['GET'])
def perform_external_function():
    logging.info("perform_external_function invoked")
    getattr(testmodule, config.get('ext.function-name').data)('test_message')
    return jsonify({'function-name': config.get('ext.function-name').data})


# możliwosć przekazania nazwy funkcji którą chce się wykonać
# request param (http://localhost:5000/tutorial/api/v2/ext-loader?func-name=func_1) /
# path param (http://localhost:5000/tutorial/api/v2/ext-loader/func_1)
def perform_external_function_with_param():
    pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)
