import os

class DataHandler:
    def __init__(self):
        self.baseDir = os.path.dirname('./.data/')

    def create(self, folderName, fileName, data):
        filePath = self.baseDir + '/' + folderName + '/' + fileName + '.json'
        
        if os.path.exists(filePath):
            return False
        else:
            with open(filePath, 'w+') as f:
                f.write(data)
                return True
        

    def read(self, folderName, fileName):
        filePath = self.baseDir + '/' + folderName + '/' + fileName + '.json'
        
        if os.path.exists(filePath):
            with open(filePath, 'r') as f:
                f_contents = f.read()
                return f_contents
        else:
            return False

    def update(self, folderName, fileName, data):
        filePath = self.baseDir + '/' + folderName + '/' + fileName + '.json'

        if os.path.exists(filePath):
            with open(filePath, 'w+') as f:
                f.write(data)
                return True
        else:
            return False

    def delete(self, folderName, fileName):
        filePath = self.baseDir + '/' + folderName + '/' + fileName + '.json'

        if os.path.exists(filePath):
            os.remove(filePath)
            return True
        else:
            return False

_data = DataHandler()
_data.create('users', '12345','{ "name" : "Adi", "phone" : "123456" }')
print(_data.read('users', '12345'))
_data.update('users', '12345','{ "name" : "Aditya", "phone" : "123456" }')
print(_data.read('users', '12345'))
# _data.delete('users', '12345')
# print(_data.read('users', '12345'))