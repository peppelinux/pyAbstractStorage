import importlib

from abstorage.type.list import SimpleList

"""
Expects configuration of the form:

ABS_STORAGE_SQLALCHEMY = dict(
    driver='sqlalchemy',
    url='sqlite:///:memory:',
    params=dict(table='Thing'),
    handler=AbstractStorageSQLAlchemy
)

STORAGE_CONFIG = {
    'class': 'abstorage.type.list.ASList',
    'kwargs': {
        'io_class': 'cryptojwt.serialize.io.JWK_IO',
        'storage_config': ABS_STORAGE_SQLALCHEMY
    }
}

or 

STORAGE_CONFIG = {
    'KeyIssuer': {
        'class': 'abstorage.type.list.ASList',
        'kwargs': {
            'io_class': 'cryptojwt.serialize.io.KeyBundleIO',
            'storage_config': ABS_STORAGE_SQLALCHEMY
        }
    },
    'KeyBundle': {
        'class': 'abstorage.type.list.ASList',
        'kwargs': {
            'io_class': 'cryptojwt.serialize.item.JWK',
            'storage_config': ABS_STORAGE_SQLALCHEMY
        }
    },
    'KeyJar': {
        'class': 'abstorage.type.list.ASList',
        'kwargs': {
            'io_class': 'cryptojwt.serialize.item.KeyJar',
            'storage_config': ABS_STORAGE_SQLALCHEMY
        }
    }

}
"""

def modsplit(name):
    """Split importable"""
    if ':' in name:
        _part = name.split(':')
        if len(_part) != 2:
            raise ValueError("Syntax error: {s}")
        return _part[0], _part[1]

    _part = name.split('.')
    if len(_part) < 2:
        raise ValueError("Syntax error: {s}")

    return '.'.join(_part[:-1]), _part[-1]


def importer(name):
    """Import by name"""
    _part = modsplit(name)
    module = importlib.import_module(_part[0])
    return getattr(module, _part[1])


def create_storage(conf):
    """
    Returns a storage instance.

    :param conf: Configuration
    """
    _name = conf.get("name", "")
    _cls = importer(conf['class'])
    _kwargs = conf['kwargs']
    _io = importer(_kwargs['io_class'])
    return _cls(_kwargs["storage_config"], name=_name, io_class=_io)


def init_storage(storage_conf, class_name):
    if storage_conf is None:
        return SimpleList()
    else:
        _conf = storage_conf.get(class_name)
        if _conf is None:
            if 'class' in storage_conf:
                return create_storage(storage_conf)
            else:
                return SimpleList()
        else:
            return create_storage(_conf)


def qualified_name(cls):
    return cls.__module__ + "." + cls.__name__
