from jwt import JWT, supported_key_types
from typing import Dict

class WherePasswordException(Exception):
    pass


class DataBase:
    '''From the start database was be a standart list Python'''

    def __init__(self):
        self.base = []
        self.__dic_password = {}



    def add(self, data):
        if 'password' not in data:
            self.base.append(data)
        else:
            self.__dic_password[data['id']] = hash(data.pop('password'))
            self.base.append(data)
        

    def delete(self, data):
        if data in self.base:
            self.base.remove(data)
            return {'Operation': 'DELETE',  'base': self.base}



    def check_validated_password(self, parent_id, password):
        if self.__dic_password[parent_id] == hash(password):
            return True
        return False
        

    def search(self, element_id):
        '''for this moment we keep a data in list, soooo we  must use a O(n) finder'''
        for i, people in enumerate(self.base):
            if people['id'] == element_id and people['role'] == 'Child':
                return self.base.pop(i)
        return {'Error': 404}


    def ___str__(self):
        return self.base