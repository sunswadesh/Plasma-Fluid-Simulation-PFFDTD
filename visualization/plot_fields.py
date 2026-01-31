import argparse
import numpy as np
import matplotlib.pyplot as plt
import os
from pffdtd_loader import load_fields

def main():
    parser = argparse.ArgumentParser(description="Visualize PFFDTD Field Data (.fd).")
    parser.add_argument("filepath", help="Path to the .fd file")
    parser.add_argument("--field", type=int, default=11, help="Field ID to plot (e.g. 11=Ex, 12=Ey). Default 11.")
    parser.add_argument("--time_idx", type=int, default=-1, help="Time step index to plot (default: last step)")
    parser.add_argument("--slice_axis", type=str, default='z', choices=['x', 'y', 'z'], help="Axis to slice along (x, y, or z)")
    parser.add_argument("--slice_idx", type=int, default=0, help="Index along the slice axis")
    parser.add_argument("--save", action="store_true", help="Save plot to file")
    
    args = parser.parse_args()

    if not os.path.exists(args.filepath):
        print(f"Error: File {args.filepath} not found.")
        return

    # 1. Load Data
    try:
        data = load_fields(args.filepath)
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    # 2. Extract specific field
    fid = args.field
    if fid not in data['fields']:
        print(f"Error: Field ID {fid} not found in file. Available: {list(data['fields'].keys())}")
        return
        
    field_data = data['fields'][fid] # Shape: (Time, Nx, Ny, Nz)
    time = data['time']
    
    # Select time step
    if args.time_idx >= len(time):
        print(f"Warning: Time index {args.time_idx} out of bounds. Using last step.")
        t_idx = -1
    else:
        t_idx = args.time_idx
        
    field_snapshot = field_data[t_idx] # Shape: (Nx, Ny, Nz)
    current_time = time[t_idx]
    
    # 3. Slicing
    # Grid coordinates
    grid = data['grid']
    nx, ny, nz = len(grid['x']), len(grid['y']), len(grid['z'])
    
    print(f"Grid Size: {nx}x{ny}x{nz}. Plotting Field {fid} at t={current_time:.2e} s.")
    
    if args.slice_axis == 'z':
        # XY plot at fixed Z
        # Map slice_idx (which is integer index 0..nz-1)
        k_idx = args.slice_idx
        if k_idx >= nz: k_idx = nz - 1
        
        slice_data = field_snapshot[:, :, k_idx] # Shape (Nx, Ny)
        xlabel, ylabel = 'X index', 'Y index'
        x_axis, y_axis = grid['x'], grid['y']
        title_str = f"Field {fid} at Z-index {k_idx} (Val={x_axis[k_idx] if k_idx < len(x_axis) else '?'})"
        
    elif args.slice_axis == 'y':
        # XZ plot at fixed Y
        j_idx = args.slice_idx
        if j_idx >= ny: j_idx = ny - 1
        
        slice_data = field_snapshot[:, j_idx, :] # Shape (Nx, Nz)
        xlabel, ylabel = 'X index', 'Z index'
        x_axis, y_axis = grid['x'], grid['z']
        title_str = f"Field {fid} at Y-index {j_idx}"

    elif args.slice_axis == 'x':
        # YZ plot at fixed X
        i_idx = args.slice_idx
        if i_idx >= nx: i_idx = nx - 1
        
        slice_data = field_snapshot[i_idx, :, :] # Shape (Ny, Nz)
        xlabel, ylabel = 'Y index', 'Z index'
        x_axis, y_axis = grid['y'], grid['z']
        title_str = f"Field {fid} at X-index {i_idx}"

    # 4. Plotting
    plt.figure(figsize=(10, 8))
    # Using imshow. Note: imshow expects (Rows, Cols) -> (Y, X).
    # so we usually transpose if we want X on horizontal.
    # extent=[xmin, xmax, ymin, ymax]
    
    # If axes are just indices:
    extent = [0, slice_data.shape[0], 0, slice_data.shape[1]]
    
    # Need to transpose for correct orientation usually: (X, Y) -> Imshow shows Y as rows
    plt.imshow(slice_data.T, origin='lower', aspect='auto', cmap='viridis')
    plt.colorbar(label='Field Amplitude')
    plt.title(f"{title_str} | t={current_time:.2e}s")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    if args.save:
        base = os.path.splitext(os.path.basename(args.filepath))[0]
        fname = f"{base}_field{fid}_{args.slice_axis}{args.slice_idx}.png"
        plt.savefig(fname)
        print(f"Saved {fname}")
    else:
        plt.show()

if __name__ == "__main__":
    main()
