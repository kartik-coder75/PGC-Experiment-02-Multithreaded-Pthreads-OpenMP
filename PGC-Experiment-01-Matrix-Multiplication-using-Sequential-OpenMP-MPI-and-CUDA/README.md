## Experiment 1: Matrix Multiplication using Sequential, OpenMP, MPI and CUDA

This experiment implements matrix multiplication using four different computing approaches:

1. Sequential CPU execution
2. OpenMP shared-memory parallelism
3. MPI distributed-memory parallelism
4. CUDA GPU parallelism

The same matrix multiplication problem is solved using all four methods and their execution times and speedups are compared.

---

# 1. Problem Definition

Two matrices `A` and `B` of size **4000 × 4000** are considered.

All elements of both matrices are initialized to `1.0`.

The matrix multiplication is:

```text
C = A × B
```

For every element:

```text
C[i][j] = Σ A[i][k] × B[k][j]
```

Since all elements of `A` and `B` are `1.0`, the expected value is:

```text
C[0][0] = 4000.00
```

The same result is verified for all four implementations.

---

# 2. System and Software Requirements

## Hardware

* CPU capable of running multi-threaded programs
* NVIDIA GPU for CUDA implementation
* NVIDIA RTX 4500 Ada Generation GPU used for the CUDA experiment
* Multiple virtual machines for the MPI experiment

## Software

* Windows 10/11
* WSL2 Ubuntu
* GCC / build-essential
* OpenMP support through GCC
* Open MPI
* OpenSSH
* CUDA Toolkit
* `nvcc` CUDA compiler
* VMware or equivalent virtualization software

---

# 3. Part A - Sequential Matrix Multiplication

## Objective

The sequential implementation performs matrix multiplication using a single CPU execution path without any parallel processing.

This implementation is used as the **baseline** for calculating speedup of the other methods.

---

## Step 1: Open Ubuntu / WSL Terminal

Open the Ubuntu terminal through WSL2.

Check that GCC is available:

```bash
gcc --version
```

If GCC is not installed:

```bash
sudo apt update
sudo apt install build-essential
```

---

## Step 2: Create the Sequential Program

Create a C program for sequential matrix multiplication.

The program:

* Creates two `4000 × 4000` matrices.
* Initializes all elements to `1.0`.
* Performs matrix multiplication using normal nested loops.
* Measures execution time.
* Prints the verification value `C[0][0]`.

The basic multiplication operation is:

```c
for (i = 0; i < N; i++)
{
    for (j = 0; j < N; j++)
    {
        for (k = 0; k < N; k++)
        {
            C[i][j] += A[i][k] * B[k][j];
        }
    }
}
```

---

## Step 3: Compile the Program

Compile the sequential program using GCC:

```bash
gcc sequential.c -o sequential
```

---

## Step 4: Run the Program

Run the executable:

```bash
./sequential
```

The program displays the execution time and verification result.

Expected verification:

```text
C[0][0] = 4000.00
```

---

## Step 5: Record the Execution Time

The measured sequential execution time was:

```text
244.120000 seconds
```

This value is taken as the baseline execution time.

Therefore:

```text
Sequential Speedup = 244.120000 / 244.120000
                   = 1.00×
```

---

# 4. Part B - OpenMP Matrix Multiplication

## Objective

OpenMP is used to parallelize matrix multiplication using multiple CPU threads.

Unlike the sequential implementation, multiple CPU threads perform matrix calculations simultaneously.

The experiment uses:

```text
8 OpenMP threads
```

---

## Step 1: Check the Number of CPU Cores

Run:

```bash
nproc
```

This displays the number of available processing units.

---

## Step 2: Create the OpenMP Program

The sequential matrix multiplication code is modified to use OpenMP.

The outer loop is parallelized using:

```c
#pragma omp parallel for
```

This allows different iterations of the loop to be executed by different threads.

Example:

```c
#pragma omp parallel for
for (i = 0; i < N; i++)
{
    for (j = 0; j < N; j++)
    {
        for (k = 0; k < N; k++)
        {
            C[i][j] += A[i][k] * B[k][j];
        }
    }
}
```

---

## Step 3: Set the Number of Threads

Set OpenMP to use 8 threads:

```bash
export OMP_NUM_THREADS=8
```

Check the value:

```bash
echo $OMP_NUM_THREADS
```

Expected output:

```text
8
```

---

## Step 4: Compile the OpenMP Program

OpenMP support is enabled using the `-fopenmp` option:

```bash
gcc -fopenmp openmp.c -o openmp
```

---

## Step 5: Run the Program

Run:

```bash
./openmp
```

The program performs matrix multiplication using 8 CPU threads.

---

## Step 6: Monitor CPU Usage

The CPU usage can be observed using:

```bash
htop
```

This helps to observe multiple CPU threads being used during execution.

---

## Step 7: Record the Result

The measured execution time was:

```text
30.830434 seconds
```

Verification:

```text
C[0][0] = 4000.00
```

Speedup:

```text
Speedup = Sequential Time / OpenMP Time

        = 244.120000 / 30.830434

        = 7.92×
```

---

# 5. Part C - MPI Distributed Matrix Multiplication

## Objective

MPI (Message Passing Interface) is used to perform distributed-memory parallel matrix multiplication.

Instead of using multiple threads in one process, MPI uses multiple processes.

For this experiment:

```text
4 MPI processes
4 virtual machines
1 Master + 3 Workers
```

are used.

---

# 5.1 MPI Environment Setup

## Step 1: Install Open MPI

Install MPI and SSH:

```bash
sudo apt update
sudo apt install openmpi-bin openmpi-common libopenmpi-dev openssh-server
```

Check MPI installation:

```bash
mpirun --version
```

---

## Step 2: Configure the MPI Machines

The MPI experiment uses four machines:

```text
Master
Worker 1
Worker 2
Worker 3
```

Each machine must be able to communicate with the others.

---

## Step 3: Check Network Connectivity

Find the IP address of a machine using:

```bash
ip addr
```

or:

```bash
hostname -I
```

Test connectivity between machines using:

```bash
ping <IP_ADDRESS>
```

The machines should be able to communicate with each other.

---

## Step 4: Configure SSH

MPI uses SSH to launch processes on remote machines.

Start the SSH service:

```bash
sudo service ssh start
```

Test SSH connectivity:

```bash
ssh username@worker_ip
```

Passwordless SSH can also be configured so that MPI can start processes without repeatedly asking for a password.

---

# 5.2 MPI Program

The sequential matrix multiplication is modified to distribute work between MPI processes.

The matrix rows are divided among the available processes.

For example, with 4 processes:

```text
Process 0 → Part of matrix rows
Process 1 → Part of matrix rows
Process 2 → Part of matrix rows
Process 3 → Part of matrix rows
```

The processes perform their assigned calculations in parallel.

MPI communication functions are used to distribute data and collect results.

Important MPI operations include:

```c
MPI_Init()
MPI_Comm_rank()
MPI_Comm_size()
MPI_Bcast()
MPI_Scatter()
MPI_Gather()
MPI_Finalize()
```

---

## Step 1: Compile the MPI Program

Use `mpicc`:

```bash
mpicc mpi_matrix.c -o mpi_matrix
```

---

## Step 2: Run Using 4 Processes

Run:

```bash
mpirun -np 4 ./mpi_matrix
```

For a multi-machine setup, the host configuration is used to specify the master and worker machines.

---

## Step 3: Observe the MPI Execution

The processes perform matrix multiplication simultaneously.

The master process distributes the required matrix data and collects the calculated results from worker processes.

---

## Step 4: Verify the Result

The calculated result is verified using:

```text
C[0][0] = 4000.00
```

This confirms that the distributed computation produces the same mathematical result as the sequential implementation.

---

## Step 5: Record the Execution Time

The measured MPI execution time was:

```text
92.979510 seconds
```

Speedup:

```text
Speedup = Sequential Time / MPI Time

        = 244.120000 / 92.979510

        = 2.63×
```

---

# 6. Part D - CUDA Matrix Multiplication

## Objective

CUDA is used to perform matrix multiplication on an NVIDIA GPU.

The GPU can execute a very large number of threads simultaneously, making it suitable for highly parallel operations such as matrix multiplication.

The GPU used for this experiment was:

```text
NVIDIA RTX 4500 Ada Generation
```

---

# 6.1 CUDA Environment Setup

## Step 1: Check NVIDIA GPU

Run:

```bash
nvidia-smi
```

This displays information about the installed NVIDIA GPU.

---

## Step 2: Check CUDA Compiler

Run:

```bash
nvcc --version
```

This verifies that the CUDA compiler is installed.

---

## Step 3: Create the CUDA Program

The matrix multiplication is implemented using a CUDA kernel.

Each CUDA thread calculates one element of the output matrix.

Conceptually:

```text
One CUDA thread → One C[i][j] element
```

The kernel performs:

```text
C[row][col] = Σ A[row][k] × B[k][col]
```

---

# 6.2 CUDA Grid and Block Configuration

The experiment uses:

```text
Block size = 16 × 16
Grid size  = 250 × 250
```

Since:

```text
250 × 16 = 4000
```

the grid covers the complete `4000 × 4000` matrix.

---

## Step 1: Compile the CUDA Program

Use the NVIDIA CUDA compiler:

```bash
nvcc matrix_cuda.cu -o matrix_cuda
```

---

## Step 2: Run the CUDA Program

Run:

```bash
./matrix_cuda
```

The program transfers the matrices to the GPU, launches the CUDA kernel, performs the multiplication, and transfers the result back.

---

## Step 3: Verify the Result

The result is checked using:

```text
C[0][0] = 4000.00
```

---

## Step 4: Record CUDA Execution Time

Measured CUDA kernel execution time:

```text
0.146443 seconds
```

Total CUDA phase:

```text
0.165004 seconds
```

The total CUDA time is used for comparison with the other implementations.

---

## Step 5: Calculate CUDA Speedup

```text
Speedup = Sequential Time / CUDA Time

        = 244.120000 / 0.165004

        = 1479.48×
```

---

# 7. Performance Results

The following table summarizes the measured results.

| Method     | Computing Model      | Configuration       | Execution Time |  Speedup |
| ---------- | -------------------- | ------------------- | -------------: | -------: |
| Sequential | Single CPU execution | 1 CPU core          |   244.120000 s |    1.00× |
| OpenMP     | Shared memory        | 8 CPU threads       |    30.830434 s |    7.92× |
| MPI        | Distributed memory   | 4 processes / 4 VMs |    92.979510 s |    2.63× |
| CUDA       | GPU parallelism      | NVIDIA RTX 4500 Ada |     0.165004 s | 1479.48× |

---

# 8. Speedup Calculation

Speedup is calculated using:

```text
Speedup = Sequential Execution Time / Parallel Execution Time
```

For example, OpenMP:

```text
Speedup = 244.120000 / 30.830434
        = 7.92×
```

For MPI:

```text
Speedup = 244.120000 / 92.979510
        = 2.63×
```

For CUDA:

```text
Speedup = 244.120000 / 0.165004
        = 1479.48×
```

---

# 9. Comparison of the Four Methods

## Sequential

The sequential method executes the complete matrix multiplication using a single CPU execution path.

It has no parallel overhead and is simple to implement, but the entire workload is processed sequentially.

It required:

```text
244.120000 seconds
```

and is therefore used as the baseline.

---

## OpenMP

OpenMP divides the work among multiple CPU threads.

Using 8 threads reduced the execution time from the sequential baseline to:

```text
30.830434 seconds
```

The measured speedup was:

```text
7.92×
```

OpenMP uses shared memory and therefore does not require the communication between separate machines used in the MPI experiment.

---

## MPI

MPI distributes the computation among multiple processes and machines.

The experiment used:

```text
4 processes
4 virtual machines
```

The measured execution time was:

```text
92.979510 seconds
```

with a speedup of:

```text
2.63×
```

The MPI implementation involves communication between processes and machines, which adds overhead to the computation.

---

## CUDA

CUDA executes the matrix multiplication on the NVIDIA GPU.

The experiment used:

```text
NVIDIA RTX 4500 Ada Generation
Grid: 250 × 250
Block: 16 × 16
```

The total CUDA phase took:

```text
0.165004 seconds
```

with a measured speedup of:

```text
1479.48×
```

The CUDA implementation achieved the smallest measured execution time in this experiment.

---

# 10. Overall Comparison

| Feature                | Sequential       | OpenMP               | MPI                                         | CUDA                              |
| ---------------------- | ---------------- | -------------------- | ------------------------------------------- | --------------------------------- |
| Processing Unit        | CPU              | CPU                  | CPU / Multiple Processes                    | GPU                               |
| Parallelism            | No               | Thread-level         | Process-level                               | Massive GPU parallelism           |
| Memory Model           | Single execution | Shared memory        | Distributed memory                          | GPU memory                        |
| Configuration          | 1 CPU core       | 8 CPU threads        | 4 processes / 4 VMs                         | RTX 4500 Ada                      |
| Execution Time         | 244.120000 s     | 30.830434 s          | 92.979510 s                                 | 0.165004 s                        |
| Speedup                | 1.00×            | 7.92×                | 2.63×                                       | 1479.48×                          |
| Communication Overhead | None             | Low                  | Higher due to process/network communication | GPU data transfer/kernel overhead |
| Main Advantage         | Simple baseline  | Easy CPU parallelism | Distributed computation                     | Very high parallel performance    |

---

# 11. Observations

1. The sequential implementation provides the baseline execution time of `244.120000 seconds`.

2. OpenMP reduces the execution time by using 8 CPU threads simultaneously.

3. The measured OpenMP speedup is `7.92×`.

4. MPI distributes the workload between multiple processes and virtual machines.

5. MPI has additional communication and virtualization/network overhead, resulting in a measured speedup of `2.63×`.

6. CUDA provides a highly parallel GPU implementation.

7. The measured CUDA execution time is `0.165004 seconds`.

8. The measured CUDA speedup is `1479.48×` compared with the sequential execution.

9. All four implementations produce the same verification result:

```text
C[0][0] = 4000.00
```

10. The experiment demonstrates the difference between sequential execution, shared-memory CPU parallelism, distributed-memory parallelism, and GPU-based parallelism.

---

# 12. Screenshots

Screenshots for the experiment are included in this repository.

The screenshots cover the execution and output of the experiment, including:

* Sequential implementation
* OpenMP implementation
* MPI implementation
* CUDA implementation
* Compilation and execution commands
* Verification output
* Performance results

---

# 13. Final Conclusion

This experiment demonstrates matrix multiplication using four different computing approaches: Sequential, OpenMP, MPI, and CUDA.

The sequential method provides the baseline for performance comparison. OpenMP improves CPU performance by using multiple threads, while MPI distributes computation among multiple processes and machines. CUDA uses GPU parallelism to execute a very large number of operations simultaneously.

For the tested `4000 × 4000` matrix multiplication, the measured execution times were:

```text
Sequential : 244.120000 seconds
OpenMP     : 30.830434 seconds
MPI        : 92.979510 seconds
CUDA       : 0.165004 seconds
```

The corresponding measured speedups were:

```text
Sequential : 1.00×
OpenMP     : 7.92×
MPI        : 2.63×
CUDA       : 1479.48×
```

All implementations produced the expected verification result:

```text
C[0][0] = 4000.00
```

Thus, the experiment provides a practical comparison of sequential CPU execution, shared-memory parallelism, distributed-memory parallelism, and GPU-based parallel computing.
