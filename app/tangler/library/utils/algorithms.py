from enum import Enum
from collections import OrderedDict
from operator import itemgetter


class Placement(Enum):
    BEFORE = 1
    AFTER = 2


def inserted(
    iterable,
    object,
    *,
    reference,
    key=None,
    placement=Placement.BEFORE,
    allow_unfound=False,
):
    if key is None:
        key = lambda v: v

    weaved = False
    for element in iterable:
        if placement == Placement.BEFORE and key(element) == reference:
            weaved = True
            yield object

        yield element

        if placement == Placement.AFTER and key(element) == reference:
            weaved = True
            yield object

    if not weaved:
        if allow_unfound:
            yield object
        else:
            raise ValueError("anchor not found")


def odict_inserted(
    od: OrderedDict,
    object,
    *,
    reference_key=None,
    placement=Placement.BEFORE,
    allow_unfound=False,
):
    return OrderedDict(
        inserted(
            od.items(),
            object,
            reference=reference_key,
            key=itemgetter(0),
            placement=placement,
            allow_unfound=allow_unfound,
        )
    )


def odict_reordered(
    od: OrderedDict,
    key,
    *,
    reference_key,
    placement=Placement.BEFORE,
    allow_unfound=False,
):
    od.move_to_end(key, last=True)
    popped = od.popitem(last=True)

    return odict_inserted(
        od,
        popped,
        reference_key=reference_key,
        placement=placement,
        allow_unfound=allow_unfound,
    )
