import time

def get_batch_and_sleep(speed: int):
    """1..100 speed -> (batch_size 1..50, sleep_time 0.1..0.0)
    Hız skalerini alıp animasyon için batch ve uyku süresi döndürür.
    """
    speed = max(1, min(100, int(speed)))
    batch_size = max(1, int(speed / 2))
    sleep_time = max(0.0, (100 - speed) / 1000.0)
    return batch_size, sleep_time


def sleep_if_needed(step_count: int, batch_size: int, sleep_time: float):
    if batch_size <= 0:
        return
    if step_count % batch_size == 0 and sleep_time > 0:
        time.sleep(sleep_time)
