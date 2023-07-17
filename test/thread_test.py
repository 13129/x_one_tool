# -*- coding: utf-8 -*-
# @Time    : 2022/9/1 21:01
# @Author  : DivingKitten
# @desc    :
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

app = FastAPI()


def heavy_workload(job_id):
    n = 15000000
    while n > 0:
        n -= 1
    return f'Job id: {job_id} done!'


@app.get('/api/easy/{request_id}/{sleep}')
async def easy_workload(request_id: str, sleep: int):
    await asyncio.sleep(sleep)
    return JSONResponse(status_code=200, content={'result': f'Request: {request_id} done!'})


@app.get('/api/heavy_single/{n_jobs}')
async def run_single(n_jobs: int):
    results = []
    for i in range(n_jobs):
        results.append(heavy_workload(i))
    return JSONResponse(status_code=200, content={'result': results})


@app.get('/api/heavy_thread/{n_jobs}')
async def run_thread(n_jobs: int):
    with ThreadPoolExecutor() as executor:
        process = executor.map(heavy_workload, range(n_jobs))
        results = [p for p in process]
    return JSONResponse(status_code=200, content={'result': results})


@app.get('/api/heavy_process/{n_jobs}')
async def run_process(n_jobs: int):
    with ProcessPoolExecutor() as executor:
        process = executor.map(heavy_workload, range(n_jobs))
        results = [p for p in process]
    return JSONResponse(status_code=200, content={'result': results})

def get_thread_name():  # 查看当前线程名字
    import threading
    return threading.current_thread(), threading.active_count()


async def scrape(executors, jid, loop):
    results = await loop.run_in_executor(executors, funcd, jid)
    return results


def current_time():
    '''
    获取当前时间
    :return:
    '''
    cur_time = datetime.datetime.now()
    return str(cur_time)


def funcd(sleep_time):
    func_name_suffix = sleep_time  # 使用 sleep_time（函数 I/O 等待时长）作为函数名后缀，以区分任务对象
    name, count = get_thread_name()
    sleep(sleep_time)
    # print(f"[{current_time()}]{name}-数量-{count}")
    return f"【[{current_time()}] 得到函数 {funcd.__name__}-{func_name_suffix} 执行结果】"


@router.get("/api/add_tasks/1")
async def get_data():
    loop = asyncio.get_event_loop()
    print("--事件循环--", loop)
    crawlers = [i for i in range(1, 50)]
    tasks = []
    with ThreadPoolExecutor(50) as pool:
        for crawler in crawlers:
            tasks.append(loop.create_task(scrape(pool, crawler, loop=loop)))
        ingredients = await asyncio.gather(*tasks)
    return {"ingredients": "ok"}


@router.get("/api/add_tasks/2")
async def get_tasks():
    loop1 = asyncio.get_event_loop()
    print("--事件循环--", loop1)
    crawlers = [i for i in range(1, 50)]
    tasks = []
    with ThreadPoolExecutor(50) as pool:
        for crawler in crawlers:
            tasks.append(loop1.create_task(scrape(pool, crawler, loop=loop1)))
        ingredients = await asyncio.gather(*tasks)
    return {"ingredients": "ok"}


@router.get("/api/get_task/list")
async def get_tasks():
    workers = [creat_event_loop_thread(print_coro, 22, a=33) for _ in range(10)]
    start_threads(*workers)
    # join_threads(*workers)
    name, count = get_thread_name()
    thread_num = len(threading.enumerate())
    print(f"[{current_time()}]{name}-数量-{thread_num}")


async def print_coro(*args, **kwargs):
    print(f'Inside the print coro on {threading.get_ident()}', (args, kwargs))


def creat_event_loop_thread(worker, *args, **kwargs):
    """"""

    def _worker(*args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(worker(*args, **kwargs))
        finally:
            loop.close()

    return threading.Thread(target=_worker, args=args, kwargs=kwargs)


def start_threads(*threads):
    [thread.start() for thread in threads if isinstance(thread, threading.Thread)]


def join_threads(*threads):
    [thread.join() for thread in threads if isinstance(thread, threading.Thread)]
