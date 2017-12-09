import numpy as np
import time

N = 8000

arr = []
A = np.random.random((N, N)).astype(np.float32)

for i in range(6):
    if i > 0:
        print(f'Test {i}...')
    st = time.time()
    B = np.dot(A, A)
    B[0,0]
    ed = time.time()
    dif = ed - st
    if i > 0:
        arr.append(dif)

avg = np.mean(arr)


print(f'{avg:.2f}s')

