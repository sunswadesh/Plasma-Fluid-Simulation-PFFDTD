import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
import sys

# Add current directory to path to find loader
# Add current directory to path to find loader
# Add current directory to path to find loader
sys.path.append(os.path.dirname(__file__))
from pffdtd_loader import load_fields, load_voltage_current

def compare_traces(file1, file2, save_path=None):
    print(f"Loading {file1}...")
    t1, v1, i1 = load_voltage_current(file1)
    print(f"Loading {file2}...")
    t2, v2, i2 = load_voltage_current(file2)
    
    # Check lengths
    min_len = min(len(t1), len(t2))
    if len(t1) != len(t2):
        print(f"Warning: Length mismatch {len(t1)} vs {len(t2)}. Truncating to {min_len}.")
        
    t1, v1, i1 = t1[:min_len], v1[:min_len], i1[:min_len]
    t2, v2, i2 = t2[:min_len], v2[:min_len], i2[:min_len]
    
    # Calc Diffs
    diff_v = v1 - v2
    diff_i = i1 - i2
    max_diff_v = np.max(np.abs(diff_v))
    max_diff_i = np.max(np.abs(diff_i))
    
    print(f"Max Voltage Diff: {max_diff_v}")
    print(f"Max Current Diff: {max_diff_i}")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Voltage
    axes[0,0].plot(t1, v1, 'b-', label='Serial')
    axes[0,0].plot(t2, v2, 'r--', label='Parallel')
    axes[0,0].set_title('Voltage Trace')
    axes[0,0].legend()
    
    axes[0,1].plot(t1, diff_v, 'k-')
    axes[0,1].set_title(f'Voltage Difference (Max: {max_diff_v:.2e})')
    
    # Current
    axes[1,0].plot(t1, i1, 'b-', label='Serial')
    axes[1,0].plot(t2, i2, 'r--', label='Parallel')
    axes[1,0].set_title('Current Trace')
    axes[1,0].legend()
    
    axes[1,1].plot(t1, diff_i, 'k-')
    axes[1,1].set_title(f'Current Difference (Max: {max_diff_i:.2e})')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        print(f"Trace comparison saved to {save_path}")
    else:
        plt.show()

def compare_fields(file1, file2, field_idx, slice_axis, slice_idx, save_path=None):
    print(f"Loading {file1}...")
    res1 = load_fields(file1)
    print(f"Loading {file2}...")
    res2 = load_fields(file2)
    
    # Check if field exists
    if field_idx not in res1['fields'] or field_idx not in res2['fields']:
        print(f"Error: Field {field_idx} not found in files. Available: {list(res1['fields'].keys())}")
        return

    # Get data for the specific field: Shape (Time, Nx, Ny, Nz)
    data1 = res1['fields'][field_idx]
    data2 = res2['fields'][field_idx]
    
    # Compare Last Time Step
    time_idx = -1 
    d1 = data1[time_idx]
    d2 = data2[time_idx]

    # Check dimensions
    if d1.shape != d2.shape:
        print(f"Error: Shape mismatch {d1.shape} vs {d2.shape}")
        return

    meta1 = res1['metadata']

    # Extract slice from 3D volume (Nx, Ny, Nz)
    if slice_axis == 'x':
        if slice_idx >= meta1['nx']: slice_idx = meta1['nx'] - 1
        slice1 = d1[slice_idx, :, :]
        slice2 = d2[slice_idx, :, :]
        extent = [0, meta1['ny'], 0, meta1['nz']]
        xlabel, ylabel = 'Y', 'Z'
    elif slice_axis == 'y':
        if slice_idx >= meta1['ny']: slice_idx = meta1['ny'] - 1
        slice1 = d1[:, slice_idx, :]
        slice2 = d2[:, slice_idx, :]
        extent = [0, meta1['nx'], 0, meta1['nz']]
        xlabel, ylabel = 'X', 'Z'
    else: # z
        if slice_idx >= meta1['nz']: slice_idx = meta1['nz'] - 1
        slice1 = d1[:, :, slice_idx]
        slice2 = d2[:, :, slice_idx]
        extent = [0, meta1['nx'], 0, meta1['ny']]
        xlabel, ylabel = 'X', 'Y'

    # Compute Difference
    diff = slice1 - slice2
    max_diff = np.max(np.abs(diff))
    print(f"Max Absolute Difference: {max_diff}")

    # Plot
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # Plot 1: Baseline
    im1 = axes[0].imshow(slice1.T, origin='lower', aspect='auto', cmap='seismic')
    axes[0].set_title(f'Baseline (Serial)\n{os.path.basename(file1)}')
    axes[0].set_xlabel(xlabel)
    axes[0].set_ylabel(ylabel)
    plt.colorbar(im1, ax=axes[0])

    # Plot 2: New
    im2 = axes[1].imshow(slice2.T, origin='lower', aspect='auto', cmap='seismic')
    axes[1].set_title(f'New (Parallel)\n{os.path.basename(file2)}')
    axes[1].set_xlabel(xlabel)
    axes[1].set_ylabel(ylabel)
    plt.colorbar(im2, ax=axes[1])

    # Plot 3: Difference
    # Use a sensitive colormap for error
    im3 = axes[2].imshow(diff.T, origin='lower', aspect='auto', cmap='viridis')
    axes[2].set_title(f'Difference (Error)\nMax Diff: {max_diff:.2e}')
    axes[2].set_xlabel(xlabel)
    axes[2].set_ylabel(ylabel)
    plt.colorbar(im3, ax=axes[2])

    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        print(f"Comparison saved to {save_path}")
    else:
        plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare two PFFDTD field files.")
    parser.add_argument("file1", help="Path to first file (Baseline)")
    parser.add_argument("file2", help="Path to second file (New)")
    parser.add_argument("--field", type=int, default=0, help="Field index to plot (default: 0)")
    parser.add_argument("--slice_axis", choices=['x', 'y', 'z'], default='z', help="Axis to slice along")
    parser.add_argument("--slice_idx", type=int, default=0, help="Index of the slice")
    parser.add_argument("--save", help="Path to save image")
    
    args = parser.parse_args()
    
    ext1 = os.path.splitext(args.file1)[1]
    ext2 = os.path.splitext(args.file2)[1]
    
    if ext1 == '.vc' and ext2 == '.vc':
        compare_traces(args.file1, args.file2, args.save)
    else:
        compare_fields(args.file1, args.file2, args.field, args.slice_axis, args.slice_idx, args.save)
