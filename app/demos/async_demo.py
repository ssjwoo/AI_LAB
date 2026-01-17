import asyncio
import time


async def fetch_io(task_id: int) -> int:
    await asyncio.sleep(0.5)
    return task_id


async def run_sequential(n: int) -> float:
    start = time.perf_counter()
    for i in range(n):
        await fetch_io(i)
    return time.perf_counter() - start


async def run_parallel_bounded(n: int, limit: int = 10) -> float:
    sem = asyncio.Semaphore(limit)

    async def worker(i: int) -> int:
        async with sem:
            return await fetch_io(i)

    start = time.perf_counter()
    await asyncio.gather(*(worker(i) for i in range(n)))
    return time.perf_counter() - start


async def demo_async():
    n = 30
    limit = 10

    t1 = await run_sequential(n)
    t2 = await run_parallel_bounded(n, limit=limit)

    print(f"[ASYNC DEMO] sequential: n={n} -> {t1:.2f}s")
    print(f"[ASYNC DEMO] parallel(bounded): n={n}, limit={limit} -> {t2:.2f}s")