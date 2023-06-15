import asyncio
import functools
import logging

_logger = logging.getLogger('suppress_exceptions')


def suppress_exceptions(func):
    """ Decorator for suppressing exceptions. The exception will be logged and the function will return None.
    This decorator works for both sync and async functions.
    """

    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            _logger.exception(e)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            _logger.exception(e)

    return async_wrapper if asyncio.iscoroutinefunction(func) else wrapper
