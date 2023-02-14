from datetime import datetime, timedelta
import huepy as colors
from os import path
from ..core.files import read_yaml, CONFIG_PATH
import textwrap


###############################
# formatters
###############################


def calendar(v, _):
    def gday(n):
        return datetime.today() - timedelta(days=n)

    weekdays = [ 'pn', 'wt', 'sr', 'czw', 'pt', 'so', 'nd' ]
    cal = []
    for day in reversed([ gday(x) for x in range(7) ]):
        color = colors.white
        day_string = day.strftime('%Y-%m-%d')
        if day_string in v:
            color = colors.green if v[day_string] == 'yes' else colors.red
        cal.append(color(weekdays[day.weekday()]))

    return str.join('  ', cal)


def indent(v, all_v):
    indent = ' ' * (all_v['_indent'] + 4)
    return f'{indent}{v}'


def body(v, all_v, width=70):
    indent = ' ' * (all_v['_indent'] + 4)
    wrapped = textwrap.wrap(v,
        initial_indent=indent,
        subsequent_indent=indent,
        width=width
    )
    return str.join('\n', wrapped)


###############################
# loading config
###############################


class Formatter:
    def __init__(self):
        config = read_yaml(path.join(CONFIG_PATH, '_terminal.yaml'))

        self.buildin_formatters = {
            'red': lambda v, _=None: colors.red(v),
            'purple': lambda v, _=None: colors.purple(v),
            'blue': lambda v, _=None: colors.blue(v),
            'white': lambda v, _=None: colors.white(v),
            'orange': lambda v, _=None: colors.orange(v),
            'green': lambda v, _=None: colors.green(v),
            'cyan': lambda v, _=None: colors.cyan(v),
            'cal': calendar,
            'body': body,
            'body_short': lambda v, all_v: body(v, all_v, width=40),
            'indent': indent,
        }

        self.templates = config['templates']
        self.formatters = { name: self.formatter(name, spec)
            for name, spec in config['formatters'].items()
        }


    def _formatter(self, fmt_string):
        assert len(fmt_string) > 0, 'empty terminal formatter definition'

        if fmt_string[0] not in ['?', '=']:
            return lambda v, all_v=None: self.buildin_formatters[fmt_string](v, all_v)

        assert len(fmt_string) > 1, 'empty terminal formatter definition (fmt string)'

        fmt = lambda v, all_v={}: fmt_string[1:].format(v=v, **all_v)
        # def fmt(v, all_v={}):
        #     result = fmt_string[1:].format(v=v, **all_v)
        #     print('fmt result:', result, 'type:', type(result))
        #     return result

        if fmt_string[0] == '=':
            return fmt 

        return lambda v, all_v={}: fmt(v, all_v) if v != '' else ''


    def formatter(self, name, spec):
        if isinstance(spec, str):
            return self._formatter(spec)

        return lambda v, all_v: self._formatter(spec[all_v[name]])(v, all_v)


    def format(self, values, what, *, indent=0):
        template = self.templates[what]

        values = values | { '_indent': indent }

        def find_format(pos):
            return template.find('{', pos), template.find('}', pos)

        text = '' 
        c = 0
        while c < len(template):
            start, stop = find_format(c)
            if -1 in [start, stop]:
                text += template[c:]
                break
            
            text += template[c:start]
            formats = template[start+1:stop].split(':')
            value = values.get(formats[0]) if formats[0][0] != "=" else formats[0][1:]
            if value is None:
                value = ''
            for fmt in formats[1:]:
                if fmt[0] in ['<', '>']:
                    value = f'{value:{fmt}}'
                else:

                    if fmt in self.formatters:
                        value = self.formatters[fmt](value, values)
                    else:
                        value = self.buildin_formatters[fmt](value, values)

            text += str(value)
            c = stop + 1

        return text

