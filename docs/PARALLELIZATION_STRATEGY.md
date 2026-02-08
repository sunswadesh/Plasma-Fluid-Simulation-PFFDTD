# Parallelization Strategy & Industry Standards

## 1. The Landscape of High Performance Computing (HPC)

When accelerating scientific code like PF-FDTD, there are two main "arenas" of parallelization, depending on whether you are running on a **Local Machine** or **Cloud HPC**.

### A. Shared Memory (Local Machine / Single Node)
*   **Technology:** **OpenMP** (Open Multi-Processing)
*   **Concept:** You have one computer with many "workers" (CPU cores) that all have access to the same memory (RAM).
*   **Analogy:** A team of engineers working around a single large table. They can all verify the same blueprint (memory) instantly without shouting across the room.
*   **Pros:** 
    *   Easiest to implement (often just adding "hints" to code).
    *   Best for modern workstations (4-64 cores).
    *   Zero network latency.
*   **Cons:** 
    *   Limited by the RAM of a single machine.
*   **Industry Standard:** The default choice for accelerating C++ loops on workstations.

### B. Distributed Memory (Cloud HPC / Clusters)
*   **Technology:** **MPI** (Message Passing Interface)
*   **Concept:** You connect many computers (nodes) together via a network. Each computer has its own private memory.
*   **Analogy:** Engineers in different buildings. If they need to share data, they must call/email (send messages). This takes time.
*   **Pros:** 
    *   Scales infinitely (thousands of nodes).
    *   Can solve problems larger than any single computer's RAM.
*   **Cons:** 
    *   Hard to code (must manually manage data splitting and communication limits).
    *   Communication overhead can slow things down if not careful.
*   **Industry Standard:** The gold standard for supercomputing (weather forecasting, nuclear sims).

### C. Hardware Acceleration (GPU)
*   **Technology:** **CUDA** (NVIDIA) or **HIP** (AMD)
*   **Concept:** Instead of 16 smart CPU cores, you use 5,000 "dumb" GPU cores.
*   **Pros:** Extreme speedups (100x) for grid-based math like FDTD.
*   **Cons:** Code must be rewritten significantly.
*   **Industry Standard:** The modern trend for AI and heavy physics simulations.

---

## 2. Our Approach: The "Tutorial Style" Plan

Since your goal is to **learn** while building, we will follow a progressive "Hero's Journey" optimization path. We will simulate the evolution of a codebase from academic helper to industrial tool.

### Step 1: OpenMP (The Low Hanging Fruit)
**Target:** Local machine optimization.
**Goal:** Use all cores of your Windows machine.
**Learning Objectives:**
1.  **Race Conditions:** What happens when two threads try to write to `Ex[i][j][k]` at the same time?
2.  **Thread Overhead:** Why making *everything* parallel sometimes makes it slower.
3.  **False Sharing:** Invisible cache conflicts that kill performance.

**Action:** We will annotate your existing `for` loops in `pffdtd.cpp` with `#pragma omp parallel for` and measure the speedup.

### Step 2: MPI (The Big Iron) - *Optional/Advanced*
**Target:** Cloud Simulation.
**Goal:** Run the simulation across 2 simulated "nodes" on your machine to learn the syntax.
**Learning Objectives:**
1.  **Domain Decomposition:** How to chop the grid into cubes.
2.  **Ghost Cells:** Exchanging boundary layers between cubes so they seamlessly connect.
3.  **Synchronization:** Making sure Node A doesn't run ahead of Node B.

### Step 3: GPU (The Speed Demon) - *Phase 6*
**Target:** Production speed.
**Goal:** Port specific loops to CUDA/HIP.

---

## 3. FAQ: Is OpenMP the same as "Multithreading"?

**Yes and No.**

*   **Multithreading** is the general concept: running multiple threads of execution at once.
*   **OpenMP** is a specific *tool* (API) to implement multithreading easily.

### The Analogy: Manual vs. Automatic Transmission

1.  **Manual Multithreading (`std::thread`, `pthreads`)**:
    *   **Like driving Manual:** You control everything. You explicitly say "Create Thread A", "Start Thread A", "Wait for Thread A", "Lock this memory", "Unlock this memory".
    *   **Good for:** Complex applications (e.g., a Web Browser having one thread for UI, one for Network, one for Rendering).
    *   **Bad for:** Math loops. It is tedious to write lines of code just to split a `for` loop.

2.  **OpenMP**:
    *   **Like driving Automatic:** You just tell the compiler "Make this loop parallel" (`#pragma omp parallel for`). The OpenMP "engine" handles creating threads, assigning indices to them (`i=0..100` to core 1, `i=101..200` to core 2), and joining them back together.
    *   **Good for:** High Performance Computing (HPC) and heavy math loops.
    *   **Bad for:** Complex UI logic.

**Verdict:** For PF-FDTD, OpenMP is the superior choice because we want to split millions of identical math operations, not manage complex application logic.

---

## 4. Recommendation for Phase 5

We should start with **OpenMP (Step 1)**.

*   **Why?** It requires minimal code restructuring but introduces critical parallel concepts. It is immediately testing on your local Windows setup without needing a cluster setup.
*   **Tutorial Plan:**
    1.  **Benchmark:** Run the serial code and record the time.
    2.  **Naive Parallelization:** Add OpenMP to the biggest loop. It might fail or be slow. We investigate why.
    3.  **Fixing Race Conditions:** We identify variables that need protection (reductions, atomic updates).
    4.  **Optimization:** We refine scheduling (static vs dynamic).
    5.  **Final Benchmark:** Compare against the serial version.

This "Break, Fix, Optimize" cycle is the best way to learn parallel programming.
