import os
from flask import request, jsonify
from ...lib.core.files import read_yaml, write_yaml, read_json, write_json, DATADIR_PATH, CONFIG_PATH


def config_read_request_handler():
    display = read_yaml(CONFIG_PATH)
    response = jsonify(display)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


def config_patch_request_handler():
    config = read_yaml(CONFIG_PATH)

    args = {**request.json}

    target = args['target']

    if target == "order":
        new_value = args['new_value']
        config['order'] = new_value
        write_yaml(CONFIG_PATH, config)
        response = jsonify({'response': 'ok (probably)'})

    elif target == "name":
        old_name = args['type_name']
        new_name = args['new_value']['name']
        new_emoji = args['new_value'].get('emoji')

        if new_name in config['types']:
            raise ValueError(f'new item type name: {new_name} is already taken')

        config['order'] = [new_name if type_name == old_name else type_name for type_name in config['order']]
        config['types'][new_name] = config['types'][old_name]
        if new_emoji:
            config['types'][new_name]['emoji'] = new_emoji

        del config['types'][old_name]
        os.rename(
            os.path.join(DATADIR_PATH, f'{old_name}.json'),
            os.path.join(DATADIR_PATH, f'{new_name}.json')
        )
        write_yaml(CONFIG_PATH, config)

        links = read_json(os.path.join(DATADIR_PATH, '_links.json'))
        for link in links:
            for key in ['from', 'to']:
                if link[key]['what'] == old_name:
                    link[key]['what'] = new_name

        write_json(os.path.join(DATADIR_PATH, '_links.json'), links)

        response = jsonify({'response': 'ok (probably)'})

    elif target in ["emoji", "fields", "field"]:
        type_config = config['types'][args['type_name']]
        new_value = args['new_value']

        if target == "field":
            field_name = args['field_name']
            i = next(i for i, field in enumerate(type_config['fields']) if field['name'] == field_name)
            type_config['fields'][i] = new_value
        else:
            type_config[target] = new_value

        write_yaml(CONFIG_PATH, config)

        response = jsonify({'response': 'ok (probably)'})

    else:
        response = jsonify({'response': 'error', 'message': f'unsupported target: {target}'})

    response.headers.add("Access-Control-Allow-Origin", "*")
    return response