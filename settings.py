from storages.absqlalchemy import AbstractStorageSQLAlchemy


ABS_STORAGE_SQLALCHEMY = dict(
                               driver = 'sqlalchemy',
                               url = 'sqlite:///things.sqlite',
                               params = dict(table='Thing'),
                               handler = AbstractStorageSQLAlchemy
                             )
