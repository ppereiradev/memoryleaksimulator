import resource
from time import sleep
from concurrent.futures import ThreadPoolExecutor
import os

''' class to monitor the resident memory '''
class MemoryMonitor:
    def __init__(self):
        self.keep_measuring = True

    ''' it monitors the resident memory every 0.1 seconds '''
    def measure_usage(self):
        memory_usage_GiB = 0
        while self.keep_measuring:
            memory_usage_GiB = max(
                memory_usage_GiB,
                resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 2**10 / 2**30
            )
            # set the resident memory limit here
            if memory_usage_GiB > 10.0:
                os.kill(os.getpid(), 9)
            print(f"Memory usage GiB: {memory_usage_GiB}")
            sleep(0.1)

        return memory_usage_GiB

''' memory leak. it consumes around 750 MB per second of the resident memory. be careful, it can be savage '''
def memory_leak():
    l = [32.54e100] * 99999999
    while True:
        aux = l.copy()
        l.append(aux)
        sleep(1)



with ThreadPoolExecutor() as executor:
    monitor = MemoryMonitor()
    mem_thread = executor.submit(monitor.measure_usage)
    try:
        fn_thread = executor.submit(memory_leak)
        result = fn_thread.result()
    finally:
        monitor.keep_measuring = False
        memory_usage_GiB = mem_thread.result()
        
    print(f"Peak memory usage (GiB): {memory_usage_GiB}")
