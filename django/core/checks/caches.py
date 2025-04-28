from django.conf import settings
from django.core.cache import DEFAULT_CACHE_ALIAS, caches

from . import Error, Tags, register

E001 = Error(
    "You must define a '%s' cache in your CACHES setting." % DEFAULT_CACHE_ALIAS,
    id="caches.E001",
)


@register(Tags.caches)
def check_default_cache_is_configured(app_configs, **kwargs):
    if DEFAULT_CACHE_ALIAS not in settings.CACHES:
        return [E001]
    return []


@register(Tags.caches)
def check_cache_backends(app_configs, **kwargs):
    """
    Call the check() method on each cache backend to collect errors and warnings.
    """
    errors = []
    for alias in settings.CACHES:
        cache = caches[alias]
        # Add the alias to the kwargs so the cache backend can include it in warnings
        backend_kwargs = {**kwargs, "alias": alias}
        errors.extend(cache.check(**backend_kwargs))
    return errors
