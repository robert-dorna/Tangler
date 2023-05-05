from flask import request, jsonify
from ...lib.core.files import read_yaml, write_yaml, CONFIG_PATH


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
        response = jsonify({'response': 'error', 'message': 'target "order" is not supported yet (will be)'})
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