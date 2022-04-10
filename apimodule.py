# This is a sample Python script.
import concurrent.futures
import json
import logging
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import threading
import time
from _ast import arg
from datetime import date
from types import SimpleNamespace
from typing import TypeVar

import jproperties as jproperties
from django.db.migrations import executor
from flask import Flask, jsonify, request, render_template, session
from werkzeug.utils import redirect

import dbmodule
import testmodule
from dbmodule import Task
from daomodule import Dao

app = Flask(__name__)
app.secret_key = 'mysecretkey'

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


@app.route(config.get('api-path').data + '/task', methods=['POST'])
def save_task():
    request_data = request.json
    name = request_data['name']
    logging.info(name)
    logging.info(str(request_data).replace('\'', '\"'))
    task = json.loads(str(request_data).replace('\'', '\"'), object_hook=lambda o: SimpleNamespace(**o))
    logging.info(task.name + " " + task.surname)
    return 'Response'


@app.route(config.get('api-path').data + '/fake-create', methods=['GET'])
def get_fake_create():
    logging.info("fake-create invoked")
    dao = Dao[Task]()
    # dao.create(Task(id=50))
    dao.update(Task(id=50, population_processed_failed=1))
    return jsonify({'offers': offers})


@app.route(config.get('api-path').data + '/ext-loader', methods=['GET'])
def perform_external_function():
    task_back = threading.Thread(target=back_thread)
    task_back.start()
    # getattr(testmodule, config.get('ext.function-name').data)('test_message')
    return jsonify({'function-name': config.get('ext.function-name').data})


@app.route(config.get('api-path').data + '/proc-loader', methods=['POST'])
def perform_proc_function():
    logging.info("perform_process_function invoked")
    task_name = request.form["taskName"]
    task_param = request.form["taskParam"]

    task = dbmodule.Task(creation_date=date.today().strftime("%d.%m.%Y"), population_size=1, name=task_name)
    dbmodule.session.add(task)
    dbmodule.session.commit()

    # with concurrent.futures.ThreadPoolExecutor(max_workers=config.get('app.max.workers')) as executor:
    task_th = threading.Thread(target=task_thread, args=(task_name, task_param,))
    task_th.start()
    # getattr(testmodule, config.get('ext.function-name').data)('test_message')
    return redirect('/dashboard')


def task_thread(task_name, task_param):
    while True:
        time.sleep(3)
        logging.info(task_name + "(" + task_param + ") started...")
        threading.Thread(getattr(testmodule, task_name)(task_param)).start()
        # threading.Thread(getattr(testmodule, config.get('ext.function-name').data)(task_name)).start()


def back_thread():
    while True:
        time.sleep(3)
        print('main')


# możliwosć przekazania nazwy funkcji którą chce się wykonać
# request param (http://localhost:5000/tutorial/api/v2/ext-loader?func-name=func_1) /
# path param (http://localhost:5000/tutorial/api/v2/ext-loader/func_1)
def perform_external_function_with_param():
    pass


@app.route('/login/credentials', methods=['POST'])
def login():
    e_mail = request.form["email"]
    password = request.form["password"]

    user = dbmodule.session.query(dbmodule.User.e_mail).filter_by(e_mail=e_mail).first()

    if user is not None:
        password = dbmodule.session.query(dbmodule.User).filter_by(e_mail=e_mail).first().password
        if password:
            session.clear()
            session["e_mail"] = e_mail
            return redirect('/dashboard')
    return redirect('/login?error')


@app.route('/register/credentials', methods=['POST'])
def register():
    e_mail = request.form["email"]
    password = request.form["password"]

    user = dbmodule.session.query(dbmodule.User.e_mail).filter_by(e_mail=e_mail).first()

    if user is None:
        user = dbmodule.User(e_mail, password)
        dbmodule.session.add(user)
        dbmodule.session.commit()
        password = dbmodule.session.query(dbmodule.User).filter_by(e_mail=e_mail).first().password
        if password:
            session.clear()
            session["e_mail"] = e_mail
            return redirect('/login')
    return redirect('/login?error')


@app.route('/login', methods=['GET'])
def display_login():
    return render_template('index.html')


@app.route('/register', methods=['GET'])
def display_register():
    return render_template('register.html')


@app.route('/dashboard', methods=['GET'])
def display_dashboard():
    lists = dbmodule.session.query(Task).all()
    return render_template('dashboard.html', lists=lists)


@app.route('/form', methods=['GET'])
def display_form():
    return render_template('form.html')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)
