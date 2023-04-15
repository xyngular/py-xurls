![PythonSupport](https://img.shields.io/static/v1?label=python&message=%203.8|%203.9|%203.10|%203.11&color=blue?style=flat-square&logo=python)
![PyPI version](https://badge.fury.io/py/xurls.svg?)

## Documentation

This is pre-release Alpha software, based on another code base and
the needed changes to make a final release version are not yet
completed.

Everything is subject to change!

**[📄 Detailed Documentation](https://xyngular.github.io/py-xurls/latest/)** | **[🐍 PyPi](https://pypi.org/project/xurls/)**

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

