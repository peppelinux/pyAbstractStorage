from typing import List

from cryptojwt.jwk import JWK
from cryptojwt.jwk.jwk import key_from_jwk_dict

from abstorage.base import AbstractStorage
from abstorage.storages.absqlalchemy import AbstractStorageSQLAlchemy


class JWK_IO:
    @staticmethod
    def serialize(key: JWK) -> dict:
        _dict = key.serialize(private=True)
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


class ASList(object):
    def __init__(self, id, storage_conf, io_class=None, value=None):
        self.id = id
        self.storage = AbstractStorage(storage_conf)
        if value:
            self.storage.set(self.id, value)
        self.io = io_class()

    def __len__(self):
        return len(self.storage.get(self.id))

    def __contains__(self, jwk):
        _jwk = jwk.serialize(private=True)
        _jwks = self.storage.get(self.id)
        if _jwk in _jwks:
            return True

    def __del__(self):
        self.storage.__delitem__(self.id)

    def __iter__(self):
        for v in self.storage.get(self.id):
            yield self.io.deserialize(v)

    def __str__(self):
        values = self._get_list()
        return "<JWKList> {}".format(values)

    def append(self, item):
        _list = self._get_list()
        if _list:
            _list.append(item)
            self._update(_list)
        else:
            self.set([item])

    def _get_list(self):
        res = []
        # get returns list of lists, right now
        ll = self.storage.get(self.id)
        for li in ll:
            if isinstance(li, dict):
                res.append(self.io.deserialize(li))
            elif isinstance(li, list):
                for l in li:
                    res.append(self.io.deserialize(l))

        return res

    def _update(self, items):
        value = [self.io.serialize(v) for v in items]
        self.storage.update(self.id, value)

    def extend(self, items):
        _list = self._get_list()
        if _list:
            _list.extend(items)
            self._update(_list)
        else:
            self.set(items)

    def remove(self, item):
        _list = self._get_list()
        if _list:
            _list.remove(item)
            self.storage.update(self.id, _list)

    def copy(self):
        raise NotImplemented()

    def get(self) -> List[JWK]:
        return self._get_list()

    def set(self, items: List[JWK]):
        value = [self.io.serialize(v) for v in items]
        self.storage.set(self.id, value)


if __name__ == "__main__":
    # POC
    from cryptojwt.jwk.rsa import new_rsa_key

    ABS_STORAGE_SQLALCHEMY = dict(
        driver='sqlalchemy',
        url='sqlite:///:memory:',
        params=dict(table='Thing'),
        handler=AbstractStorageSQLAlchemy
    )

    _list = ASList('ciao', ABS_STORAGE_SQLALCHEMY, JWK_IO)

    _rsa1 = new_rsa_key()
    _rsa2 = new_rsa_key()
    _list.append(_rsa1)
    _list.append(_rsa2)
    # should be 2 keys by now
    print('len:', len(_list))
    print('Has key1:', _rsa1 in _list)
    del _list