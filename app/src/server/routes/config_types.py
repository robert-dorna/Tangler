import os
from flask import request, jsonify
from ..app import app
from ...lib.core.files import read_yaml, write_yaml, read_json, write_json, DATADIR_PATH, CONFIG_PATH


LINKS_FILE_PATH = os.path.join(DATADIR_PATH, '_links.json')


# not sure if POST by some convention should not have <what> (new resource name) in URL but in params instead
@app.route("/config/types/<what>", methods=['POST', 'PUT'])
def create_or_set_config_type(what):
    config = read_yaml(CONFIG_PATH)
    if what in config['types']:
        if request.method == 'POST':
            raise ValueError(f'type {what} already exists')
    else:
        data_file_path = os.path.join(DATADIR_PATH, f'{what}.json')
        if not os.path.exists(data_file_path):
            write_json(data_file_path, [])

        config['order'].append(what)

    config['types'][what] = {**request.json}
    write_yaml(CONFIG_PATH, config)

    response = jsonify({'response': 'ok (probably)'})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/config/types/<what>", methods=['GET'])
def get_config_type(what):
    response = jsonify(read_yaml(CONFIG_PATH)['types'][what])
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/config/types/<what>", methods=['PATCH'])
def update_config_type(what):
    args = {**request.json}

    config = read_yaml(CONFIG_PATH)
    if what not in config['types']:
      raise ValueError(f'type {what} does not exist')

    if '_name' in args:
        new_name = args.pop('_name')
        if new_name != what:
            if new_name in config['types']:
                raise ValueError(f'rename of "{what}" failed because new name "{new_name}" already exists')

            config['order'] = [new_name if type_name == what else type_name for type_name in config['order']]

            # todo: this entire set of not atomic operations is very bad and error prone
            os.rename(
                os.path.join(DATADIR_PATH, f'{what}.json'),
                os.path.join(DATADIR_PATH, f'{new_name}.json')
            )

            # e.g. an error here (lets say permission denied) will result in partial resource rename and maybe "unrecoverable" (conveniently) state
            links = read_json(LINKS_FILE_PATH)
            for link in links:
                for key in ['from', 'to']:
                    if link[key]['what'] == what:
                        link[key]['what'] = new_name

            write_json(LINKS_FILE_PATH, links)

            config['types'][new_name] = config['types'][what]
            del config['types'][what]
            what = new_name

    config['types'][what] = config['types'][what] | args
    write_yaml(CONFIG_PATH, config)

    response = jsonify({'response': 'ok (probably)'})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/config/types/<what>", methods=['DELETE'])
def delete_config_type(what):
    config = read_yaml(CONFIG_PATH)
    if what in config['types']:
        # terrible again: no locks, no transactions, shit performance etc.
        # probably should move soon to NoSQL (probably best option), or SQL, or implement DATADIR support properly 
        # (I guess ideally NoSQL + DATADIR implemented properly to have two options for convenience but that
        # will most probably require a lot more maintainance and overall commitment)
        # (btw. this entire loop is horrible, refactor it no matter what, it's already too much with this CORS
        # duplications, ulgy response constructions, and raw plus poorly chosen exceptions; to name a few)
        links_to_remove = []
        links = read_json(LINKS_FILE_PATH)
        for i, link in enumerate(links):
            a, b = link['from'], link['to']
            if (a == what and b != what) or (a != what and b == what):
                raise ValueError(f'cannot delete type "{what}": items of other types are linked with "{what}" items')
            elif a == what and b == what:
                links_to_remove.append(i)
        
        if len(links_to_remove):
            # yes, I know, very bad performance. No need to optimize it yet.
            write_json(LINKS_FILE_PATH, list(link for i, link in enumerate(links) if i not in links_to_remove))

        config['order'] = [type_name for type_name in config['order'] if type_name != what]
        del config['types'][what]

        write_yaml(CONFIG_PATH, config)

        os.remove(os.path.join(DATADIR_PATH, f'{what}.json'))

    response = jsonify({'response': 'ok (probably)'})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response