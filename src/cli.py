from .core.validation import validated_values
from .output.terminal import Formatter
from .api import Api


api = Api()


formatter = Formatter()


def display_item(what, index, item, *, indent = 2):
    print(' '*indent, formatter.format(item | {'index': index+1}, what, indent = indent), sep='')
    children_links = api.children(what, item['_id'])
    for link in children_links:
        child_what, child_id = link['to']['what'], int(link['to']['_id'])
        child_index, child_item = api.read(child_what, child_id)
        display_item(child_what, child_index, child_item, indent = indent * 2)


def display(what, _id, *, count=False, fresh=False, only_roots=True):
    if what is None:
        assert _id is None, 'cli display error, got _id for unknown item type'

        whats = ['email', 'check', 'task', 'note', '+item', '+account', '+transaction', '+journal', '+contact']
        for what in whats:
            display(what, None)
        return

    if what[0] == '+':
        return display(what[1:], _id, count=True)


    if _id is None:
        data = api.parentless(what) if only_roots else api.get(what)
        print(f'{what}s:\n')

        if count or len(data) == 0:
            print('  ', len(data), ' elements\n', sep='')
            return

        for i, item in enumerate(data):
            display_item(what, i, item)
        print()
        return

    i, item = api.read(what, _id)
    display_item(what, i, item)
    print()


def run_command(command_name='read', what=None, args=[]):
    def values(args): return {args[i]: args[i+1] for i in range(0, len(args), 2)}

    if command_name == 'read':
        _id = int(args[0]) if len(args) > 0 else None
        display(
            what,
            _id = _id,
            # only_roots = not bool(what is not None and _id is None)
        )
        return

    if command_name in ['link', 'unlink']:
        _id, target_what, target_id = int(args[0]), args[1], int(args[2])
        getattr(api, command_name)(what, _id, target_what, target_id)
        display(what, _id = _id, fresh=True)
        return

    assert what is not None, 'missing item type'

    commands = {
        "create": lambda args: {
            'values': validated_values(what, values(args), enforce_required = True)
        },
        "update": lambda args: {
            'values': validated_values(what, values(args[1:]), enforce_required = False),
            '_id': int(args[0])
        },
        "swap": lambda args: {
            '_id_a': int(args[0]),
            '_id_b': int(args[1])
        },
        "move": lambda args: {
            '_id': int(args[0]),
            'destination_index': int(args[1]) - 1
        },
        "delete": lambda args: {
            '_id': int(args[0])
        }
    }

    args = commands[command_name](args)


    known_ids = None
    if command_name == "create":
        # print('collecting known ids')
        known_ids = set(item['_id'] for item in api.read(what)[0])
    # print('known ids:', known_ids)

    def on_closed(_):
        if command_name in ['move', 'swap', 'delete']:
            display(what, _id = None)
        elif command_name == "create":
            ids = set(item['_id'] for item in api.read(what)[0])
            # print('ids:', ids)
            # print('known_ids:', known_ids)
            new_id = (ids - known_ids).pop()
            display(what, _id = new_id)
        else:
            display(what, _id = args['_id'])

    print('running commnad')
    getattr(api, command_name)(what, **args, on_closed = on_closed)
    print('done')


def parse_args(args):
    return {
        'command_name': args[0] if len(args) > 0 else 'read',
        'what': args[1] if len(args) > 1 else None,
        'args': args[2:]
    }
