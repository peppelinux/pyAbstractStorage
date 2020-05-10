from uuid import uuid4

from abstorage.base import AbstractStorage
from abstorage.storages.absqlalchemy import AbstractStorageSQLAlchemy

class SimpleList():
    def __init__(self, value=None):
        if value is None:
            self.db = []
        else:
            self.set(value)

    def __len__(self):
        return len(self.db)

    def __contains__(self, item):
        return item in self.db

    def __del__(self):
        del self.db

    def __iter__(self):
        for i in self.db:
            yield i

    def __str__(self):
        return str(self.db)

    def append(self, item):
        self.db.append(item)

    def extend(self, items):
        self.db.extend(items)

    def remove(self, item):
        self.db.remove(item)

    def get(self):
        return self.db

    def set(self, value):
        if isinstance(value, list):
            self.db = value
        else:
            raise ValueError("Wrong value type")

    def copy(self):
        return SimpleList(self.db[:])

    def close(self):
        return


class ASList(object):
    def __init__(self, storage_conf, name='', io_class=None, value=None):
        self.name = name or str(uuid4())
        self.storage = AbstractStorage(storage_conf)
        self._conf = storage_conf
        if value:
            self.storage.set(self.name, value)
        self.io = io_class()

    def __len__(self):
        return len(self.storage.get(self.name))

    def __contains__(self, jwk):
        _jwk = jwk.serialize(private=True)
        _jwks = self.storage.get(self.name)
        if _jwk in _jwks:
            return True

    def __del__(self):
        self.storage.__delitem__(self.name)

    def __iter__(self):
        for v in self.storage.get(self.name):
            yield self.io.deserialize(v)

    def __str__(self):
        values = self._get_list()
        return "<JWKList> {}".format(values)

    def append(self, item):
        _list = self._get_list()
        if _list is None:
            self.set([item])
        else:
            _list.append(item)
            self._update(_list)

    def _get_list(self):
        res = []
        # get returns list of lists, right now
        ll = self.storage.get(self.name)
        for li in ll:
            if isinstance(li, dict):
                res.append(self.io.deserialize(li))
            elif isinstance(li, list):
                for l in li:
                    res.append(self.io.deserialize(l))

        return res

    def _update(self, items):
        value = [self.io.serialize(v) for v in items]
        del self.storage[self.name]
        self.storage.set(self.name, value)

    def extend(self, items):
        _list = self._get_list()
        if _list is None:
            self.set(items)
        else:
            _list.extend(items)
            self._update(_list)

    def remove(self, item):
        _list = self._get_list()
        if _list:
            _list.remove(item)
            self._update(_list)

    def copy(self):
        _new = ASList(self._conf, io_class=self.io.__class__)
        _new.set(self.get())
        return _new

    def get(self):
        return self._get_list()

    def set(self, items):
        value = [self.io.serialize(v) for v in items]
        if self.storage.get(self.name):
            del self.storage[self.name]

        self.storage.set(self.name, value)


if __name__ == "__main__":
    # POC
    from cryptojwt.jwk.rsa import new_rsa_key

    ABS_STORAGE_SQLALCHEMY = dict(
        driver='sqlalchemy',
        url='sqlite:///:memory:',
        params=dict(table='Thing'),
        handler=AbstractStorageSQLAlchemy
    )

    _list = ASList(ABS_STORAGE_SQLALCHEMY, io_class=JWK_IO)

    _rsa1 = new_rsa_key()
    _rsa2 = new_rsa_key()
    _list.append(_rsa1)
    _list.append(_rsa2)
    # should be 2 keys by now
    print('len:', len(_list))
    print('Has key1:', _rsa1 in _list)
    del _list
