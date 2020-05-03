class AbstractStorage(object):
    """
    An AbsractStorage that take a storage engine and offer a standard set
    of methods and I/O to data.
    """
    def __init__(self, conf_dict):
        self.storage = conf_dict['handler'](conf_dict)
    
    def get(self, k):
        return self.storage.get(k)

    def set(self, k, v):
        return self.storage.set(k, v)

    def update(self, k, v):
        return self.storage.update(k, v)

    def delete(self, k, v):
        return self.storage.delete(v, k=k)

    def __getitem__(self, k):
        return self.storage.get(k)

    def __setitem__(self, k, v):
        return self.storage.set(k, v)

    def __delitem__(self, v):
        return self.storage.delete(v)

    def __call__(self):
        return self.storage() 

    def __repr__(self):
        return self.__str__() 
    
    def __len__(self):
        return len(self.storage())

    def __contains__(self, k):
        return self.storage.__contains__(k)

    def __str__(self):
        return self.storage.__str__()

    def __iter__(self):
        return iter(self.storage.__iter__())

    def flush(self):
        return self.storage.flush()
