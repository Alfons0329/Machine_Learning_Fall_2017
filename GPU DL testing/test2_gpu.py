import numpy as np
import time
import torch

N = 8000

arr = []
A = torch.randn(N, N).cuda()

for i in range(2000):
    print(f'Test {i}...')
    st = time.time()
    B = torch.mm(A, A)
    # print(B[0,0])
    B[0,0]
    ed = time.time()
    dif = ed - st
    arr.append(dif)

avg = np.mean(arr)


print(f'{avg:.2f}s')
