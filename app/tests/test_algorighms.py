from typing import Any
from collections import OrderedDict

from tangler.library import types
from tangler.library.spaces.config import SpacesConfig
from tangler.library.spaces.filesystem import FilesystemSpace
from tangler.library.utils import algorithms

from . import utils_assets as assets
from .utils_fixtures import *
from .utils_requests import *


def test_odict_inserted():
    data = [
        ('a', 1),
        ('b', 2),
        ('c', 3),
        ('d', 4),
        ('e', 5),
        ('f', 6),
    ]

    odict = OrderedDict(data)

    odict_inserted = algorithms.odict_inserted(odict, ('x', 100), reference_key='c')
    odict_inserted_keys = list(odict_inserted.keys())
    odict_inserted_values = list(odict_inserted.values())

    assert odict_inserted_keys == ['a', 'b', 'x', 'c', 'd', 'e', 'f']
    assert odict_inserted_values == [1, 2, 100, 3, 4, 5, 6]
