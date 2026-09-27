# Multithreaded Programming Using Pthreads and OpenMP

## EXPERIMENT

**Develop Multithreaded Programs Using Parallel Programming Libraries to Understand Thread Creation, Management, and Coordination**

---

# 1. AIM

To develop multithreaded programs using Pthreads and OpenMP and understand:

- Thread creation
- Thread management
- Work distribution
- Race conditions
- Synchronization
- Thread coordination
- Performance improvement using multiple threads

---

# 2. BASIC IDEA OF THE EXPERIMENT

A thread is an execution path inside a program.

Think of a thread as a worker.

## Sequential Program

One worker performs all the work.

```text
Sequential Program

One thread
    |
    |---- Task 1
    |---- Task 2
    |---- Task 3
    |---- Task 4
    |---- ...
