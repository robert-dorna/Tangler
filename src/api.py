from os import path
from .core.sorting import sort
from .core.files import JsonFile, read_json, DATADIR_PATH
from .core.datadir import ItemFile


LINKS_PATH = path.join(DATADIR_PATH, '_links.json')


class Api:
    def __init__(self):
        self.cache = {}
        self.links = None

    def refresh(self, what):
        data = read_json(path.join(DATADIR_PATH, f'{what}.json'))
        self.cache[what] = data
        return data

    def get(self, what):
        if what in self.cache:
            return sort(self.cache[what], what)

        return sort(self.refresh(what), what)

    def _prepend_refresh(self, what, on_closed):
        def prepended_refresh(_=None):
            self.refresh(what)
            if on_closed:
                on_closed()
        return prepended_refresh

    def create(self, what, values, index=None, *, on_closed=None):
        on_closed = self._prepend_refresh(what, on_closed)
        with ItemFile(what, on_closed=on_closed) as items:
            new_id = items.create(values, index)
        return new_id

    def read(self, what, _id=None):
        data = self.get(what)
        if _id is None:
            result = [item | {'_what': what} for item in sort(data, what)]
            return result, None

        try:
            i, item = next((i, item)
                           for i, item in enumerate(data) if item['_id'] == _id)
            return i, item | {'_what': what}
        except StopIteration:
            raise KeyError(f'cannot find item of type "{what}" with _id {_id}')

    def readall(self, what, _id=None):
        if _id is None:
            data = self.parentless(what)
            data = sort(data, what)
            for i, item in enumerate(data):
                item['_index'] = i
                item['_what'] = what
                item['_children'] = [
                    self.readall(
                        what=l['to']['what'],
                        _id=int(l['to']['_id'])
                    ) for l in self.children(what, item['_id'])
                ]
            return data

        i, item = self.read(what, _id)
        item['_index'] = i
        item['_what'] = what
        item['_children'] = [
            self.readall(
                what=l['to']['what'],
                _id=int(l['to']['_id'])
            ) for l in self.children(what, _id)
        ]
        return item

    def update(self, what, _id, values, *, on_closed=None):
        on_closed = self._prepend_refresh(what, on_closed)
        with ItemFile(what, on_closed=on_closed) as data:
            data.update(_id, values)

    def swap(self, what, _id_a, _id_b, *, on_closed=None):
        on_closed = self._prepend_refresh(what, on_closed)
        with ItemFile(what, on_closed=on_closed) as items:
            items.swap(_id_a, _id_b)

    def move(self, what, _id, destination_index, *, on_closed=None):
        on_closed = self._prepend_refresh(what, on_closed)
        with ItemFile(what, on_closed=on_closed) as items:
            items.move(_id, destination_index)

    def delete(self, what, _id, *, on_closed=None):
        on_closed = self._prepend_refresh(what, on_closed)

        fr = {'what': what, '_id': _id}

        parent_data = self.parent(what, _id)
        if parent_data is not None:
            link_index, parent = parent_data

            self.read_links()
            self.links.pop(link_index)

            for link in self.links:
                if link['from'] == fr:
                    link['from'] = { 'what': parent['_what'], '_id': parent['_id'] }
            
            self.write_links()


        self.read_links()
        self.links = [link for link in self.links if link['from'] != fr]
        self.write_links()

        with ItemFile(what, on_closed=on_closed) as items:
            items.delete(_id)

    def read_links(self):
        self.links = read_json(LINKS_PATH)

    def write_links(self):
        with JsonFile(LINKS_PATH) as file:
            file.data = self.links

    def children(self, what, _id):
        if self.links is None:
            self.read_links()

        fr = {'what': what, '_id': _id}
        return [link for link in self.links if link['from'] == fr]

    def parentless(self, what):
        if self.links is None:
            self.read_links()

        def has_parent(item):
            to = {'what': what, '_id': item['_id']}
            try:
                next(None for link in self.links if link['to'] == to)
                return True
            except:
                return False

        data = self.get(what)
        return [item for item in data if not has_parent(item)]

    def parent(self, what, _id):
        if self.links is None:
            self.read_links()

        to = {'what': what, '_id': _id}
        try:
            i, link = next((i, v)
                           for i, v in enumerate(self.links) if v['to'] == to)
            _, parent = self.read(link['from']['what'], link['from']['_id'])
            return i, parent
        except StopIteration:
            return None

    def link(self, from_what, from_id, to_what, to_id, index=None):
        # TODO: recursion check & prevention mechanism
        self.read_links()
        new_link = {
            'from': {'what': from_what, '_id': from_id},
            'to': {'what': to_what, '_id': to_id},
        }
        try:
            next(None for link in self.links if link == new_link)
            print('link already exists, skipping')
        except StopIteration:
            if index is None:
                self.links.append(new_link)
            else:
                self.links.insert(index, new_link)
            self.write_links()

    def unlink(self, from_what, from_id, to_what, to_id):
        self.read_links()
        target_link = {
            'from': {'what': from_what, '_id': from_id},
            'to': {'what': to_what, '_id': to_id},
        }
        try:
            i = next(i for i, link in enumerate(
                self.links) if link == target_link)
            self.links.pop(i)
            self.write_links()
        except StopIteration:
            print('link does not exist, skipping')
