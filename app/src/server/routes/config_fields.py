import os
from flask import request, jsonify
from ..app import app
from ...lib.core.files import read_yaml, write_yaml, read_json, write_json, DATADIR_PATH, CONFIG_PATH


@app.route("/config/fields/<what>", methods=['GET'])
def get_config_type_fields(what):
    response = jsonify(read_yaml(CONFIG_PATH)['types'][what]['fields'])
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/config/fields/<what>/<field>", methods=['POST', 'PUT'])
def create_or_set_config_type_field(what, field):
    config = read_yaml(CONFIG_PATH)
    fields_config = config['types'][what]['fields']
    
    new_field = {**request.json} | { "name": field }
    try:
        field_index = next(i for i, fc in enumerate(fields_config) if fc['name'] == field)
        if request.method == 'POST':
            raise ValueError(f'type "{what}" already has field named "{field}"')
        fields_config[field_index] = new_field
    except StopIteration:
        fields_config.append(new_field)

    # todo: "required" spec cheching and updating {what}.json
    # idea: raise an error if name is specified in json but differs from path's <field>
    write_yaml(CONFIG_PATH, config)

    response = jsonify({'response': 'ok (probably)'})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/config/fields/<what>/<field>", methods=['GET'])
def get_config_type_field(what, field):
    fields_config = read_yaml(CONFIG_PATH)['types'][what]['fields']
    response = jsonify(next(fc for fc in fields_config if fc['name'] == field))
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/config/fields/<what>/<field>", methods=['PATCH'])
def update_config_type_field(what, field):
    config = read_yaml(CONFIG_PATH)
    fields_config = config['types'][what]['fields']
    field_index = next(i for i, fc in enumerate(fields_config) if fc['name'] == field)

    args = {**request.json}

    if 'name' in args and args['name'] != field:
        # todo: title should probably have more enforcements like type which must be string
        if field == "title":
            raise ValueError(f'cant rename field "{field}" of type "{what}", because "title" is required')

        new_field_name = args['name']
        try:
            next(i for i, fc in enumerate(fields_config) if fc['name'] == new_field_name)
            raise ValueError(f'cant rename field "{field}" as type "{what}" already has field named "{new_field_name}"')
        except StopIteration:
            pass
        
    fields_config[field_index] = fields_config[field_index] | args
    write_yaml(CONFIG_PATH, config)

    response = jsonify({'response': 'ok (probably)'})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/config/fields/<what>/<field>", methods=['DELETE'])
def delete_config_type_field(what, field):
    if field == "title":
        raise ValueError(f'cant delete field "{field}" of type "{what}", because "title" is required')

    config = read_yaml(CONFIG_PATH)
    fields_config = config['types'][what]['fields']

    try:
        field_index = next(i for i, fc in enumerate(fields_config) if fc['name'] == field)

        data = read_json(os.path.join(DATADIR_PATH, f'{what}.json'))
        for item in data:
            if field in item:
                del item[field]
        write_json(os.path.join(DATADIR_PATH, f'{what}.json'), data)

        del fields_config[field_index]
        write_yaml(CONFIG_PATH, config)
    except StopIteration:
        pass

    response = jsonify({'response': 'ok (probably)'})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response