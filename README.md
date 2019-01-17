# litereval

`litereval` is wrapper around `ast.literal_eval` with new additional `{foo='bar', key=None}` `dict` syntax.
Plus some helper tools to merge dictionaries, parse `ast.literal_eval` python data to `*args` and `**kwargs`.

* `merge`: Deep merge two dictionaries.
* 
* `get_args_kwargs`: Read `*args` and `*kwargs` from `dict` by key.


# API

### litereval

```py
def litereval(string: str):
    """
    Small extension of ``ast.literal_eval`` that also
    accepts dict in a form of ``{key=100, foo='bar'}``

    Returns
    -------
    ret :
        ast.literal_eval(preprocess(string))
    """
```

### merge

```py
def merge(source: dict, destination: dict,
          copy: bool = False) -> dict:
    """
    Deep merge two dictionaries.
    Overwrites in case of conflicts.
    From https://stackoverflow.com/a/20666342
    """
```

### args_kwargs

```py
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
    """
```

### get

```py
def get(key: str, dic, default=None):
    """Gets key even from not a dictionary."""
```

### tuple\_

```py
def tuple_(obj: Any) -> tuple:
    """Converts any object to tuple. ``string`` to ``(string,)``."""
```

### validated

```py
def validated(args: tuple, kwargs: dict) -> Tuple[tuple, dict]:
    """Validates inputs and returns ``*args, **kwargs``."""
```
