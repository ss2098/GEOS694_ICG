from mpi4py import MPI
import random


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


if size < 2:
    if rank == 0:
        print("Run with at least 2 processes.")
    raise SystemExit


if rank == 0:
    value = random.randint(1, 10)
    message_parts = ["hello world!", str(value)]
    comm.send((value, message_parts), dest=1)

    final_message = comm.recv(source=size - 1)
    print(" ".join(final_message))

elif rank == size - 1:
    value, message_parts = comm.recv(source=rank - 1)
    value *= rank
    message_parts.append(str(value))
    message_parts.append("goodbye world!")
    comm.send(message_parts, dest=0)

else:
    value, message_parts = comm.recv(source=rank - 1)
    value *= rank
    message_parts.append(str(value))
    comm.send((value, message_parts), dest=rank + 1)
