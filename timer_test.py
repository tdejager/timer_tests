import numpy as np
import asyncio
import time
import trio


def test_sleep(N, w):
    data = []
    for _ in range(N):
        t0 = time.perf_counter()
        time.sleep(w)
        t1 = time.perf_counter()
        data.append(t1 - t0)
    print(
        "ave = %s, min = %s, max = %s" % (np.average(data), np.min(data), np.max(data))
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
        "ave = %s, min = %s, max = %s" % (np.average(data), np.min(data), np.max(data))
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
        "ave = %s, min = %s, max = %s" % (np.average(data), np.min(data), np.max(data))
    )


async def test_trio_sleep(n, w):
    async with trio.open_nursery() as nursery:
        nursery.start_soon(_trio_sleep, n, w)


N = 100
W = 0.004

loop = asyncio.get_event_loop()
test_sleep(N, W)
test_async_sleep(N, W)
trio.run(test_trio_sleep, N, W)


loop.close()
