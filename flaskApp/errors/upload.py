from flask import jsonify

class InvalidUploadRequestException(Exception):
    status_code = 500
    def __init__(self, message=None, status_code=None):
        Exception.__init__(self)
        if status_code is not None:
            self.status_code = status_code
        if message is None:
            self.message = 'Something went wrong'
        else:
            self.message = message

    def to_dict(self):
        rv = dict()
        rv['message'] = self.message
        return rv
