from mpi4py import MPI
import numpy as np
import sys


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


if len(sys.argv) > 1:
    n_value = int(sys.argv[1])
else:
    n_value = 10


if rank == 0:
    data = np.arange(1, n_value + 1, dtype=int)
    remainder = len(data) % size

    if remainder != 0:
        pad_width = size - remainder
        data = np.concatenate([data, np.zeros(pad_width, dtype=int)])

    chunks = np.array_split(data, size)
else:
    chunks = None


local_chunk = comm.scatter(chunks, root=0)
local_sum = int(np.sum(local_chunk))
all_sums = comm.gather(local_sum, root=0)


if rank == 0:
    distributed_sum = sum(all_sums)
    check_sum = n_value * (n_value + 1) // 2
    print(f"The sum of 1-{n_value} is {distributed_sum} == {check_sum}.")
