import sys
import ast
import copy
import re


def litereval(string: str):
    """
    Small extension of ``ast.literal_eval`` that also
    accepts dict in a form of ``{key=100, foo='bar'}``
    """
    input_charset = set(list(string))
    reps = []
    
    for ch in range(256, sys.maxunicode):
        if not (chr(ch) in input_charset):
            reps.append(chr(ch))
            if len(reps) == 3:
                break

    reps = {'\\': reps[0], '"': reps[1], "'": reps[2]}
    string = re.sub(
        r"(^|(?<=[^\\]))\\[\\'\"]",
        lambda m: reps[m.group(0)[1:]],
        string
    )
    string = re.sub(
        r"(^|(?<=[^\\]))('''(.*?[^\\'])?'''|\"\"\"(.*?[^\\\"])?\"\"\"|'(.*?[^\\'])?'|\"(.*?[^\\\"])?\"|\w+[=]((?=[^=])|$))",
        lambda m: f'"{m.group(0)[:-1]}": ' if (m.group(0)[-1] == '=') else m.group(0),
        string,
        flags=re.DOTALL
    )
    reps = {val: key for key, val in reps.items()}
    string = re.sub(
        r"[{''.join(map(re.escape, reps.keys()))}]",
        lambda m: reps[m.group(0)],
        string
    )
    return ast.literal_eval(string)


def merge(source: dict, destination: dict,
              deepcopy: bool=False):
    """
    Deep merge two dictionaries.
    Overwrites in case of conflics.
    From https://stackoverflow.com/a/20666342

    >>> dst = {'first': {
    >>>     'inn': {'foo': 'dog', 'n': 1}
    >>> }}
    >>> src = {'first': {
    >>>     'inn': {'bar': 'cat', 'n': 5}
    >>> }}
    >>> merge(src, dst) == {'first': {
    >>>     'inn': {'foo': 'dog', 'bar': 'cat', 'n': 5}
    >>> }}
    True
    """
    if deepcopy:
        destination = copy.deepcopy(destination)

    for key, val in source.items():
        if isinstance(val, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            merge(val, node, deepcopy)
        else:
            destination[key] = (copy.deepcopy(val)
                                if deepcopy else val)

    return destination
