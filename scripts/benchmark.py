import subprocess
import time
import os
import matplotlib.pyplot as plt

def run_benchmark(executable, input_file, threads):
    """Runs the PFFDTD simulation with a specific number of threads."""
    env = os.environ.copy()
    env["OMP_NUM_THREADS"] = str(threads)
    
    start_time = time.time()
    # Assuming the executable takes the input file as an argument
    # and we want to suppress output for speed/cleanliness
    try:
        subprocess.run([executable, input_file], env=env, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running with {threads} threads: {e}")
        return None
    end_time = time.time()
    
    return end_time - start_time

def main():
    executable = "pffdtd_parallelMP.exe"
    # Create a small test input file if it doesn't exist, or use a standard one
    # For now, we assume 'dipole.str' exists as seen in the file list
    input_file_base = "dipoleTest" 
    
    thread_counts = [1, 2, 4, 8]
    execution_times = []

    print(f"Benchmarking {executable} with input {input_file_base}...")

    for t in thread_counts:
        print(f"Running with {t} threads...")
        duration = run_benchmark(executable, input_file_base, t)
        if duration is not None:
            print(f"  Time: {duration:.4f} seconds")
            execution_times.append(duration)
        else:
            execution_times.append(0)

    # Calculate Speedup
    if execution_times[0] > 0:
        speedups = [execution_times[0] / t if t > 0 else 0 for t in execution_times]
    else:
        speedups = [0] * len(thread_counts)

    print("\nResults:")
    print("Threads | Time (s) | Speedup")
    print("------- | -------- | -------")
    for i, t in enumerate(thread_counts):
        print(f"{t:7d} | {execution_times[i]:8.4f} | {speedups[i]:.2f}x")

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(thread_counts, speedups, 'o-', label='Measured Speedup')
    plt.plot(thread_counts, thread_counts, 'k--', label='Ideal Linear Speedup')
    plt.title('PFFDTD OpenMP Scaling')
    plt.xlabel('Number of Threads')
    plt.ylabel('Speedup')
    plt.legend()
    plt.grid(True)
    plt.savefig('scaling_results.png')
    print("Scaling plot saved to scaling_results.png")

if __name__ == "__main__":
    main()
