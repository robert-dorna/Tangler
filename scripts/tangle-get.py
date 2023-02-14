#!/usr/bin/env python
import sys
from src.api import Api


api = Api()


def main(argv):
    accounts, _ = api.read('account')
    try:
        match = lambda acc: bool(acc['_id'] == int(argv[0]))
        i, acc = next((i, acc) for i, acc in enumerate(accounts) if match(acc))
        for k, v in acc.items():
            print(f'{k:<15}: {v}')
    except StopIteration:
        print('cant find')



if __name__ == '__main__':
    main(sys.argv[1:])


