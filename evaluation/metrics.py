
import time
import tracemalloc


def measure_performance(function, *args, **kwargs):
   

    tracemalloc.start()

    start_time = time.perf_counter()

    result = function(*args, **kwargs)

    end_time = time.perf_counter()

    current_memory, peak_memory = tracemalloc.get_traced_memory()

    tracemalloc.stop()

    peak_memory_mb = peak_memory / (1024 * 1024)

    execution_time = end_time - start_time

    metrics = {
        "execution_time": execution_time,
        "peak_memory_mb": peak_memory_mb
    }

    return result, metrics
