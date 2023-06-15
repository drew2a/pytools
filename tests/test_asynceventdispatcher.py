import asyncio

import pytest

from asynceventdispatcher import AsyncEventDispatcher


@pytest.fixture
def subscriber():
    class Subscriber:
        handled = False
        value = None

        async def handle(self):
            self.handled = True

        async def set_value(self, value=None):
            self.value = value

    return Subscriber()


@pytest.fixture
def dispatcher():
    return AsyncEventDispatcher()


def test_subscribe_same_topic_function(dispatcher):
    topic = 'topic'

    def _f():
        pass

    dispatcher.subscribe(topic, _f)
    dispatcher.subscribe(topic, _f)
    assert len(dispatcher._subscribers[topic]) == 1


def test_subscribe_same_topic_lambda(dispatcher):
    topic = 'topic'
    dispatcher.subscribe(topic, lambda: None)
    dispatcher.subscribe(topic, lambda: None)
    assert len(dispatcher._subscribers[topic]) == 2


def test_unsubscribe_same_topic(dispatcher):
    topic = 'topic'

    def _f():
        pass

    dispatcher.subscribe(topic, lambda: None)
    dispatcher.subscribe(topic, lambda: None)
    dispatcher.subscribe(topic, _f)

    assert len(dispatcher._subscribers[topic]) == 3

    dispatcher.unsubscribe(topic, lambda: None)
    assert len(dispatcher._subscribers[topic]) == 3

    dispatcher.unsubscribe(topic, _f)
    assert len(dispatcher._subscribers[topic]) == 2


def test_subscribe_different_topics(dispatcher):
    dispatcher.subscribe('topic', lambda: None)
    dispatcher.subscribe('topic2', lambda: None)
    assert len(dispatcher._subscribers) == 2

    dispatcher.subscribe('', lambda: None)
    dispatcher.subscribe(None, lambda: None)
    assert len(dispatcher._subscribers) == 4


@pytest.mark.asyncio
async def test_return_empty_topic(dispatcher):
    with pytest.raises(ValueError):
        await asyncio.wait(dispatcher.publish(''))

    assert dispatcher.publish('') == []


@pytest.mark.asyncio
async def test_publish(dispatcher, subscriber):
    dispatcher.subscribe('topic', subscriber.handle)
    assert not subscriber.handled

    assert dispatcher.publish('any other topic') == []
    assert not subscriber.handled

    await asyncio.wait(dispatcher.publish('topic'))
    assert subscriber.handled


@pytest.mark.asyncio
async def test_publish_with_args(dispatcher, subscriber):
    topic = 'topic'

    dispatcher.subscribe(topic, subscriber.set_value)
    assert not subscriber.value

    await asyncio.wait(dispatcher.publish(topic, value=42))
    assert subscriber.value == 42


@pytest.mark.asyncio
async def test_publish_two_topics(dispatcher, subscriber):
    topic = 'topic'
    topic1 = 'topic1'

    dispatcher.subscribe(topic, subscriber.handle)
    dispatcher.subscribe(topic1, subscriber.set_value)

    assert not subscriber.handled
    assert not subscriber.value

    await asyncio.wait(dispatcher.publish(topic))
    assert subscriber.handled
    assert not subscriber.value

    await asyncio.wait(dispatcher.publish(topic1, value=42))
    assert subscriber.handled
    assert subscriber.value == 42


@pytest.mark.asyncio
async def test_publish_call_wrong_args(dispatcher, subscriber):
    topic = 'topic'
    topic1 = 'topic1'

    dispatcher.subscribe(topic, subscriber.handle)
    with pytest.raises(TypeError):
        await asyncio.wait(dispatcher.publish(topic, 'some argument'))

    dispatcher.subscribe(topic1, subscriber.set_value)
    with pytest.raises(TypeError):
        await asyncio.wait(dispatcher.publish(topic1, 'some argument'))


@pytest.mark.asyncio
async def test_mixed_call_args(dispatcher, subscriber):
    topic = 'topic'

    dispatcher.subscribe(topic, subscriber.set_value)
    dispatcher.subscribe(topic, subscriber.handle)

    await asyncio.wait(dispatcher.publish(topic))
    assert subscriber.handled
    assert not subscriber.value
