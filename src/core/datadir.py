from os import path
from .files import JsonFile, read_yaml, DATADIR_PATH, CONFIG_PATH


def read_config(what):
    return read_yaml(path.join(CONFIG_PATH, f'{what}.yaml'))


# List of same type items, handles storage I/O
class ItemFile(JsonFile):
    def __init__(self, what, *, readonly = False, on_closed = None):
        super().__init__(path.join(DATADIR_PATH, f'{what}.json'), on_closed)
        if readonly:
            self.file.close()


    def create(self, values, index = None):
        new_values = {k: v for (k, v) in values.items() if v is not None}
        new_values = new_values | { '_id': 0 }

        if len(self.data) != 0:
            new_values['_id'] = max(self.data, key=lambda item: item['_id'])['_id'] + 1

        # we assume self.data is a list that always exists
        if index is None:
            self.data.append(new_values)
        else:
            self.data.insert(index, new_values)

        return new_values['_id']


    def read(self, _id = None):
        if _id is not None:
            try:
                return next((v, i) for i, v in enumerate(self.data) if v['_id'] == _id)
            except StopIteration:
                return None, None

        return self.data, None


    def update(self, _id, values):
        item, _ = self.read(_id)
        if not isinstance(item, dict):
            raise RuntimeError(f'List.udpate() bad id: {_id}')

        for k, v in values.items():
            if type(v) is dict:
                current_value = item.get(k) or {}
                current_value.update(v)
                v = { nk: nv for (nk, nv) in current_value.items() if nv is not None }
           
            item[k] = v
    
    
    def swap(self, _id_a, _id_b):
        _, ia = self.read(_id_a)
        _, ib = self.read(_id_b)
        self.data[ia], self.data[ib] = self.data[ib], self.data[ia]
    
    
    def move(self, _id, destination_index):
        _, current_index = self.read(_id)
        moved = self.data.pop(current_index)
        self.data.insert(destination_index, moved)
    
    
    def delete(self, _id):
        _, index = self.read(_id)
        self.data.pop(index)

