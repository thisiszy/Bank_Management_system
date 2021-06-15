from flask import Flask, jsonify
from flask_cors import CORS
from backend.action import *

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

# @app.route('/books', methods=['GET', 'POST'])
# def all_books():
#     response_object = {'status': 'success'}
#     if request.method == 'POST':
#         post_data = request.get_json()
#         BOOKS.append({
#             'title': post_data.get('title'),
#             'author': post_data.get('author'),
#             'read': post_data.get('read')
#         })
#         response_object['message'] = 'Book added!'
#     else:
#         response_object['books'] = BOOKS
#     return jsonify(response_object)

@app.route('/workers', methods=['GET'])
def allWorkers():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        createWorker({
            'SubName': post_data.get('SubName'),
            'DepartNum': post_data.get('DepartNum'),
            'WorkerID': post_data.get('WorkerID'),
            'WorkerAddr': post_data.get('WorkerAddr'),
            'StartDate': post_data.get('StartDate')
        })
        response_object['message'] = 'Worker added!'
    else:
        workers = getAllWorkerInfo()
        response_object['workers'] = [{ k: str(v) for k, v in item.to_dict().items() } for item in workers]
    return jsonify(response_object)

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


if __name__ == '__main__':
    app.run()