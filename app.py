from flask import Flask, jsonify
from flask_cors import CORS
from backend.action import *
from backend.database import db_session

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

from flask import Flask, jsonify, request

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/workers', methods=['GET'])
def allWorkers():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        # createWorker({
        #     'SubName': post_data.get('SubName'),
        #     'DepartNum': post_data.get('DepartNum'),
        #     'WorkerID': post_data.get('WorkerID'),
        #     'WorkerAddr': post_data.get('WorkerAddr'),
        #     'StartDate': post_data.get('StartDate')
        # })
        response_object['message'] = 'Worker added!'
    else:
        workers = getAllWorkerInfo()
        response_object['workers'] = [{ k: str(v) for k, v in item.to_dict().items() } for item in workers]
    return jsonify(response_object)

@app.route('/user', methods=['GET', 'POST'])
def userLogic():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        print(post_data)
        createUser({
            'ID': post_data.get('ID'),
            'Address': post_data.get('Address'),
            'ContectName': post_data.get('ContectName'),
            'ContectTel': post_data.get('ContectTel'),
            'ContectEmail': post_data.get('ContectEmail'),
            'Relationship': post_data.get('Relationship'),
        })
        response_object['message'] = 'User added!'
    else:
        users = getAllUser()
        response_object['users'] = [{ k: str(v) for k, v in item.to_dict().items() } for item in users]
        print(response_object['users'])
    return jsonify(response_object)

@app.route('/deluser', methods=['POST'])
def delUserLogic():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        delUser(post_data.get('ID'))
        response_object['message'] = 'User deleted!'
        return jsonify(response_object)

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


if __name__ == '__main__':
    app.run()