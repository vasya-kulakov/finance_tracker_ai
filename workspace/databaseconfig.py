KEY = 'ABC'

class DataBase:
    '''From the start database was be a standart list Python'''

    def __init__(self):
        self.base = []
        self.__secret_key = KEY


    @staticmethod
    def create_hash(data):
        return hash(data)

    def add(self, data):
        self.base.append(data)


    def delete(self, data):
        self.base.remove(data)

    def ___str__(self):
        return self.base