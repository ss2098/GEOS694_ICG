from mpi4py import MPI
import random


comm = MPI.COMM_WORLD
rank = comm.Get_rank()


local_value = random.randint(0, 1000)
global_max = comm.reduce(local_value, op=MPI.MAX, root=0)
global_max = comm.bcast(global_max, root=0)


if local_value == global_max:
    print(
        f"Rank {rank} has value {local_value} "
        f"which is the global max {global_max}"
    )
else:
    print(
        f"Rank {rank} has value {local_value} "
        f"which is less than global max {global_max}"
    )
