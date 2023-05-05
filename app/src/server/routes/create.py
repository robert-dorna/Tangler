from flask import request, jsonify
from ...lib.api import Api


def create_route_handler():
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