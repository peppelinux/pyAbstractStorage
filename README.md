pyAbstractStorage
-----------------
This is a POC of a simple Abstract Storage System.
It aim to be general purpose, customizable and easy to be
plugged in existing applications, in particular those who works with dictionaries and shelve serializations.



To start using this POC you have to create or edit these two files:
- `settings.py` - connections urls and handlers definitions
- `db_setup.py` - schemas and utilities related to the database setup
- `pip install sqlalchemy` - it's the RDBMS Object Relational Mapper used in this example
- `git clone $this_repository` - the example files


Create the Schemas defined `db_setup.py`, in the database configured in `settings.py`.
This should be done for RDBMS schemas or ElasticSearch indexes setup,
NoSQL and other kinds of storages should not need to create a specific database:
````
from settings import ABS_STORAGE_SQLALCHEMY

from db_setup import create_database
create_database(ABS_STORAGE_SQLALCHEMY)
````

Usage example
````
from abstorage.base import AbstractStorage  
from settings import ABS_STORAGE_SQLALCHEMY

# that's our database
absdb = AbstractStorage(ABS_STORAGE_SQLALCHEMY)

# put data in it
complex_data = {'agave': 5, 'agamennone': 78, 'ingoalla': 'antani'}
absdb.set('peppe', complex_data)
absdb['emy'] = 'dfsdfdsf'

# get data from it
absdb.get('peppe')
absdb['emy']  

# delete - you can specify the query to match on the column, it returns how many rows have been deleted
absdb.delete('owner', 'peppe')

# delete - like it would have been a dictionary
del(absdb['emy']) 

# put some other data
absdb.set('peppe', complex_data)
absdb.set('emy', ['maradona', 'marulla'])

# get all
absdb()

# len
len(absdb)

# contains
'ciao' in absdb    # false, there's not 'ciao' there !
1 in absdb         # true, 1 is a primary key
'peppe' in absdb   # true, peppe matches in the owner field in the database entries

# __iter__
for i in absdb:
    print(i)
````

Further customizations
----------------------

You should Inherit `AbstractStorage` to add data handlers to have customization from data fetched or saved, from and to a database.
The behaviour explained in the __Usage Example__ can be customized in a AbstractStorage child or in a
customized `asbstorage.storages` class.

Authors
-------

giuseppe.demarco@unical.it


Credits
-------

A friend who calls himself rohe
