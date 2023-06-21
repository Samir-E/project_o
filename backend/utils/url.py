from typing import Any, Callable, Mapping

from django.urls import reverse
from django.utils.functional import lazy
from django.utils.http import urlencode


def reverse_querystring(
    viewname: Callable | str | None,
    urlconf: str | None = None,
    args: Any = None,
    kwargs: dict[str, Any] | None = None,
    current_app: str | None = None,
    query: Mapping[str, Any] | None = None,
) -> str:
    """Custom reverse to handle query strings."""
    base_url = reverse(
        viewname,
        urlconf=urlconf,
        args=args,
        kwargs=kwargs,
        current_app=current_app,
    )
    if query:
        return '{}?{}'.format(base_url, urlencode(query))
    return base_url


reverse_lazy = lazy(reverse_querystring, str)
