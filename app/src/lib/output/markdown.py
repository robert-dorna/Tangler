#!/bin/python
import json
import yaml
from itertools import zip_longest



def generate(schema, data):

    def matches(item, criteria):
        for field, expected in criteria.items():
            if item[field] != expected:
                return False
        return True

    def fmt(item, formatting):
        value = item.get(formatting['field']) or ''
        if 'format' in formatting:
            value = f'*{value}*'
        if 'link_target' in formatting:
            url = item[formatting['link_target']]
            value = f'[{value}]({url})'
        if 'prefix' in formatting:
            for prefix in item[formatting['prefix']]:
                value = f'`{prefix}` {value}'
        return value

    titles = []
    paddings = []
    values = []

    for column in schema['lists']:
        formatting, criteria = column['value'], column['criteria']
        values.append( [ fmt(item, formatting) for item in data if matches(item, criteria) ] )

        titles.append( column['title'] )

        paddings.append( max([ max([ len(value) for value in values[-1] ]), len(titles[-1]) ]) )

    output = ''

    for i, title in enumerate(titles):
        output += f'| {title:<{paddings[i]}} '
    output += '|\n'

    for padding in paddings:
        output += f'|-{"-"*padding}-'
    output += '|\n'

    for row in zip_longest(*values, fillvalue=''):
        for i, col in enumerate(row):
            output += f'| {col:<{paddings[i]}} '
        output += '|\n'

    print(output)


if __name__ == "__main__":
    with open('format.yaml') as format_file:
        schema = yaml.safe_load(format_file)
        with open('tech.json', 'r') as data_file:
            data = json.load(data_file)
            generate(schema, data)
