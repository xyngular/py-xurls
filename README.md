This is pre-release Alpha software, based on another code base and
the needed changes to make a final release version are not yet
completed.

Everything is subject to change!

## Getting Started

```shell
poetry install xurls
```

or

```shell
pip install xurls
```

Very basic example:

```python
from xurls import URLMutable

url = URLMutable("http://www.google.com/some/path")
assert url.host == "www.google.com"

url.host = "apple.com"
assert url.url() == "http://appe.com/some/path"
```

