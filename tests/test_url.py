import dataclasses
from typing import List, Any

import xurls.url
from xurls.url import (
    Url,
    _FormattedQueryValue,
    QueryValue,
    DuplicateKeyNamesQueryValueListFormat,
    UrlFormattingOptions, Query,
)


def test_hst_url():
    url = Url("//some.host")
    print(url)


def test_basic_url_formatting():
    url = Url("/some/endpoint/{id}")

    # Ensure it Url encodes special values.
    assert url.url(secondary_values={'id': 1}) == "/some/endpoint/1"
    assert (
        url.url(secondary_values={'id': "hello#1@gmail.com"})
        == "/some/endpoint/hello%231%40gmail.com"
    )

    url = url.copy_mutable()

    url.is_valid(secondary_values={'id': 1}, attach_values=True)
    assert url.url() == "/some/endpoint/1"

    url.is_valid(secondary_values={'id': "hello#1@gmail.com"}, attach_values=True)
    assert url.url() == "/some/endpoint/hello%231%40gmail.com"


def test_formatting_list_with_no_delimiter():
    url = Url(
        query={'query_name': ['v1', 'v2']},
        formatting_options=DuplicateKeyNamesQueryValueListFormat,
    )

    assert url.url() == "?query_name=v1&query_name=v2"


def test_formatting_list():
    url = Url("/some/path")
    url.query_add("hello1", ['1', 'two'])
    assert url.url() == "/some/path?hello1__in=1,two"


def test_formatting_custom_type():
    @dataclasses.dataclass()
    class FormatValue(_FormattedQueryValue):
        postfix: str = "1"

        def url_query_value(self, *args, **kwargs) -> QueryValue:
            return f"formatted-value-{self.postfix}"

    # Basic custom formatter.
    url = Url("/some/path")
    url.query_add("hello1", FormatValue())
    assert url.url() == "/some/path?hello1=formatted-value-1"

    # Another custom-formatter
    url = Url("/some/path")
    url.query_add("hello2", FormatValue(postfix="B"))
    assert url.url() == "/some/path?hello2=formatted-value-B"

    # Try list of custom-formatters
    url = Url("/some/path")
    url.query_add("hello1", [FormatValue(postfix="B"), FormatValue(postfix="C")])
    assert url.url() == "/some/path?hello1__in=formatted-value-B,formatted-value-C"


# def test_formatting_date_range():
#     range = DateRange(
#         start=dt.date(year=2021, month=2, day=3), end=dt.date(year=2022, month=3, day=4)
#     )
#
#     url_str = Url(query={"create-date": range}).url()
#     assert url_str == "?create-date__range=2021-02-03,2022-03-04"


def test_ensure_url_and_default_formatting_options_work():
    # By default, this should always produce a list regardless of formatting options (dup-keys)
    url = Url.ensure_url("?hello=1&hello=2")
    assert url.query_value('hello') == ['1', '2']

    # Default options use comma separation and `__in` postfix.
    assert url.url() == "?hello__in=1,2"

    url = Url.ensure_url(
        "?hello=1&hello=2", default_formatting_options=DuplicateKeyNamesQueryValueListFormat
    )

    assert url.query_value('hello') == ['1', '2']

    # Url should now have the `DuplicateKeyNamesQueryValueListFormat` options on it.
    assert url.url() == "?hello=1&hello=2"

    # Make sure default_formatting_options is not used if Url already has options set.
    options = UrlFormattingOptions(list_key_suffix=':in', list_value_delimiter=',')
    url = Url(formatting_options=DuplicateKeyNamesQueryValueListFormat)
    url = Url.ensure_url(url, default_formatting_options=options)
    assert url.formatting_options is DuplicateKeyNamesQueryValueListFormat

    # Make sure default_formatting_options IS used if Url has no options unset.
    url = Url()
    url = Url.ensure_url(url, default_formatting_options=options)
    assert url.formatting_options is options


def test_ensure_append_url_uses_url_formatting_options():
    options = UrlFormattingOptions(list_key_suffix=':in', list_value_delimiter=',')
    url = Url(formatting_options=options)
    url = url.append_url("?something:in=value1,value2,value3")
    assert url.query_value('something') == ['value1', 'value2', 'value3']


def test_url_implicit_str_conversion_with_invalid_url():
    url = Url('https://www.test.com/v1/objects/{id}')
    assert not url.is_valid()
    implicit_str = f'some url ({url})'
    assert implicit_str == 'some url (https://www.test.com/v1/objects/{id})'

    # See if we can get a fully-formatted url via secondary_values
    assert url.url(secondary_values={'id': 5}) == 'https://www.test.com/v1/objects/5'

    # See if we can get a fully-formatted url via adding a query key for it.
    url = url.copy_mutable()
    url.query_add('id', 4)
    implicit_str = f'some url 2 ({url})'
    assert implicit_str == 'some url 2 (https://www.test.com/v1/objects/4)'
