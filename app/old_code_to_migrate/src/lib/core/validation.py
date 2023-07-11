from .files import read_yaml, CONFIG_PATH


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

    text_types = ['text', 'text_protected', 'date', 'file', 'html', 'markdown', 'any']

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
    config = read_yaml(CONFIG_PATH)['types'][what]
    fields = {field['name']: field for field in config['fields']}

    names_to_check = set(values)

    if enforce_required:
        names_to_check.update([name for name, spec in fields.items() if spec['required']])

    validated = {}

    for name in names_to_check:
        value_type = fields[name]['values']

        validated[name] = parse_value(
            name = name,
            value = values[name],
            value_type = list(value_type) if type(value_type) is dict else value_type,
            required = fields[name]['required'] 
        )

    return validated
