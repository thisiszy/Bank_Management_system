import json
from urllib.request import Request
from werkzeug.exceptions import HTTPException

class APIException(HTTPException):
    code = 500
    msg = 'unknown error'
    error_code = 999

    def __init__(self, msg=None, code=None, error_code=None, headers=None):
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if msg:
            self.msg = msg
        super(APIException, self).__init__(msg, None)

    def get_body(self, environ=None):
        body = dict(
            msg=self.msg,
            error_code=self.error_code,
            request=Request.method + ' ' + self.get_url_no_param()
        )
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None):
        """Get a list of headers."""
        return [('Content-Type', 'application/json')]

    @staticmethod
    def get_url_no_param():
        full_path = str(Request.full_path)
        main_path = full_path.split('?')
        return main_path[0]

class DupId(APIException):
    code = 600
    msg = 'duplicated key'
    error_code = 600

class IncompleteData(APIException):
    code = 601
    msg = 'Incomplete data'
    error_code = 601

class NotFind(APIException):
    code = 602
    msg = 'Not find'
    error_code = 602

class Unmodifiable(APIException):
    code = 603
    msg = "Can't modify primary key"
    error_code = 603

class PermissionDenied(APIException):
    code = 604
    msg = "No permission"
    error_code = 604

class UndefindBehaviour(APIException):
    code = 605
    msg = "Undefined Behaviour"
    error_code = 605

class OutOfBound(APIException):
    code = 606
    msg = "Amount out of bound"
    error_code = 606

class UnknownError(APIException):
    code = 607
    msg = "Fetal error"
    error_code = 607