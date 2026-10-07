import os
import matplotlib.pyplot as plt
import pandas as pd

# Load benchmark metrics
csv_path = os.path.join("..", "data", "metrics_summary.csv")
if not os.path.exists(csv_path):
    csv_path = "data/metrics_summary.csv"

df = pd.read_csv(csv_path)

threads = df["threads"]
pthreads_time = df["pthreads_time"]
openmp_time = df["openmp_time"]
pthreads_speedup = df["pthreads_speedup"]
openmp_speedup = df["openmp_speedup"]
pthreads_eff = df["pthreads_efficiency_pct"]
openmp_eff = df["openmp_efficiency_pct"]

output_dir = os.path.dirname(__file__) if os.path.dirname(__file__) else "."

# 1. Execution Time Plot
plt.figure(figsize=(9, 5.5))
plt.plot(threads, pthreads_time, marker="o", linewidth=2, label="Pthreads")
plt.plot(threads, openmp_time, marker="o", linewidth=2, label="OpenMP")
plt.title("Execution Time vs Number of Threads", fontsize=14, pad=12)
plt.xlabel("Number of Threads", fontsize=12)
plt.ylabel("Execution Time (seconds)", fontsize=12)
plt.xticks([1, 2, 4, 6, 16])
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "execution_time_vs_threads.png"), dpi=300)
plt.close()

# 2. Speedup Plot
plt.figure(figsize=(9, 5.5))
plt.plot(threads, pthreads_speedup, marker="o", linewidth=2, label="Pthreads")
plt.plot(threads, openmp_speedup, marker="o", linewidth=2, label="OpenMP")
plt.plot(threads, threads, linestyle=":", color="gray", label="Ideal Linear Speedup")
plt.title("Speedup vs Number of Threads", fontsize=14, pad=12)
plt.xlabel("Number of Threads", fontsize=12)
plt.ylabel("Speedup (x)", fontsize=12)
plt.xticks([1, 2, 4, 6, 16])
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "speedup_vs_threads.png"), dpi=300)
plt.close()

# 3. Efficiency Plot
plt.figure(figsize=(9, 5.5))
plt.plot(threads, pthreads_eff, marker="o", linewidth=2, label="Pthreads")
plt.plot(threads, openmp_eff, marker="o", linewidth=2, label="OpenMP")
plt.axhline(y=100, linestyle=":", color="gray", label="100% Ideal Efficiency")
plt.title("Efficiency vs Number of Threads", fontsize=14, pad=12)
plt.xlabel("Number of Threads", fontsize=12)
plt.ylabel("Efficiency (%)", fontsize=12)
plt.xticks([1, 2, 4, 6, 16])
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "efficiency_vs_threads.png"), dpi=300)
plt.close()

print("Graphs successfully generated in:", output_dir)