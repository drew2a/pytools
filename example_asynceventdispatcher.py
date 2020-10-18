"""This is an example of how to work with AsyncEventDispatcher

Here we will emulate three types of subscribers:
* slow
* medium
* fast

>>> asyncio.run(main())
Enter main
Before publish
After publish
→ Enter Slow subscriber
→ Enter Fast subscriber
→ Enter Medium subscriber
  Fast: foo
← Leave Fast subscriber
  Medium: foo
← Leave Medium subscriber
  Slow: foo
← Leave Slow subscriber
Leave main
"""
import asyncio

from asynceventdispatcher import AsyncEventDispatcher


async def wait_and_print(name, delay, **kwargs):
    value = kwargs.pop('value', None)
    print(f'→ Enter {name} subscriber')
    await asyncio.sleep(delay)
    print(f'  {name}: {value}')
    print(f'← Leave {name} subscriber')


async def fast_subscriber(**kwargs):
    await wait_and_print('Fast', 1, **kwargs)


async def medium_subscriber(**kwargs):
    await wait_and_print('Medium', 5, **kwargs)


async def slow_subscriber(**kwargs):
    await wait_and_print('Slow', 10, **kwargs)


async def main():
    print('Enter main')

    dispatcher = AsyncEventDispatcher()
    topic = 'topic'

    dispatcher.subscribe(topic, fast_subscriber)
    dispatcher.subscribe(topic, medium_subscriber)
    dispatcher.subscribe(topic, slow_subscriber)

    print("Before publish")
    publish_tasks = dispatcher.publish(topic, value='foo')
    print("After publish")

    if publish_tasks:
        await asyncio.wait(publish_tasks)

    print("Leave main")


asyncio.run(main())
