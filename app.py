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
        if request.args.get("type") == "0":
            users = getAllUser()
            response_object['users'] = [{ k: str(v) for k, v in item.to_dict().items() } for item in users]
        elif request.args.get("type") == "1":
            users = getUserByID(request.args.get("content"))
            if users is not None:
                response_object['users'] = [{ k: str(v) for k, v in item.to_dict().items() } for item in users]
        elif request.args.get("type") == "2":
            users = getUserByAccount(request.args.get("content"))
            if users is not None:
                response_object['users'] = [{ k: str(v) for k, v in item.to_dict().items() } for item in users]
        else:
            response_object['message'] = 'get error!'
    return jsonify(response_object)

@app.route('/alteruser', methods=['POST'])
def userAlterLogic():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        alterUser(
            post_data.get('ID'),
            {
            'ID': post_data.get('ID'),
            'Address': post_data.get('Address'),
            'ContectName': post_data.get('ContectName'),
            'ContectTel': post_data.get('ContectTel'),
            'ContectEmail': post_data.get('ContectEmail'),
            'Relationship': post_data.get('Relationship'),
            }
        )
        response_object['message'] = 'User altered!'
        return jsonify(response_object)

@app.route('/deluser', methods=['POST'])
def delUserLogic():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        delUser(post_data.get('ID'))
        response_object['message'] = 'User deleted!'
        return jsonify(response_object)

@app.route('/account', methods=['GET', 'POST'])
def accountLogic():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        if post_data.get('type') == "0":
            print(post_data)
            createAccount(
                'Saving',
                {
                'AccNum': post_data.get('AccNum'),
                'ID': post_data.get('ID'),
                'Balance': post_data.get('Balance'),
                'OpenDate': post_data.get('OpenDate'),
                'SubName': post_data.get('SubName'),
                'Rate': post_data.get('Rate'),
                'CurrencyType': post_data.get('CurrencyType'),
                })
        elif post_data.get('type') == "1":
            createAccount(
                'Checking',
                {
                'AccNum': post_data.get('AccNum'),
                'ID': post_data.get('ID'),
                'Balance': post_data.get('Balance'),
                'OpenDate': post_data.get('OpenDate'),
                'SubName': post_data.get('SubName'),
                'Overdraft': post_data.get('Overdraft'),
                })
        else:
            response_object['message'] = 'Add failed!'
    else:
        if request.args.get("type") == "0":
            accounts = getAllAccount()
            response_object['accounts'] = []
            for bound in accounts:
                temp = {k: str(v) for k, v in bound[0].to_dict().items()}
                temp = dict({k: str(v) for k, v in bound[1].to_dict().items()}, **temp )
                response_object['accounts'].append(temp)
        elif request.args.get("type") == "2":
            accounts = getAccountByID(request.args.get("content"))
            response_object['accounts'] = []
            for bound in accounts:
                temp = {k: str(v) for k, v in bound[0].to_dict().items()}
                temp = dict({k: str(v) for k, v in bound[1].to_dict().items()}, **temp )
                temp = dict({k: str(v) for k, v in bound[2].to_dict().items()}, **temp )
                response_object['accounts'].append(temp)
        elif request.args.get("type") == "1":
            accounts = getAccountBySub(request.args.get("content"))
            response_object['accounts'] = [request.args.get("content")]
            for bound in accounts:
                temp = {k: str(v) for k, v in bound[0].to_dict().items()}
                temp = dict({k: str(v) for k, v in bound[1].to_dict().items()}, **temp )
                temp = dict({k: str(v) for k, v in bound[2].to_dict().items()}, **temp )
                response_object['accounts'].append(temp)
        else:
            response_object['message'] = 'get error!'
    return jsonify(response_object)

@app.route('/delacc', methods=['POST'])
def delAccountLogic():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        delAccount(post_data.get('AccNum'))
        response_object['message'] = 'Account deleted!'
        return jsonify(response_object)

@app.route('/adduser2acc', methods=['POST'])
def addUser2AccLogic():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        addUser2Account(post_data.get('ID'), post_data.get('AccNum'))
        response_object['message'] = 'User added!'
        return jsonify(response_object)

@app.route('/acctype', methods=['GET'])
def accountTypeLogic():
    response_object = {'status': 'success'}
    if request.method == 'GET':
        type = getAccountType(request.args.get("AccNum"))
        if type == 'Checking':
            response_object['acctype'] = '1'
        elif type == 'Saving':
            response_object['acctype'] = '0'
        return jsonify(response_object)

@app.route('/alteracc', methods=['POST'])
def accAlterLogic():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        alterAccount(
            post_data.get('AccNum'),
            {
            'AccNum': post_data.get('AccNum'),
            'Balance': post_data.get('Balance'),
            'LastAccessTime': post_data.get('LastAccessTime'),
            'Rate': post_data.get('Rate'),
            'CurrencyType': post_data.get('CurrencyType'),
            'Overdraft': post_data.get('Overdraft'),
            }
        )
        response_object['message'] = 'Account altered!'
        return jsonify(response_object)

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


if __name__ == '__main__':
    app.run()