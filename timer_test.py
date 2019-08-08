import numpy as np
import asyncio
import time
import trio
import datetime


async def until(t, logarithmic_sleep=False):
    """
    Pause your program until a specific end time.
    'time' is either a valid datetime object or unix timestamp in seconds (i.e. seconds since Unix epoch)
    """
    end = t

    # Type check
    if not isinstance(end, (int, float)):
        raise RuntimeError('The time parameter is not a number datetime object')

    # Now we wait
    if logarithmic_sleep:
        while True:
            now = time.time()
            diff = end - now

            #
            # Time is up!
            #
            if diff <= 0:
                break
            else:
                # 'logarithmic' sleeping to minimize loop iterations
                await asyncio.sleep(diff / 2)
    else:
        now = time.time()
        diff = end - now
        await asyncio.sleep(diff)


def test_sleep(N, w):
    data = []
    for _ in range(N):
        t0 = time.perf_counter()
        time.sleep(w)
        t1 = time.perf_counter()
        data.append(t1 - t0)
    print(
        "Regular: ave = %s, min = %s, max = %s" % (np.average(data), np.min(data), np.max(data))
    )
    return data


async def _sleep(n, w):
    data = []
    for _ in range(n):
        t0 = time.perf_counter()
        await asyncio.sleep(w)
        t1 = time.perf_counter()
        data.append(t1 - t0)
    print(
        "Asyncio: ave = %s, min = %s, max = %s" % (np.average(data), np.min(data), np.max(data))
    )


def test_async_until(n, w):
    loop.run_until_complete(_until(n, w))

async def _until(n, w):
    data = []
    start = time.time()
    for x in range(n):
        t0 = time.perf_counter()
        await until(start + (x * 0.004), logarithmic_sleep=False)
        t1 = time.perf_counter()
        data.append(t1 - t0)
    print(
        "Async until: ave = %s, min = %s, max = %s" % (np.average(data), np.min(data), np.max(data))
    )


def test_async_sleep(n, w):
    loop.run_until_complete(_sleep(n, w))

async def _trio_sleep(n, w):
    data = []
    for _ in range(n):
        t0 = time.perf_counter()
        await trio.sleep(w)
        t1 = time.perf_counter()
        data.append(t1 - t0)
    print(
        "Trio: ave = %s, min = %s, max = %s" % (np.average(data), np.min(data), np.max(data))
    )


async def test_trio_sleep(n, w):
    async with trio.open_nursery() as nursery:
        nursery.start_soon(_trio_sleep, n, w)


N = 100
W = 0.004

loop = asyncio.get_event_loop()
test_sleep(N, W)
test_async_sleep(N, W)
test_async_until(N, W)
trio.run(test_trio_sleep, N, W)

loop.close()
