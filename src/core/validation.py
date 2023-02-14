from .datadir import read_config


def parse_value(name, value, value_type, *, required):
    if value.lower() == 'null':
        value = None

    if required:
        assert value is not None, f'{name} is required'
    
    buildin_types = {
        # date as actual date yyyy-mm-dd
        # array
        # link: text, type/id
        # title: 'each type has:'
        # id:
        # type: number
        # links:
        # type: link
        # multiple: true
        # optional: true
    }

    text_types = ['text', 'text_protected', 'date', 'file', 'html', 'markdown']

    if type(value_type) is list:
        assert value is None or value in value_type, f'{name} must be one of {value_type}, not: {value}'
    elif type(value_type) is dict:
        assert 'map' in value_type, f'unknown type {value_type} for field {name} in config'
        k, v = value.split('=')
        v = parse_value(name, v, value_type['map'], required=required)
        value = {k: v}
    elif value_type == 'number':
        value = int(value)
    elif value_type not in text_types:
        raise RuntimeError(f'{name}: unknown type in config: {value_type}')

    return value


def validated_values(what, values, *, enforce_required):
    config = read_config(what)
    names_to_check = set(values)

    if enforce_required:
        names_to_check.update(config['required'])

    validated = {}

    for name in names_to_check:
        required = name in config['required']
        specs = config['required'] if required else config['optional']

        validated[name] = parse_value(
            name = name,
            value = values[name],
            value_type = specs[name],
            required = required
        )

    return validated
