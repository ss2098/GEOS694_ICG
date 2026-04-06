from mpi4py import MPI
import numpy as np


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


if rank == 0:
    matrix_a = np.random.randint(0, 10, size=(size, size))
    vector_x = np.random.randint(0, 10, size=size)
    rows = [matrix_a[index, :] for index in range(size)]
else:
    matrix_a = None
    vector_x = None
    rows = None


local_row = comm.scatter(rows, root=0)
vector_x = comm.bcast(vector_x, root=0)

local_y = int(np.dot(local_row, vector_x))

comm.Barrier()

send_buffer = np.array(local_y, dtype="i")

if rank == 0:
    receive_buffer = np.empty(size, dtype="i")
else:
    receive_buffer = None


request = comm.Igather(send_buffer, receive_buffer, root=0)
request.Wait()


if rank == 0:
    print("Matrix A:")
    print(matrix_a)
    print()

    print("Vector x:")
    print(vector_x)
    print()

    print("Result vector y = A * x:")
    print(receive_buffer)
    print()

    print("Row-by-row output:")
    vector_str = " ".join(f"{value:3d}" for value in vector_x)

    for index in range(size):
        row_str = " ".join(f"{value:3d}" for value in matrix_a[index])
        print(f"[{row_str}] dot [{vector_str}] = {receive_buffer[index]}")
