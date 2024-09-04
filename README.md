![PythonSupport](https://img.shields.io/static/v1?label=python&message=%203.8|%203.9|%203.10|%203.11&color=blue?style=flat-square&logo=python)
![PyPI version](https://badge.fury.io/py/xurls.svg?)

## Documentation

A high-level `Url` class to make parsing, looking at and manipulating
urls much easier.

Also allows for easily composable urls.

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
from xurls import Url

url = Url("http://www.google.com/some/path?some_key=some-value")
assert url.host == "www.google.com"

url.host = "apple.com"
assert str(url) == "http://apple.com/some/path"

assert url['some_key'] == 'some-value'

```

You can also compose urls:

```python
from xurls import Url

base_url = Url(host='www.example.com')
url_to_append = Url(path='hello/today')

# Append url; paths will append to end, queries merged together.
# Other components like host will be replaced if there is a value in the appended url.
final_url = base_url.copy().append_url(url_to_append)

assert str(final_url) == 'www.example.com/hello/today'

```
