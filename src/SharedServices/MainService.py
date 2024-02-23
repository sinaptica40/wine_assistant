import datetime
import enum
import json
import os
import re
from flask import Response, request


class StatusType(enum.Enum):
    success = "SUCCESS"
    fail = "FAIL"
    error = "ERROR"

def errorResponse(statusCode, message):
    response = json.dumps({
        'status': 'error',
        'message': message
    })
    return Response(mimetype="application/json", response=response, status=statusCode)


class CustomError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class MainService:
    def __init__(self):
        pass
        
    @staticmethod
    def getDateTimeNow():
        return datetime.datetime.now()
        
    # Create response data
    @classmethod
    def responseModel(cls, values):
        if values.get('status') == StatusType.error.value:
            msg = cls.__setErrorMessages(values.get('data', ''))
            response = {
                "status": values.get('status', ''),
                "data": dict(),
                "message": msg,
                "errors": values.get('data', '')
            }
        else:
            try:
                data = json.loads(values.get('data', ''))
            except Exception as e:
                if type(values.get('data', '')) == dict:
                    data = values.get('data', '')
                else:
                    data = dict()
            response = {
                "status": values.get('status', ''),
                "data": data,
                "message": values.get('message', '')
            }
        response = json.dumps(response)
        return response
        
    # Response method
    @classmethod
    def response(cls, data, status_code):
        """
        Custom Response Function
        """
        response = cls.responseModel(data)
        return Response(
            mimetype="application/json",
            response=response,
            status=status_code
        )

    # Error message create
    @staticmethod
    def __setErrorMessages(data):
        message = ""
        for k, v in data.items():
            if message:
                message = str(message) + str(', ') + str(v)
            else:
                message = str(v)
        return message
