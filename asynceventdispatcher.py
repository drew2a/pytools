import asyncio
from collections import defaultdict


class AsyncEventDispatcher:
    def __init__(self):
        self._subscribers = defaultdict(lambda: set())

    def subscribe(self, topic, async_function):
        self._subscribers[topic].add(async_function)

    def unsubscribe(self, topic, async_function):
        self._subscribers[topic].discard(async_function)

    def publish(self, topic, **kwargs):
        return [asyncio.create_task(async_function(**kwargs))
                for async_function in self._subscribers[topic]]
