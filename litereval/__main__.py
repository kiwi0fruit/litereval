import sys
import ast
from copy import deepcopy
import re
from typing import Union, Tuple, Any, NamedTuple


class LiterEvalError(Exception):
    pass


_obj = {'gg': '676', None: 0, (): (1, 2, 3), 'a': """{-1: "123", foo='bar'}
""",
 'x': [1, 2, {'foo': 33, 'bar': '{x=1, y=2, \
z=3}'}]}  # noqa

_str = """\
{gg='676', None: 0, (): (1, 2, 3), a=\"\"\"{-1: "123", foo='bar'}
\"\"\",
 x=[1, 2, {foo=33, bar='{x=1, y=2, \\
z=3}'}]}\
"""


class Args(NamedTuple):
    """args: tuple, kwargs: dict"""
    args: Union[tuple, None]
    kwargs: Union[dict, None]


def litereval(string: str):
    """
    Small extension of ``ast.literal_eval`` that also
    accepts dict in a form of ``{key=100, foo='bar'}``

    Returns
    -------
    ret :
        ast.literal_eval(preprocess(string))

    >>> assert repr(_obj) == repr(litereval(_str))
    """
    try:
        return ast.literal_eval(string)
    except SyntaxError:
        pass

    input_charset = set(list(string))
    reps = []

    for ch in range(256, sys.maxunicode):
        if not (chr(ch) in input_charset):
            reps.append(chr(ch))
            if len(reps) == 3:
                break

    reps = {'\\': reps[0], '"': reps[1], "'": reps[2]}  # language=PythonRegExp
    no_esc = r"(?:^|(?<=[^\\]))"
    string = re.sub(
        rf"{no_esc}\\[\\'\"]",
        lambda m: reps[m.group(0)[1:]],
        string
    )
    string = re.sub(
        rf"{no_esc}('''(.*?[^\\'])?'''|\"\"\"(.*?[^\\\"])?\"\"\"|'(.*?[^\\'])?'|\"(.*?[^\\\"])?\"|\w+[=]((?=[^=])|$))",
        lambda m: f'"{m.group(0)[:-1]}": ' if (m.group(0)[-1] == '=') else m.group(0),
        string,
        flags=re.DOTALL
    )
    reps = {val: key for key, val in reps.items()}
    string = re.sub(
        rf"[{''.join(map(re.escape, reps.keys()))}]",
        lambda m: reps[m.group(0)],
        string
    )
    return ast.literal_eval(string)


def merge(source: dict, destination: dict,
          copy: bool = False) -> dict:
    """
    Deep merge two dictionaries.
    Overwrites in case of conflicts.
    From https://stackoverflow.com/a/20666342

    Returns
    -------
    ret :
        ...

    >>> dst = {'first': {'inn': {'foo': 'dog', 'n': 1}}}
    >>> repr_dst = repr(dst)
    >>> src = {'first': {'inn': {'bar': 'cat', 'n': 5}}}
    >>> repr_src = repr(src)
    >>> ret = {'first': {'inn': {'foo': 'dog', 'n': 5, 'bar': 'cat'}}}
    >>> assert repr(merge(src, dst, copy=True)) == repr(ret)
    >>> assert (repr(dst) == repr_dst) and (repr(src) == repr_src)
    >>> assert repr(merge(src, dst)) == repr(ret)
    >>> assert not (repr(dst) == repr_dst) and (repr(src) == repr_src)
    """
    if copy:
        destination = deepcopy(destination)

    for key, val in source.items():
        if isinstance(val, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            merge(val, node, copy=False)
        else:
            destination[key] = (deepcopy(val) if copy else val)

    return destination


def tuple_(obj: Any) -> tuple:
    """Converts any object to tuple. ``string`` to ``(string,)``."""
    if isinstance(obj, str):
        return obj,
    try:
        return tuple(obj)
    except TypeError:
        return obj,


def validated(args: tuple, kwargs: dict) -> Tuple[tuple, dict]:
    """Validates inputs and returns ``*args, **kwargs``."""
    def ret(*args_, **kwargs_):
        return args_, kwargs_
    try:
        return ret(*args, **kwargs)
    except TypeError as e:
        raise LiterEvalError(e)


def get(key: str, dic, default=None):
    """Gets key even from not a dictionary."""
    try:
        return dict(dic).get(key, default)
    except TypeError:
        return default


def args_kwargs(args: Any) -> Tuple[
    Union[tuple, None], Union[dict, None]
]:
    """
    Parses ``args`` object to ``(*args, **kwargs)`` tuple.
    Special case when ``args`` is ``None``: returns ``(None, None)``.
    Otherwise tries to put not iterable object to tuple:
    ``args`` to ``(args,)``. Examples:

    * ``(1, 2)`` to ``(1, 2), {}``
    * ``"foo"`` to ``("foo",), {}``
    * ``{(): ('a', 0), 'foo': None} to
      ``('a', 0), {'foo': None}``

    Returns
    -------
    ret :
        tuple: *args, **kwargs

    >>> dic = litereval("{func={(): (1, 2), foo=True, bar=100}, foo={(): 'bar'}}")
    >>> args_kwargs(get('func', dic))
    ((1, 2), {'foo': True, 'bar': 100})
    >>> args_kwargs(get('foo', dic))
    (('bar',), {})
    >>> args_kwargs(get('bar', dic, {}))
    ((), {})
    >>> args_kwargs(get('bar', dic))
    (None, None)
    >>> args_kwargs(get('bar', [1, 2]))
    (None, None)
    >>> from collections import OrderedDict
    >>> args_kwargs(get('bar', OrderedDict([('bar', {'key': 'val'}),])))
    ((), {'key': 'val'})
    >>> args_kwargs(get('foo', {'foo': {0: 0, 1: 1}}))
    Traceback (most recent call last):
    LiterEvalError: ret() keywords must be strings
    """
    if args is None:
        return None, None
    try:
        dic = dict(args)
        args_ = dic.get((), ())
        dic.pop((), None)
        return validated(tuple_(args_), dic)
    except TypeError:
        return validated(tuple_(args), {})


def get_args(name: str, args, default=None) -> Args:
    """
    Gets ``*args`` and ``**kwargs`` for a ``name`` function
    from an ``args`` dict. Wrapper around ``args_kwargs`` function.

    Returns ``NamedTuple`` ``Args``: ``(args: tuple, kwargs: dict)``
    """
    return Args(*args_kwargs(get(name, args, default)))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
