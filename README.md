# litereval

* `litereval`: Wrapper around `ast.literal_eval` with new additional `{foo='bar', key=None}` `dict` syntax.
* `merge`: Deep merge two dictionaries.
* `get_args_kwargs`: Read `*args` and `*kwargs` from `dict` by key.


# API

```py
def litereval(string: str):
    """
    Small extension of ``ast.literal_eval`` that also
    accepts dict in a form of ``{key=100, foo='bar'}``
    """
    ...
    return ast.literal_eval(string)
```

```py
def merge(source: dict, destination: dict,
          copy: bool = False) -> dict:
    """
    Deep merge two dictionaries.
    Overwrites in case of conflics.
    From https://stackoverflow.com/a/20666342
    ...
    """
    ...
    
```


```py
def get_args_kwargs(name: str, args: dict, default=None) -> Tuple[
    Union[list, None], Union[dict, None]
]:
    """
    Reads *args and **kwars for function/method from a dict by ``name`` key.

    * ``(1, 2)`` -> ``[1, 2], {}``
    * ``"foo"`` -> ``["foo"], {}``
    * ``{(): ('a', 0), 'foo': None} ->
      ``['a', 0], {'foo': None}``


    Parameters
    ----------
    name :
        function/method name
    args :
        dict with function/method names as first level keys
    default :
        default fallback value to extract from args

    Returns
    -------
    ret :
        tuple: *args, **kwargs
    """
    ...
```
