class DataBase:
    '''From the start database was be a standart list Python'''

    def __init__(self):
        self.base = []


    @staticmethod
    def create_hash(data):
        return hash(data)

    def add(self, data):
        self.base.append(data)


    def delete(self, data):
        self.base.remove(data)

    def ___repr__(self):
        return self.base