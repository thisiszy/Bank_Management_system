from flask import Flask, jsonify, make_response, session, redirect, g
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from flask_login import login_user,UserMixin,LoginManager,login_required
from flask_cors import CORS
from backend.action import *
from backend.database import db_session
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

# configuration
DEBUG = True
SECRET_KEY = 'jklklsadhfjkhwbii9/sdf\sdf'

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

from flask import Flask, jsonify, request

currentsub = {}

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.after_request
def after_request(resp):
    resp = make_response(resp)
    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:8080'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    resp.headers['Access-Control-Allow-Headers'] = 'content-type,token'
    return resp

@app.route('/login',methods=['POST'])
def login():
    json = request.get_json()
    if Auth(json['username'], json['password']):
        s = Serializer(SECRET_KEY, expires_in = 600)
        token = s.dumps({ 'username': json['username'] })
        return jsonify({"token": token.decode("utf-8")})
    return "wrong password"

@auth.verify_password
def verify_password(username, pwd):
    token = request.headers.get('token')
    if token is None:
        return None
    s = Serializer(SECRET_KEY)
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None # valid token, but expired
    except BadSignature:
        return None # invalid token
    admin = getAdmin(data['username'])
    if admin is not None:
        g.admin = admin
        return True
    return False

@auth.login_required
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
@auth.login_required
def userLogic():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
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
        users = getUser({
            'ID': request.args.get("ID"),
            'Address': request.args.get("Address"),
            'ContectName': request.args.get("ContectName"),
            'ContectTel': request.args.get("ContectTel"),
            'ContectEmail': request.args.get("ContectEmail"),
            'Relationship': request.args.get("Relationship"),
        })
        response_object['users'] = [{ k: str(v) for k, v in item.to_dict().items() } for item in users]
    return jsonify(response_object)

@app.route('/alteruser', methods=['POST'])
@auth.login_required
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
@auth.login_required
def delUserLogic():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        delUser(post_data.get('ID'))
        response_object['message'] = 'User deleted!'
        return jsonify(response_object)

@app.route('/account', methods=['GET', 'POST'])
@auth.login_required
def accountLogic():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        if post_data.get('type') == "0":
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
@auth.login_required
def delAccountLogic():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        delAccount(post_data.get('AccNum'))
        response_object['message'] = 'Account deleted!'
        return jsonify(response_object)

@app.route('/adduser2acc', methods=['POST'])
@auth.login_required
def addUser2AccLogic():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        addUser2Account(post_data.get('ID'), post_data.get('AccNum'))
        response_object['message'] = 'User added!'
        return jsonify(response_object)

@app.route('/acctype', methods=['GET'])
@auth.login_required
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
@auth.login_required
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

@app.route('/loan', methods=['GET', 'POST'])
@auth.login_required
def loanLogic():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        createLoan({
            'LoanNum': post_data.get('LoanNum'),
            'Budget': post_data.get('Budget'),
            'SubName': post_data.get('SubName'),
        }, 
        post_data.get('ID'))
        response_object['message'] = 'Loan added!'
    else:
        if request.args.get("type") == "0":
            loans = getAllLoan()
            response_object['loans'] = [dict({"Status":getLoanStatus(item.LoanNum), "Paied":getPaied4Loan(item.LoanNum)}, **{ k: str(v) for k, v in item.to_dict().items() }) for item in loans]
        elif request.args.get("type") == "1":
            loans = getLoanByID(request.args.get("content"))
            response_object['loans'] = [dict({"Status":getLoanStatus(item.LoanNum), "Paied":getPaied4Loan(item.LoanNum)}, **{ k: str(v) for k, v in item.to_dict().items() }) for item in loans]
        elif request.args.get("type") == "2":
            loans = getLoanByNum(request.args.get("content"))
            response_object['loans'] = [dict({"Status":getLoanStatus(loans.LoanNum), "Paied":getPaied4Loan(loans.LoanNum)}, **{ k: str(v) for k, v in loans.to_dict().items() })]
        else:
            response_object['message'] = 'get error!'
    return jsonify(response_object)

@app.route('/delloan', methods=['POST'])
@auth.login_required
def delLoanLogic():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        delLoan(post_data.get('LoanNum'))
        response_object['message'] = 'Loan deleted!'
        return jsonify(response_object)

@app.route('/grantloan', methods=['POST'])
@auth.login_required
def grantLoanLogic():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        payForLoan({
            'PayNum': post_data.get('PayNum'),
            'LoanNum': post_data.get('LoanNum'),
            'PayDate': post_data.get('PayDate'),
            'Amount': post_data.get('Amount'),
        })
        response_object['message'] = 'Loan deleted!'
        return jsonify(response_object)


@app.route('/subbranch', methods=['GET'])
@auth.login_required
def getsubLogic():
    global currentsub
    response_object = {'status': 'success'}
    if request.method == 'GET':
        if request.args.get("type") == "0" or request.args.get("content") == "All":
            sub = getAllSub()
            sublist = [item.SubName for item in sub]
            response_object['sub'] = dataStatistic(sublist, request.args.get("start"), request.args.get("end"))
        else:
            response_object['sub'] = dataStatistic([request.args.get("content")], request.args.get("start"), request.args.get("end"))
    return jsonify(response_object)

@app.route('/sublist', methods=['GET'])
@auth.login_required
def getsublistLogic():
    global currentsub
    response_object = {'status': 'success'}
    if request.method == 'GET':
        sub = getAllSub()
        response_object['subbranch'] = []
        currentsub.clear()
        for i in range(len(sub)):
            response_object['subbranch'].append(
                {
                    "id": str(i),
                    "name": sub[i].SubName
                }
            )
            currentsub[i] = sub[i].SubName
    return jsonify(response_object)

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


if __name__ == '__main__':
    app.run()