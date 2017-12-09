import numpy as np
import time

N = 8000

arr = []
A = np.random.random((N, N))

for i in range(4):
    if i > 0:
        print(f'Test {i}...')
    st = time.time()
    B = np.dot(A, A)
    ed = time.time()
    dif = ed - st
    if i > 0:
        arr.append(dif)

avg = np.mean(arr)


print(f'{avg:.2f}s')
