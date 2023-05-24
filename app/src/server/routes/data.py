import os
import json
from flask import request, abort, jsonify
from ..app import app
from ...lib.api import Api



@app.route("/data/<what>", methods=['GET'])
def get_type_items(what):
    response = jsonify(Api().readall(what))
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


# note: this is not consistant with config POST as this one does not have exactly the same
# path as the resulting (new/being created) resource
@app.route("/data/<what>", methods=['POST'])
def create_type_item(what):
    args = {**request.json}

    # this whole functions looks "ugly", is too long and complex and just overall bad
    # todo: refactor lib.api

    # todo: config API/lib.api should block attempts on defining those fields or any fields starting with '_'
    if '_id' in args or '_what' in args:
        raise ValueError(f'item cannot be created with manually specified _id or _what as those keys are reserved')

    place = args.pop('_place')
    relationship = place['relationship']
    reference = place['reference'] if relationship != 'top' else None

    api = Api()
    api.read_links()

    if relationship == 'child':
        new_id = api.create(what, args)
        api.links.append({
            'from': {'_id': reference['_id'], 'what': reference['what']},
            'to': {'_id': new_id, 'what': what}
        })
        api.write_links()
    elif relationship != 'top':
        try:
            i, link = next((i, v)
                           for i, v in enumerate(api.links) if v['to'] == reference)
            new_id = api.create(what, args)
            api.links.insert(i if relationship == 'above' else i+1, {
                'from': link['from'],
                'to': {'_id': new_id, 'what': what}
            })
            api.write_links()
        except StopIteration:
            i, _ = api.read(reference['what'], reference['_id'])
            api.create(what, index=i if relationship == 'above' else i+1, values=args)

    response = jsonify({'new_item_id': new_id})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/data/<what>/<int:id>", methods=['GET'])
def get_type_item(what, id):
    response = jsonify(Api().read(what, id))
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/data/<what>/<int:id>", methods=['PATCH'])
def update_type_item(what, id):
    # todo: move, link and maybe more 
    args = {**request.json}

    # todo: duplicates logic of POST method
    if '_id' in args or '_what' in args:
        raise ValueError(f'item cannot be created with manually specified _id or _what as those keys are reserved')

    if '_place' in args:
        place = args.pop('_place')
        relationship = place['relationship']

        if relationship == 'top':
            api = Api()
            parent_data = api.parent(what, id)
            if parent_data:
                _, parent = parent_data
                # todo: standarize '_' in special types (sometimes its missing, e.g. in link and reference)
                api.unlink(parent['_what'], parent['_id'], what, id)

        reference = place['reference']

        api = Api()

        reference_parent = api.parent(reference['what'], reference['_id'])
        if (reference_parent is None) and (what != reference['what']) and (relationship != "child"):
            abort(400)
        
        parent_data = api.parent(what, id)
        if parent_data:
            _, parent = parent_data
            api.unlink(parent['_what'], parent['_id'], what, id)

        if relationship == "child":
            api.link(reference['what'], reference['_id'], what, id)
        else:
            if reference_parent is None:
                index, _ = api.read(reference['what'], reference['_id'])
                api.move(what, id, index if relationship == 'above' else index + 1)
            else:
                link_index, parent = reference_parent
                if relationship == "below":
                    link_index += 1

                api.links.insert(link_index, {
                    'from': {'what': parent['_what'], '_id': parent['_id']},
                    'to': {'what': what, '_id': id}
                })
                api.write_links()

    app.logger.info('calling update %s %s %s', what, id, json.dumps(args))
    Api().update(what, id, values=args)
    return get_type_item(what, id)


@app.route("/data/<what>/<int:id>", methods=['DELETE'])
def delete_type_item(what, id):
    # todo: delete throws if id does not exist and that is not indempotent
    Api().delete(what, id)
    response = jsonify({'response': 'ok (probably)'})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response