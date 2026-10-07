# Laboratory Report: Multithreaded Programming Using Pthreads and OpenMP

## 1. Objectives & Scope
The objective of this laboratory experiment is to study concurrent execution models across explicit and implicit multithreading paradigms:
1. Low-level POSIX Threads (`Pthreads`): manual creation (`pthread_create`), thread joining (`pthread_join`), and mutex locks (`pthread_mutex_t`).
2. High-level OpenMP: compiler-directed parallelism (`#pragma omp parallel`), work-sharing (`parallel for`), reduction operators, critical regions, and synchronization barriers.
3. Comparative benchmarking under compute-heavy loop reductions ($N = 10^9$ iterations) across 1, 2, 4, 6, and 16 threads against a sequential baseline.

---

## 2. Experimental Environment & Setup
- **Operating System:** Ubuntu on Windows Subsystem for Linux (WSL2)
- **Compiler:** GCC 15.2.0 (`gcc -fopenmp -pthread`)
- **Core Library Dependencies:** `build-essential`, `libgomp1`, POSIX Pthreads runtime
- **Available Hardware Threads:** 16 logical threads

---

## 3. Implementation Analysis & Synchronizations

### 3.1 Race Conditions and Mutual Exclusion
When concurrent threads execute unsynchronized write operations (`counter++`) across $4 \times 10^5$ operations:
- **Pthreads Race (`race.c`):** Returned incomplete values ($179,154$ and $129,732$) due to read-modify-write interleaved hazards.
- **Pthreads Mutex (`mutex.c`):** Fixed race condition via `pthread_mutex_lock()` and `pthread_mutex_unlock()`, yielding an exact expected count of $400,000$.
- **OpenMP Race (`omp_race.c`):** Produced an inconsistent output of $122,322$.
- **OpenMP Critical Section (`omp_critical.c`):** Enforced serialization on the critical increment using `#pragma omp critical`, returning $400,000$.

### 3.2 Thread Coordination via Barriers
OpenMP barriers (`#pragma omp barrier`) enforce strict barrier synchronization:
- All threads ($0$ through $3$) completed Stage 1 before any thread executed Stage 2, establishing phase-based execution safety.

---

## 4. Performance Metrics and Comparative Evaluation

The workload executes $N = 1,000,000,000$ loop operations.

$$\text{Sequential Baseline Time } (T_{\text{seq}}) = 1.838037\text{ seconds}$$

$$\text{Speedup } (S) = \frac{T_{\text{seq}}}{T_{\text{parallel}}}$$

$$\text{Efficiency } (E) = \frac{S}{\text{Thread Count}} \times 100\%$$

### Performance Benchmark Summary Table

| Threads ($p$) | Pthreads Time (s) | Pthreads Speedup | Pthreads Efficiency | OpenMP Time (s) | OpenMP Speedup | OpenMP Efficiency |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1** | 1.822517 | 1.009x | 100.85% | 1.827739 | 1.006x | 100.56% |
| **2** | 0.933641 | 1.969x | 98.43% | 0.929209 | 1.978x | 98.90% |
| **4** | 0.484443 | 3.794x | 94.85% | 0.486579 | 3.778x | 94.44% |
| **6** | 0.412023 | 4.461x | 74.35% | 0.415275 | 4.426x | 73.77% |
| **16** | 0.260299 | 7.061x | 44.13% | 0.231678 | 7.934x | 49.58% |

---

## 5. Key Findings & Discussion

1. **Near-Ideal Scaling at Low Thread Counts:**  
   Between 1 and 4 threads, speedup is almost perfectly linear ($3.79\text{x}$ on 4 threads, maintaining $>94\%$ efficiency), showing that compute-bound tasks benefit directly from multi-core parallelism.
2. **Diminishing Returns at High Concurrency:**  
   At 16 threads, efficiency drops to $44.13\%$ (Pthreads) and $49.58\%$ (OpenMP). This behavior reflects **Amdahl's Law** and hardware bottlenecks:
   - Shared memory bus bandwidth saturation when 16 threads continuously read and update memory.
   - Operating system context switching and thread management overhead.
3. **Pthreads vs OpenMP Efficiency:**  
   While Pthreads offers explicit structural control, OpenMP achieves comparable or slightly superior speedup at 16 threads ($7.93\text{x}$ vs $7.06\text{x}$) due to optimized reduction tree implementations managed directly by the `libgomp` runtime.