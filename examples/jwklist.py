from typing import List

from abstorage.base import AbstractStorage
from settings import ABS_STORAGE_SQLALCHEMY

from cryptojwt.jwk import JWK
from cryptojwt.jwk.jwk import key_from_jwk_dict
from cryptojwt.jwk.rsa import new_rsa_key


class JWK_IO:
    @staticmethod
    def serialize(key: JWK) -> dict:
        _dict = key.serialize()
        inactive = key.inactive_since
        if inactive:
            _dict['inactive_since'] = inactive
        return _dict

    @staticmethod
    def deserialize(jwk: dict) -> JWK:
        k = key_from_jwk_dict(jwk)
        inactive = jwk.get("inactive_since", 0)
        if inactive:
            k.inactive_since = inactive
        return k


class JWKList(AbstractStorage):
    def __init__(self, storage_conf, name=None, value=None):
        super().__init__(storage_conf)
        # deprecate this: the storage will be the handler of all the entries, all the ids, like a dictionary
        # self.id = name
        if name and value:
            self.storage.set(name, value)
        self.io = JWK_IO()

    # this has been inherited as it is
    #def __len__(self):
        #self.storage.__len__()

    def __contains__(self, jwk):
        _jwk = jwk.io.serialize(private=True)
        _jwks = self.get(self.id)
        return (_jwk in _jwks)

    def __iter__(self):
        for v in self.get(self.id):
            yield self.io.deserialize(v)

    def __str__(self):
        return "<JWKList> {}".format(self.__call__())

    # DELETE or UPDATE here ...
    #def remove(self, item):
        #_list = self._get_list()
        #_list.remove(item)
        #self.set(_list)

    def delete(self, name_id):
        return self.storage.delete(name_id, k='owner')

    def get(self, name_id) -> List[JWK]:
        return [self.io.deserialize(i) for i in self.storage.get(name_id)]

    def _data_to_db(self, data):
        if isinstance(data, list):
            value = [self.io.serialize(i) for i in data]
        else:
            value = self.io.serialize(data)
        return value

    def set(self, name, items: List[JWK]):
        value = self._data_to_db(items)
        pre = self.storage.get(name)
        if pre:
            self.storage.update(name, value)
        else:
            self.storage.set(name, value)

    def append(self, name_id, item):
        _list = self.storage.get(name_id)
        if _list:
            _list.append(self._data_to_db(item))
            self.update(name_id, _list)
        else:
            self.set(name_id, item)

    # is it needed?
    #def extend(self, name_id, items):
        #_list = self.storage.get(name_id)
        #_list.extend(name_id, items)
        #self.update(name_id, _list)

    def copy(self):
        raise NotImplemented()


# POC
_list = JWKList(ABS_STORAGE_SQLALCHEMY)

_list.set('ciao', new_rsa_key())
_list

_list.append('ciao', new_rsa_key())
_list

_list.delete('ciao')
