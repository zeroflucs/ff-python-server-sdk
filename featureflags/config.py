"""Configuration is a base class that has default values that you can change
during the instance of the client class"""

from typing import Any, Callable, Dict

from .interface import Cache
from .lru_cache import LRUCache
from .util import log

BASE_URL = "https://config.ff.harness.io/api/1.0"
EVENTS_URL = "https://events.ff.harness.io/api/1.0"
MINUTE = 60
PULL_INTERVAL = 1 * MINUTE
PERSIST_INTERVAL = 1 * MINUTE
EVENTS_SYNC_INTERVAL = 1 * MINUTE


class Config(object):
    def __init__(
            self,
            base_url: str = BASE_URL,
            events_url: str = EVENTS_URL,
            pull_interval: int = PULL_INTERVAL,
            persist_interval: int = PERSIST_INTERVAL,
            events_sync_interval: int = EVENTS_SYNC_INTERVAL,
            cache: Cache = None,
            store: object = None,
            enable_stream: bool = True,
            enable_analytics: bool = True,
            max_auth_retries: int = 10,
            tls_trusted_cas_file: str = None,
            httpx_args: Dict[str, Any] = None,
    ):
        self.base_url = base_url
        self.events_url = events_url
        self.pull_interval = pull_interval
        self.persist_interval = persist_interval
        if events_sync_interval < EVENTS_SYNC_INTERVAL:
            log.warning("Metrics events sync interval cannot be lower than "
                        "60 seconds. Default of 60 seconds will be used")
            self.events_sync_interval = EVENTS_SYNC_INTERVAL
        else:
            self.events_sync_interval = events_sync_interval

        self.cache = cache
        if self.cache is None:
            self.cache = LRUCache()
        self.store = store
        self.enable_stream = enable_stream
        self.enable_analytics = enable_analytics
        self.max_auth_retries = max_auth_retries
        self.tls_trusted_cas_file = tls_trusted_cas_file
        self.httpx_args = httpx_args
        if self.httpx_args is None:
            self.httpx_args = {}


default_config = Config()


def with_base_url(base_url: str) -> Callable:
    def func(config: Config) -> None:
        config.base_url = base_url

    return func


def with_events_url(events_url: str) -> Callable:
    def func(config: Config) -> None:
        config.events_url = events_url

    return func


def with_stream_enabled(value: bool) -> Callable:
    def func(config: Config) -> None:
        config.enable_stream = value

    return func


def with_analytics_enabled(value: bool) -> Callable:
    def func(config: Config) -> None:
        config.enable_analytics = value

    return func


def with_pull_interval(value: int) -> Callable:
    def func(config: Config) -> None:
        config.pull_interval = value

    return func


def with_max_auth_retries(value: int) -> Callable:
    def func(config: Config) -> None:
        config.max_auth_retries = value

    return func


def with_tls_trusted_cas_file(value: str) -> Callable:
    """
    This config item is for on-prem or proxy customers using custom TLS certs.
    It takes a filename of a CA bundle. It should include all intermediate CAs
    and the root CA (concatenated in PEM format).
    """
    def func(config: Config) -> None:
        config.tls_trusted_cas_file = value

    return func


def with_httpx_args(args: Dict[str, Any]) -> Callable:
    def func(config: Config) -> None:
        config.httpx_args.update(args)

    return func
