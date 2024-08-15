

class MyExpectation(Exception):
    def __init__(self, status_code, detail, headers):
        self.status_code = status_code
        self.detail = detail
        self.headers = headers
