# litereval

Wrapper around `ast.literal_eval` with new additional `{foo='bar', key=None}` dict syntax. + Deep merge two dictionaries.


# API

```py
def litereval(string: str):
    # do stuff...
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
