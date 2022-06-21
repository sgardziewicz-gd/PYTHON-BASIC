import multiprocessing
import os
from random import randint
from multiprocessing import Pool
import time
import csv
import concurrent.futures


OUTPUT_DIR = './output'
RESULT_FILE = './output/result.csv'


def fib(n: int):
    """Calculate a value in the Fibonacci sequence by ordinal number"""

    f0, f1 = 0, 1
    for _ in range(n-1):
        f0, f1 = f1, f0 + f1
    return f1


def func1(array: list):
    with Pool(multiprocessing.cpu_count()) as p:
        p.map(calc, array)

def calc(number: int):
    with open(f'{OUTPUT_DIR}/{number}.txt', 'w') as f:
        f.write(str(fib(number)))

def read(filename: str):
    path = f'{OUTPUT_DIR}/{filename}'
    with open(path, 'r') as f:
        num = f.readline()
    return [filename.strip('.txt'), num]

def func2(result_file: str):
    files = os.listdir(OUTPUT_DIR)
    data = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        futures = {executor.submit(read, file) for file in files}
        
        for fut in concurrent.futures.as_completed(futures):
            data.append(fut.result())

    write_csv(data, result_file)


def write_csv(data, path):
    with open(path, 'w+') as f:
        write = csv.writer(f)
        write.writerows(reversed(data))


if __name__ == '__main__':
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    func1([randint(1000, 100000) for _ in range(500)])
    start_time = time.time()
    func2(result_file=RESULT_FILE)
    print(" --- %s seconds" % (time.time() - start_time))

#--func2
#for each                         ---- 0.75
#256 workers threadpool range 500  --- 0.4
#64 workers threadpool range 500  --- 0.4
#16 workers threadpool range 500    --- 0.37
#8 workers threadpool range 500    --- 0.39

#8 cpu processing 500             ---- 0.72

