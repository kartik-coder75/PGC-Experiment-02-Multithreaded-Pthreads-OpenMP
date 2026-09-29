# Experiment 2: Multithreaded Programming Using Pthreads and OpenMP

**Develop multithreaded programs using parallel programming libraries to understand thread creation, management, and coordination.**

---

## Table of Contents

1. [Aim](#1-aim)
2. [Basic Idea of the Experiment](#2-basic-idea-of-the-experiment)
3. [Software Environment](#3-software-environment)
4. [Setup (WSL, Lab Directory, GCC, OpenMP)](#4-setup)
5. [Part A: Pthreads](#part-a--pthreads)
6. [Part B: OpenMP](#part-b--openmp)
7. [Part C: Performance Analysis](#part-c--performance-analysis)
8. [Quick Difference: Pthreads vs OpenMP](#19-quick-difference--pthreads-vs-openmp)
9. [Important Terms](#20-important-terms)
10. [Implemented Programs](#21-implemented-programs)
11. [Complete Learning Flow](#22-complete-learning-flow)
12. [Conclusion](#23-conclusion)

---

## 1. Aim

To develop multithreaded programs using **Pthreads and OpenMP** and understand:

- Thread creation
- Thread management
- Work distribution
- Race conditions
- Synchronization
- Thread coordination
- Performance improvement using multiple threads

---

## 2. Basic Idea of the Experiment

A **thread** is an execution path inside a program. Think of a thread as a **worker**.

### Sequential Program

```text
One worker
    |
    |---- Task 1
    |---- Task 2
    |---- Task 3
    |---- Task 4
    |---- ...
```

One thread performs all the work.

### Multithreaded Program

```text
                 Program
                    |
          ---------------------
          |     |      |      |
       Thread1 Thread2 Thread3 Thread4
          |     |      |      |
        Work   Work   Work   Work
```

Several threads can work on different parts of the problem. That is the basic idea of **parallel programming**.

This experiment uses two technologies:

- **Pthreads**
- **OpenMP**

The final part measures whether increasing the number of threads reduces execution time.

---

## 3. Software Environment

- Windows
- WSL Ubuntu
- GCC compiler
- Pthreads
- OpenMP
- Nano editor

---

## 4. Setup

### 4.1 Start WSL

1. Press the **Windows key** and search for **PowerShell**.
2. Click **Windows PowerShell**. You should see:

```text
PS C:\WINDOWS\system32>
```

3. Start WSL:

```powershell
wsl
```

Expected prompt (your username and computer name may differ):

```text
powerx@DESKTOP-5MP543G:~$
```

**What are we doing?** We are leaving Windows PowerShell and entering the Linux environment where the C programs will be created and executed.

### 4.2 Create the lab directory

```bash
mkdir -p ~/parallel_lab
cd ~/parallel_lab
pwd
```

Expected:

```text
/home/powerx/parallel_lab
```

`parallel_lab` is the folder where all the C programs for this experiment are stored.

### 4.3 Check GCC

```bash
gcc --version
```

Expected output shows the installed GCC version, for example:

```text
gcc (Ubuntu ...) ...
```

### 4.4 Check OpenMP support

```bash
gcc -fopenmp --version
```

The `-fopenmp` option enables OpenMP support when compiling C programs.

> **Saving files in Nano:** press `Ctrl + O`, then `Enter` to save, then `Ctrl + X` to exit. This applies to every program below.

---

# Part A: Pthreads

Pthreads stands for **POSIX Threads**. With Pthreads, threads are explicitly created and managed. The main functions used are:

```c
pthread_create()
pthread_join()
pthread_mutex_lock()
pthread_mutex_unlock()
```

## Step 1: Create One Thread

**Objective:** Learn how to create a thread, how the new thread executes a function, and how the main thread waits for the new thread.

Create the file:

```bash
nano thread1.c
```

Paste this program:

```c
#include <stdio.h>
#include <pthread.h>

void *thread_function(void *arg)
{
    printf("Hello from the thread!\n");
    return NULL;
}

int main()
{
    pthread_t thread;

    pthread_create(&thread, NULL, thread_function, NULL);

    pthread_join(thread, NULL);

    printf("Main thread finished.\n");

    return 0;
}
```

Compile and run:

```bash
gcc thread1.c -o thread1 -pthread
./thread1
```

Expected output:

```text
Hello from the thread!
Main thread finished.
```

### What did we just do?

**`pthread_t thread;`** creates a variable that stores the **thread identifier**. It does not create the thread by itself.

**`pthread_create(&thread, NULL, thread_function, NULL);`** actually creates the **additional thread**. When the program starts, the main thread already exists.

```text
Before pthread_create():

Main Thread
     |
   main()

After pthread_create():

             Program
             /     \
            /       \
     Main Thread   New Thread
         |             |
       main()    thread_function()
```

One execution of `pthread_create()` creates one additional thread:

```text
1 main thread + 1 additional thread = 2 threads
```

**How did the new thread know what to execute?** We passed `thread_function` to `pthread_create()`, so the new thread starts executing that function:

```text
pthread_create()
       |
       v
New thread created
       |
       v
thread_function()
       |
       v
Hello from the thread!
```

**`pthread_join(thread, NULL);`** tells the main thread to wait until the created thread finishes.

```text
pthread_create() -> CREATE
pthread_join()   -> WAIT
```

---

## Step 2: Create Multiple Threads

```bash
nano thread2.c
```

```c
#include <stdio.h>
#include <pthread.h>

void *thread_function(void *arg)
{
    int thread_id = *(int *)arg;

    printf("Hello from Thread %d\n", thread_id);

    return NULL;
}

int main()
{
    pthread_t threads[4];
    int thread_ids[4];

    for (int i = 0; i < 4; i++)
    {
        thread_ids[i] = i + 1;

        pthread_create(
            &threads[i],
            NULL,
            thread_function,
            &thread_ids[i]
        );
    }

    for (int i = 0; i < 4; i++)
    {
        pthread_join(threads[i], NULL);
    }

    printf("All threads have finished.\n");

    return 0;
}
```

```bash
gcc thread2.c -o thread2 -pthread
./thread2
```

Expected output may look like this:

```text
Hello from Thread 1
Hello from Thread 2
Hello from Thread 4
Hello from Thread 3
All threads have finished.
```

Your order may be different, for example:

```text
Hello from Thread 3
Hello from Thread 1
Hello from Thread 4
Hello from Thread 2
All threads have finished.
```

Both are acceptable.

### What are we learning?

The loop calls `pthread_create()` four times:

```text
1st execution -> Thread 1
2nd execution -> Thread 2
3rd execution -> Thread 3
4th execution -> Thread 4
```

So we create **4 additional threads** (plus the original main thread).

**Why is the output order different?** The operating system schedules the threads. We cannot assume `1 -> 2 -> 3 -> 4`.

> **Thread execution order is not guaranteed.**

---

## Step 3: Divide Work Among Threads

Now we use threads to perform actual useful work. The array is:

```text
10 20 30 40 50 60 70 80
```

The work is divided into four parts, one per thread.

```bash
nano thread_sum.c
```

```c
#include <stdio.h>
#include <pthread.h>

#define NUM_THREADS 4
#define ARRAY_SIZE 8

int array[ARRAY_SIZE] = {10, 20, 30, 40, 50, 60, 70, 80};

int partial_sum[NUM_THREADS];

void *calculate_sum(void *arg)
{
    int thread_id = *(int *)arg;

    int start = thread_id * (ARRAY_SIZE / NUM_THREADS);
    int end = start + (ARRAY_SIZE / NUM_THREADS);

    partial_sum[thread_id] = 0;

    for (int i = start; i < end; i++)
    {
        partial_sum[thread_id] += array[i];
    }

    printf("Thread %d calculated sum = %d\n",
           thread_id + 1,
           partial_sum[thread_id]);

    return NULL;
}

int main()
{
    pthread_t threads[NUM_THREADS];
    int thread_ids[NUM_THREADS];

    for (int i = 0; i < NUM_THREADS; i++)
    {
        thread_ids[i] = i;

        pthread_create(
            &threads[i],
            NULL,
            calculate_sum,
            &thread_ids[i]
        );
    }

    for (int i = 0; i < NUM_THREADS; i++)
    {
        pthread_join(threads[i], NULL);
    }

    int total_sum = 0;

    for (int i = 0; i < NUM_THREADS; i++)
    {
        total_sum += partial_sum[i];
    }

    printf("Total sum = %d\n", total_sum);

    return 0;
}
```

```bash
gcc thread_sum.c -o thread_sum -pthread
./thread_sum
```

Expected output (the order of the four thread messages may change):

```text
Thread 1 calculated sum = 30
Thread 2 calculated sum = 70
Thread 3 calculated sum = 110
Thread 4 calculated sum = 150
Total sum = 360
```

### What are we doing here?

Instead of one thread calculating `10 + 20 + 30 + 40 + 50 + 60 + 70 + 80`, we divide the work:

```text
Thread 1 -> 10 + 20 = 30
Thread 2 -> 30 + 40 = 70
Thread 3 -> 50 + 60 = 110
Thread 4 -> 70 + 80 = 150

30 + 70 + 110 + 150 = 360
```

This is called **work distribution**: the large problem is divided into smaller pieces.

---

## Step 4: Demonstrate a Race Condition

Now we deliberately create a problem. Several threads will modify the same variable using `counter++;`.

```bash
nano race.c
```

```c
#include <stdio.h>
#include <pthread.h>

#define NUM_THREADS 4
#define INCREMENTS 100000

int counter = 0;

void *increment_counter(void *arg)
{
    for (int i = 0; i < INCREMENTS; i++)
    {
        counter++;
    }

    return NULL;
}

int main()
{
    pthread_t threads[NUM_THREADS];

    for (int i = 0; i < NUM_THREADS; i++)
    {
        pthread_create(
            &threads[i],
            NULL,
            increment_counter,
            NULL
        );
    }

    for (int i = 0; i < NUM_THREADS; i++)
    {
        pthread_join(threads[i], NULL);
    }

    printf("Expected counter = %d\n",
           NUM_THREADS * INCREMENTS);

    printf("Actual counter   = %d\n",
           counter);

    return 0;
}
```

```bash
gcc race.c -o race -pthread
./race
```

You may get:

```text
Expected counter = 400000
Actual counter   = 167739
```

Run it again and you may get a different value:

```text
Expected counter = 400000
Actual counter   = 131342
```

### Why is the result wrong?

Four threads each perform 100000 increments, so theoretically `4 x 100000 = 400000`. But all four threads modify the same variable. Imagine `counter = 10`:

```text
Thread 1 -> reads 10
Thread 2 -> reads 10

Thread 1 -> writes 11
Thread 2 -> writes 11
```

We wanted `12` but got `11`. One update was lost. This is a **race condition**: multiple threads access and modify the same shared data at the same time.

---

## Step 5: Fix the Race Condition Using a Mutex

We now protect the shared variable using a mutex.

```bash
nano mutex.c
```

```c
#include <stdio.h>
#include <pthread.h>

#define NUM_THREADS 4
#define INCREMENTS 100000

int counter = 0;

pthread_mutex_t mutex;

void *increment_counter(void *arg)
{
    for (int i = 0; i < INCREMENTS; i++)
    {
        pthread_mutex_lock(&mutex);

        counter++;

        pthread_mutex_unlock(&mutex);
    }

    return NULL;
}

int main()
{
    pthread_t threads[NUM_THREADS];

    pthread_mutex_init(&mutex, NULL);

    for (int i = 0; i < NUM_THREADS; i++)
    {
        pthread_create(
            &threads[i],
            NULL,
            increment_counter,
            NULL
        );
    }

    for (int i = 0; i < NUM_THREADS; i++)
    {
        pthread_join(threads[i], NULL);
    }

    pthread_mutex_destroy(&mutex);

    printf("Expected counter = %d\n",
           NUM_THREADS * INCREMENTS);

    printf("Actual counter   = %d\n",
           counter);

    return 0;
}
```

```bash
gcc mutex.c -o mutex -pthread
./mutex
```

Expected output:

```text
Expected counter = 400000
Actual counter   = 400000
```

### What are we doing here?

The important part is:

```c
pthread_mutex_lock(&mutex);
counter++;
pthread_mutex_unlock(&mutex);
```

Think of a mutex as a **key**. Only one thread can enter the protected section at a time:

```text
Thread 1 -> lock -> counter++ -> unlock
Thread 2 -> lock -> counter++ -> unlock
Thread 3 -> lock -> counter++ -> unlock
Thread 4 -> lock -> counter++ -> unlock
```

Therefore the shared counter is protected.

---

# Part B: OpenMP

Pthreads gives more manual control. OpenMP provides a higher-level approach where directives such as the following are used for parallel execution and coordination:

```c
#pragma omp parallel
#pragma omp parallel for
#pragma omp critical
#pragma omp barrier
```

## Step 6: OpenMP Basic Parallel Region

**Objective:** Learn how OpenMP creates a group of threads, how to identify the current thread, and how to determine the total number of threads.

```bash
nano omp1.c
```

```c
#include <stdio.h>
#include <omp.h>

int main()
{
    #pragma omp parallel
    {
        int thread_id = omp_get_thread_num();
        int total_threads = omp_get_num_threads();

        printf("Hello from Thread %d of %d\n",
               thread_id,
               total_threads);
    }

    return 0;
}
```

```bash
gcc omp1.c -o omp1 -fopenmp
./omp1
```

Your output may contain many lines such as:

```text
Hello from Thread 18 of 32
Hello from Thread 13 of 32
Hello from Thread 19 of 32
...
Hello from Thread 0 of 32
```

On the system used for this experiment, OpenMP used **32 threads** for this program. The exact order may change, and the thread count depends on your machine.

### What are we learning?

- `#pragma omp parallel` means: execute the following block using multiple OpenMP threads.
- `omp_get_thread_num()` asks: *Which thread am I?*
- `omp_get_num_threads()` asks: *How many threads are in this parallel team?*

OpenMP lets us create a **parallel region** without explicitly calling `pthread_create()` ourselves.

---

## Step 7: OpenMP Work Sharing

Now we want OpenMP to divide work automatically.

```bash
nano omp_sum.c
```

```c
#include <stdio.h>
#include <omp.h>

#define ARRAY_SIZE 8

int array[ARRAY_SIZE] = {10, 20, 30, 40, 50, 60, 70, 80};

int main()
{
    int total_sum = 0;

    #pragma omp parallel for reduction(+:total_sum)
    for (int i = 0; i < ARRAY_SIZE; i++)
    {
        int thread_id = omp_get_thread_num();

        printf("Thread %d processing array[%d] = %d\n",
               thread_id,
               i,
               array[i]);

        total_sum += array[i];
    }

    printf("Total sum = %d\n", total_sum);

    return 0;
}
```

```bash
gcc omp_sum.c -o omp_sum -fopenmp
./omp_sum
```

Expected output contains lines such as the following (order can vary):

```text
Thread 5 processing array[5] = 60
Thread 7 processing array[7] = 80
Thread 0 processing array[0] = 10
...
Total sum = 360
```

### What does `parallel for` mean?

`#pragma omp parallel for` tells OpenMP to divide the loop iterations among the available threads.

```text
Sequential:   One thread: 0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7

OpenMP:       Thread 0 -> some iterations
              Thread 1 -> some iterations
              Thread 2 -> some iterations
              ...
```

### What does `reduction(+:total_sum)` mean?

Each thread calculates a partial result, and OpenMP safely combines them:

```text
Thread 1 -> partial sum
Thread 2 -> partial sum
Thread 3 -> partial sum
Thread 4 -> partial sum
          |
          v
     OpenMP combines
          |
          v
      total_sum
```

---

## Step 8: OpenMP Race Condition

Now we deliberately create the same race condition in OpenMP.

```bash
nano omp_race.c
```

```c
#include <stdio.h>
#include <omp.h>

#define NUM_THREADS 4
#define INCREMENTS 100000

int counter = 0;

int main()
{
    omp_set_num_threads(NUM_THREADS);

    #pragma omp parallel
    {
        for (int i = 0; i < INCREMENTS; i++)
        {
            counter++;
        }
    }

    printf("Expected counter = %d\n",
           NUM_THREADS * INCREMENTS);

    printf("Actual counter   = %d\n",
           counter);

    return 0;
}
```

```bash
gcc omp_race.c -o omp_race -fopenmp
./omp_race
```

Example output:

```text
Expected counter = 400000
Actual counter   = 100000
```

The exact incorrect result depends on execution timing and compiler optimization, and will vary between runs.

### What did we learn?

OpenMP creates and manages the threads, but it does **not automatically make every shared-data operation safe**. Multiple threads are still modifying `counter++`, so a race condition can occur.

---

## Step 9: OpenMP `critical`

We fix the race condition using `#pragma omp critical`, which allows only one thread at a time to execute the protected section.

```bash
nano omp_critical.c
```

```c
#include <stdio.h>
#include <omp.h>

#define NUM_THREADS 4
#define INCREMENTS 100000

int counter = 0;

int main()
{
    omp_set_num_threads(NUM_THREADS);

    #pragma omp parallel
    {
        for (int i = 0; i < INCREMENTS; i++)
        {
            #pragma omp critical
            {
                counter++;
            }
        }
    }

    printf("Expected counter = %d\n",
           NUM_THREADS * INCREMENTS);

    printf("Actual counter   = %d\n",
           counter);

    return 0;
}
```

```bash
gcc omp_critical.c -o omp_critical -fopenmp
./omp_critical
```

Expected output:

```text
Expected counter = 400000
Actual counter   = 400000
```

### What is a critical section?

Only one OpenMP thread can execute the block at a time:

```text
Thread 1 -> enters
Thread 2 -> waits
Thread 3 -> waits
Thread 4 -> waits

Thread 1 -> exits

Thread 2 -> enters
```

This protects the shared operation.

---

## Step 10: OpenMP Barrier

Now we learn **coordination** using `#pragma omp barrier`. A barrier means every thread must reach the barrier before any thread continues beyond it.

```bash
nano omp_barrier.c
```

```c
#include <stdio.h>
#include <omp.h>

int main()
{
    omp_set_num_threads(4);

    #pragma omp parallel
    {
        int thread_id = omp_get_thread_num();

        printf("Thread %d completed Stage 1\n", thread_id);

        #pragma omp barrier

        printf("Thread %d started Stage 2\n", thread_id);
    }

    return 0;
}
```

```bash
gcc omp_barrier.c -o omp_barrier -fopenmp
./omp_barrier
```

Expected pattern:

```text
Thread 0 completed Stage 1
Thread 3 completed Stage 1
Thread 1 completed Stage 1
Thread 2 completed Stage 1
Thread 3 started Stage 2
Thread 2 started Stage 2
Thread 0 started Stage 2
Thread 1 started Stage 2
```

The order may differ, but all "completed Stage 1" messages appear before any "started Stage 2" message.

### What did we learn?

The barrier is a **meeting point**:

```text
Thread 1 -- Stage 1 --|
Thread 2 -- Stage 1 --|
Thread 3 -- Stage 1 --|-- Barrier
Thread 4 -- Stage 1 --|
                       |
                       v
                    Stage 2
```

This is thread **coordination**.

---

# Part C: Performance Analysis

Now that thread creation, management, synchronization, and coordination have been demonstrated, the next question is:

> **Does using multiple threads actually make the program faster?**

A large computational workload is used to compare sequential, Pthreads, and OpenMP execution.

## Step 11: Sequential Baseline

```bash
nano sequential.c
```

```c
#include <stdio.h>
#include <time.h>

#define N 1000000000L

double get_time()
{
    struct timespec ts;

    clock_gettime(CLOCK_MONOTONIC, &ts);

    return ts.tv_sec + ts.tv_nsec / 1e9;
}

int main()
{
    double sum = 0.0;

    double start = get_time();

    for (long i = 0; i < N; i++)
    {
        sum += (double)i * 0.000001;
    }

    double end = get_time();

    printf("Result = %.2f\n", sum);
    printf("Execution time = %.6f seconds\n",
           end - start);

    return 0;
}
```

```bash
gcc sequential.c -o sequential
./sequential
```

Expected:

```text
Result = 499999999500.00
Execution time = ... seconds
```

Measured runs (seconds):

| Run | Time (s) |
| --- | --- |
| 1 | 1.353895 |
| 2 | 1.355794 |
| 3 | 1.349621 |
| 4 | 1.353422 |
| 5 | 1.353365 |

**Average: 1.353219 seconds.** This value is used as the **sequential baseline**.

> **What is a baseline?** The reference value against which the parallel versions are compared.

---

## Step 12: Pthreads Performance

We now perform the same large calculation using Pthreads.

```bash
nano pthread_perf.c
```

```c
#include <stdio.h>
#include <pthread.h>
#include <time.h>

#define N 1000000000L

double partial_sum[32];

typedef struct
{
    int thread_id;
    long start;
    long end;
} ThreadData;

double get_time()
{
    struct timespec ts;

    clock_gettime(CLOCK_MONOTONIC, &ts);

    return ts.tv_sec + ts.tv_nsec / 1e9;
}

void *calculate(void *arg)
{
    ThreadData *data = (ThreadData *)arg;

    double sum = 0.0;

    for (long i = data->start; i < data->end; i++)
    {
        sum += (double)i * 0.000001;
    }

    partial_sum[data->thread_id] = sum;

    return NULL;
}

int main()
{
    int num_threads;

    printf("Enter number of threads: ");
    scanf("%d", &num_threads);

    if (num_threads < 1 || num_threads > 32)
    {
        printf("Please enter a value between 1 and 32.\n");
        return 1;
    }

    pthread_t threads[num_threads];
    ThreadData data[num_threads];

    long chunk = N / num_threads;

    double start_time = get_time();

    for (int i = 0; i < num_threads; i++)
    {
        data[i].thread_id = i;
        data[i].start = i * chunk;

        if (i == num_threads - 1)
            data[i].end = N;
        else
            data[i].end = (i + 1) * chunk;

        pthread_create(
            &threads[i],
            NULL,
            calculate,
            &data[i]
        );
    }

    for (int i = 0; i < num_threads; i++)
    {
        pthread_join(threads[i], NULL);
    }

    double total_sum = 0.0;

    for (int i = 0; i < num_threads; i++)
    {
        total_sum += partial_sum[i];
    }

    double end_time = get_time();

    printf("Result = %.2f\n", total_sum);
    printf("Execution time = %.6f seconds\n",
           end_time - start_time);

    return 0;
}
```

Compile:

```bash
gcc pthread_perf.c -o pthread_perf -pthread
```

Run the program once for each thread count (1, 2, 4, 6, 16). Each time, enter the number of threads when prompted:

```bash
./pthread_perf
```

Example (1 thread):

```text
Enter number of threads: 1
Result = 499999999500.00
Execution time = 1.348142 seconds
```

Measured execution times: 2 threads = 0.680737 s, 4 threads = 0.358872 s, 6 threads = 0.241345 s, 16 threads = 0.144812 s.

## 13. Pthreads Performance Results

| **Threads** | **Pthreads Time** |
| --- | --- |
| 1 | 1.348142 s |
| 2 | 0.680737 s |
| 4 | 0.358872 s |
| 6 | 0.241345 s |
| 16 | 0.144812 s |

### What are we learning?

The computational problem remains the same; only the number of threads changes (1 → 2 → 4 → 6 → 16). The execution time generally decreases, which demonstrates the benefit of parallelism for this workload.

---

## Step 14: OpenMP Performance

Now we perform the same performance experiment using OpenMP.

```bash
nano omp_perf.c
```

```c
#include <stdio.h>
#include <omp.h>
#include <time.h>

#define N 1000000000L

double get_time()
{
    struct timespec ts;

    clock_gettime(CLOCK_MONOTONIC, &ts);

    return ts.tv_sec + ts.tv_nsec / 1e9;
}

int main()
{
    double sum = 0.0;
    int num_threads;

    printf("Enter number of threads: ");
    scanf("%d", &num_threads);

    if (num_threads < 1 || num_threads > 32)
    {
        printf("Please enter a value between 1 and 32.\n");
        return 1;
    }

    omp_set_num_threads(num_threads);

    double start_time = get_time();

    #pragma omp parallel for reduction(+:sum)
    for (long i = 0; i < N; i++)
    {
        sum += (double)i * 0.000001;
    }

    double end_time = get_time();

    printf("Result = %.2f\n", sum);
    printf("Execution time = %.6f seconds\n",
           end_time - start_time);

    return 0;
}
```

Compile:

```bash
gcc omp_perf.c -o omp_perf -fopenmp
```

Run for 1, 2, 4, 6, and 16 threads:

```bash
./omp_perf
```

Example (1 thread):

```text
Enter number of threads: 1
Result = 499999999500.00
Execution time = 1.409294 seconds
```

Measured execution times: 2 threads = 0.715560 s, 4 threads = 0.360803 s, 6 threads = 0.241608 s, 16 threads = 0.140692 s.

---

## 15. Final Performance Results

**Sequential baseline: 1.353219 seconds**

### Pthreads and OpenMP Comparison

| **Threads** | **Pthreads Time (s)** | **OpenMP Time (s)** |
| --- | --- | --- |
| 1 | 1.348142 | 1.409294 |
| 2 | 0.680737 | 0.715560 |
| 4 | 0.358872 | 0.360803 |
| 6 | 0.241345 | 0.241608 |
| 16 | 0.144812 | 0.140692 |

![Figure 1: Execution Time vs Number of Threads](images/fig1_execution_time.png)

*Figure 1: Execution Time vs Number of Threads*

### Observation

As the number of threads increases, the execution time generally decreases for both Pthreads and OpenMP. The execution time becomes much smaller with 16 threads compared with 1 thread.

---

## 16. Speedup

**How much faster did the parallel program become compared with the sequential program?**

$$\text{Speedup} = \frac{\text{Sequential Time}}{\text{Parallel Time}}$$

For example, OpenMP with 16 threads:

```text
Sequential = 1.353219 s
OpenMP     = 0.140692 s

Speedup = 1.353219 / 0.140692 ≈ 9.62
```

This means the measured 16-thread OpenMP execution completed the workload in roughly 1/9.62 of the sequential time.

### Speedup Results

| **Threads** | **Pthreads Speedup** | **OpenMP Speedup** |
| --- | --- | --- |
| 1 | 1.004x | 0.960x |
| 2 | 1.988x | 1.891x |
| 4 | 3.771x | 3.751x |
| 6 | 5.608x | 5.601x |
| 16 | 9.345x | 9.618x |

![Figure 2: Speedup vs Number of Threads](images/fig2_speedup.png)

*Figure 2: Speedup vs Number of Threads*

### Observation

Speedup increases as the number of threads increases. With 16 threads:

- Pthreads achieved approximately **9.35x speedup**
- OpenMP achieved approximately **9.62x speedup**

These values represent the measured results for this execution environment and workload.

---

## 17. Efficiency

Efficiency tells us how effectively the available threads contribute to the speedup.

$$\text{Efficiency} = \frac{\text{Speedup}}{\text{Number of Threads}} \times 100$$

For 16-thread OpenMP:

```text
Speedup = 9.62
Threads = 16

Efficiency = 9.62 / 16 x 100 ≈ 60.1%
```

### Efficiency Results

| **Threads** | **Pthreads Efficiency** | **OpenMP Efficiency** |
| --- | --- | --- |
| 1 | 100.38% | 96.02% |
| 2 | 99.39% | 94.56% |
| 4 | 94.27% | 93.76% |
| 6 | 93.45% | 93.35% |
| 16 | 58.40% | 60.11% |

![Figure 3: Efficiency vs Number of Threads](images/fig3_efficiency.png)

*Figure 3: Efficiency vs Number of Threads*

### Observation

Efficiency remains relatively high at lower thread counts but decreases at 16 threads. This shows that adding more threads does not automatically provide proportional speedup.

---

## 18. Why Does 16 Threads Not Give 16x Speedup?

We might expect `1.35 / 16 ≈ 0.084 seconds`, but the measured OpenMP time was `0.140692 seconds`.

The reason is that real parallel programs have overhead. Examples include:

- Thread management
- Scheduling
- Synchronization
- Memory access
- Operating-system activity
- Non-parallel work

> **More threads can reduce execution time, but the speedup is not perfectly linear.**

---

## 19. Quick Difference: Pthreads vs OpenMP

| **Concept** | **Pthreads** | **OpenMP** |
| --- | --- | --- |
| Create threads | `pthread_create()` | `#pragma omp parallel` |
| Wait for threads | `pthread_join()` | OpenMP runtime handles team completion at region end |
| Work distribution | Programmer explicitly divides work | `parallel for` can distribute loop iterations |
| Protect shared data | Mutex | `critical` |
| Coordination | Join / synchronization mechanisms | `barrier` |
| Combine partial results | Programmer-managed | `reduction` |

---

## 20. Important Terms

| Term | Meaning |
| --- | --- |
| **Thread** | A path of execution inside a program. |
| **Main thread** | The thread that starts executing the `main()` function when the program begins. |
| **Additional thread** | A new thread created by the program using a mechanism such as `pthread_create()`. |
| **Multithreading** | Using multiple threads within one program. |
| **Parallel programming** | Dividing work so that multiple execution units can perform parts of the work concurrently. |
| **Work distribution** | Dividing one large task into smaller tasks and assigning them to different threads. |
| **Race condition** | Multiple threads access or modify shared data without proper coordination, so the result can become incorrect. |
| **Mutex** | A locking mechanism used in Pthreads to protect a critical section. |
| **Critical section** | A section of code where simultaneous execution by multiple threads must be restricted. |
| **Barrier** | A synchronization point where threads wait until all required threads reach the same point. |
| **Speedup** | How much faster the parallel program is compared with the sequential baseline. |
| **Efficiency** | How effectively the available threads produce the measured speedup. |

---

## 21. Implemented Programs

### Part A: Pthreads

- `thread1.c`: Create one thread
- `thread2.c`: Create multiple threads
- `thread_sum.c`: Divide work among threads
- `race.c`: Demonstrate race condition
- `mutex.c`: Fix race condition using mutex
- `pthread_perf.c`: Measure performance

### Part B: OpenMP

- `omp1.c`: Parallel region and thread identification
- `omp_sum.c`: Work sharing and reduction
- `omp_race.c`: Demonstrate race condition
- `omp_critical.c`: Synchronization using critical
- `omp_barrier.c`: Thread coordination
- `omp_perf.c`: Measure performance

### Part C: Performance Analysis

- `sequential.c`: Sequential baseline
- Pthreads execution
- OpenMP execution
- Execution-time comparison
- Speedup calculation
- Efficiency calculation
- Graphical analysis
- Performance interpretation

---

## 22. Complete Learning Flow

```text
START
  |
  v
Understand Threads
  |
  v
Create One Thread
  |
  v
Create Multiple Threads
  |
  v
Divide Work
  |
  v
Shared Data
  |
  v
Race Condition
  |
  v
Synchronization
  |
  v
OpenMP Parallel Region
  |
  v
OpenMP Work Sharing
  |
  v
OpenMP Race Condition
  |
  v
OpenMP Critical Section
  |
  v
OpenMP Barrier
  |
  v
Sequential Performance
  |
  v
Pthreads Performance
  |
  v
OpenMP Performance
  |
  v
Execution-Time Graph
  |
  v
Speedup
  |
  v
Speedup Graph
  |
  v
Efficiency
  |
  v
Efficiency Graph
  |
  v
Final Analysis
```

---

## 23. Conclusion

The experiment demonstrates how multithreaded programs can be developed using **Pthreads and OpenMP**.

Pthreads provides explicit control over thread creation, joining, and mutex-based synchronization. OpenMP provides a higher-level programming model using parallel regions, work-sharing directives, critical sections, barriers, and reductions.

The experiments also demonstrate that multiple threads can introduce race conditions when shared data is not protected. Synchronization mechanisms such as mutexes and critical sections are therefore necessary.

The performance experiment demonstrates that increasing the number of threads can reduce execution time for a suitable workload. Both Pthreads and OpenMP showed substantial reductions in execution time as the thread count increased.

The graphs provide three complementary views of the results:

- **Execution time** shows how long the computation takes.
- **Speedup** shows how much faster the parallel execution is relative to the sequential baseline.
- **Efficiency** shows how effectively the available threads contribute to the measured speedup.

The measured results also show that speedup is not perfectly proportional to the number of threads, because parallel execution introduces overhead such as scheduling, synchronization, memory access, thread management, and non-parallel work.

The complete learning flow is:

**Create → Manage → Divide Work → Share Data → Handle Race Conditions → Synchronize → Coordinate → Measure Performance → Analyze Results**

---

*Multithreaded Programming Using Pthreads and OpenMP*

