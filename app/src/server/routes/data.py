from flask import request, jsonify
from ..app import app
from ...lib.api import Api


@app.route("/old/data", methods=['GET'])
def data_read():  # not really, now it callls arbitrary function

    args = {**request.args}

    if 'index' in args:
        args['index'] = int(args['index'])
    if '_id' in args:
        args['_id'] = int(args['_id'])

    app.logger.info('args: %s', args)

    api = Api()
    method = args.pop('method') if 'method' in args else 'read'
    method = getattr(api, method)

    what = args.pop('what')if 'what' in args else 'task'
    if ',' in what:
        what = what.split(',')

    app.logger.info('calling with')
    app.logger.info(' > what: %s', what)
    app.logger.info(' > args: %s', args)

    if isinstance(what, list):
        result = {w: method(what=w, **args) for w in what}
    else:
        result = method(what=what, **args)

    # data.flush()

    success = True  # todo, way to check from Data that it was updated
    response = jsonify(
        {'status': 'ran method, success unknown', 'result': result} if success else
        {'status': 'error'}
    )

    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/old/data", methods=['POST'])
def data_update():
    args = {**request.args}

    what = args.pop('what')
    _id = int(args.pop('_id'))

    api = Api()
    api.update(what, _id, values=args)

    response = jsonify({'status': 'ran update, success unknown'})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/old/data", methods=['PUT'])
def data_create():
    args = {**request.args}

    args.pop('_id')

    what = args.pop('_what')
    location = int(args.pop('_location'))
    anchor = {
        '_id': int(args.pop('_anchorId')),
        'what': args.pop('_anchorWhat'),
    }

    api = Api()
    api.read_links()

    ABOVE = 1
    BELOW = 2
    CHILD = 3

    if location == CHILD:
        newId = api.create(what, values=args)
        new_link = {
            'from': {'_id': anchor['_id'], 'what': anchor['what']},
            'to': {'_id': newId, 'what': what}
        }
        api.links.append(new_link)
        api.write_links()
    else:
        try:
            i, link = next((i, v)
                           for i, v in enumerate(api.links) if v['to'] == anchor)
            newId = api.create(what, values=args)
            new_link = {'from': link['from'], 'to': {'_id': newId, 'what': what}}
            api.links.insert(i if location == ABOVE else i+1, new_link)
            api.write_links()
        except StopIteration:
            i, _ = api.read(anchor['what'], anchor['_id'])
            api.create(what, index=i if location == ABOVE else i+1, values=args)

    response = jsonify({'status': 'ran craete, success unknown'})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response