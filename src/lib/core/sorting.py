from .datadir import read_config


def sort(data, what):
    sort_config = read_config(what).get('sort')
    if sort_config is None:
        return data

    def key(item):
        key_value = 0;
        for field_idx, field_name in enumerate(sort_config):
            values = sort_config[field_name]

            prio = 0
            for value_idx, value in enumerate(values):
                if item[field_name] == value:
                    # we don't substract 1 to handle unmatched values as lowest prio
                    prio = len(values) - value_idx

            prio = prio * ( 10**(len(sort_config)-1-field_idx) )

            key_value += prio 

        _id = item['_id']
        title = item['title']
        # print(f'sorting: key id : {_id:<4} title : {title:<20} :: {key_value}')
        return key_value

    return sorted(data, key=key)
