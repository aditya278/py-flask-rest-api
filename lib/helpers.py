import hashlib

class Helpers:
    def __init__(self):
        pass

    def hash_str(self, str):
        res = hashlib.sha1(str.encode())
        return res.hexdigest()