from flask import request, abort, jsonify
from ...lib.api import Api


def move_route_handler(app):
    args = {**request.args}

    location = args.pop('location')
    what = args.pop('what')
    id = int(args.pop('id'))
    to_what = args.pop('to_what')
    to_id = int(args.pop('to_id'))

    api = Api()

    if api.parent(to_what, to_id) is None and what != to_what and location != "child":
        abort(400)

    parent_data = api.parent(what, id)
    if parent_data:
        app.logger.info('unlinking source')
        _, parent = parent_data
        api.unlink(parent['_what'], parent['_id'], what, id)

    app.logger.info('location is %s', location)
    if location == "child":
        app.logger.info('location is child')
        api.link(to_what, to_id, what, id)
    else:
        app.logger.info('location is not child')
        parent_data = api.parent(to_what, to_id)
        if parent_data is None:
            app.logger.info('"to" parent is None')
            index, _ = api.read(to_what, to_id)
            api.move(what, id, index)
        else:
            link_index, parent = parent_data
            new_link = {
                'from': {'what': parent['_what'], '_id': parent['_id']},
                'to': {'what': what, '_id': id}
            }
            app.logger.info('new link is %s', new_link)
            if location == "below":
                link_index += 1
            api.links.insert(link_index, new_link)
            api.write_links()

    response = jsonify({'status': 'ran move, success unknown'})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response