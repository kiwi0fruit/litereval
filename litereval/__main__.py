import sys
import ast
from copy import deepcopy
import re

obj = {'gg': '676', None: 0, (): (1, 2, 3), 'a': """{-1: "123", foo='bar'}
""",
 'x': [1, 2, {'foo': 33, 'bar': '{x=1, y=2, \
z=3}'}]}  # noqa

str_ = """\
{gg='676', None: 0, (): (1, 2, 3), a=\"\"\"{-1: "123", foo='bar'}
\"\"\",
 x=[1, 2, {foo=33, bar='{x=1, y=2, \\
z=3}'}]}\
"""


def litereval(string: str):
    """
    Small extension of ``ast.literal_eval`` that also
    accepts dict in a form of ``{key=100, foo='bar'}``

    >>> assert repr(obj) == repr(litereval(str_))
    """
    input_charset = set(list(string))
    reps = []

    for ch in range(256, sys.maxunicode):
        if not (chr(ch) in input_charset):
            reps.append(chr(ch))
            if len(reps) == 3:
                break

    reps = {'\\': reps[0], '"': reps[1], "'": reps[2]}  # language=PythonRegExp
    no_esc = r"(^|(?<=[^\\]))"
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
          copy: bool = False):
    """
    Deep merge two dictionaries.
    Overwrites in case of conflics.
    From https://stackoverflow.com/a/20666342

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


if __name__ == "__main__":
    import doctest
    doctest.testmod()
