import numpy as np
import os

def load_voltage_current(filepath, source_number=1):
    """
    Parses PFFDTD .vc (Voltage/Current) output files.

    Args:
        filepath (str): Path to the .vc file.
        source_number (int): Source identifier (default: 1).

    Returns:
        tuple: (time_array, voltage_array, current_array)
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    try:
        # Load all data, assuming space delimiter
        # The first row is 'index' in Matlab script, rest are 'values'
        raw_data = np.loadtxt(filepath)
        
        if raw_data.ndim == 1:
            # Handle case where file might only have one line or header issue?
            # Or if loadtxt separates everything into 1D array
            # But usually it returns 2D array if multiple lines
             raise ValueError("File content format unexpected (1D array).")

        # Skip the first row (index/header)
        values = raw_data[1:, :]
        
        # Matlab Logic:
        # T = values(:,1);      -> Python col 0
        # V = values(:,2*sn);   -> Python col 2*sn - 1
        # C = values(:,2*sn+1); -> Python col 2*sn
        
        # Wait, check indices again.
        # Matlab (1-based): col 1 -> Python 0
        # Matlab: col 2*sn.  If sn=1 -> col 2. Python 1.
        # Matlab: col 2*sn+1. If sn=1 -> col 3. Python 2.
        
        time_col = 0
        voltage_col = 2 * source_number - 1
        current_col = 2 * source_number
        
        if values.shape[1] <= current_col:
             raise ValueError(f"File does not contain enough columns for source number {source_number}")

        time = values[:, time_col]

    except Exception as e:
        raise RuntimeError(f"Failed to parse {filepath}: {e}")

def load_fields(filepath):
    """
    Parses PFFDTD .fd (Field Data) output files.
    
    Format according to src/io/output.cpp:
    - Line 1: '0' then Field IDs (11, 12, 13, etc.)
    - Line 2: '0' then i-coordinates
    - Line 3: '0' then j-coordinates
    - Line 4: '0' then k-coordinates
    - Line 5+: Time + Data values flattened
    
    Returns:
        dict: containing:
            'time': np.array (T,)
            'coords': dict with 'i', 'j', 'k' arrays matching columns
            'field_ids': list of field identifiers
            'data': np.array (T, N_points, N_fields_per_point??)
            # Actually, the file format flattens X,Y,Z loops.
            # Row = [Time, Val(x0,y0,z0,F1), Val(x0,y0,z0,F2)... Val(x1..)]
            # It seems it iterates i,j,k and prints selected fields for each point.
            
            Rearranging this into a ND-array is tricky without knowing the exact grid dimensions beforehand 
            unless we deduce it from the coord lines.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(filepath, 'r') as f:
        # Read Headers
        # Line 1: 0 <FieldID1> <FieldID2> ...
        line1 = f.readline().strip().split()
        if not line1: raise ValueError("Empty file")
        field_ids = [int(x) for x in line1[1:]]
        
        # Line 2: 0 <i1> <i2> ...
        line2 = f.readline().strip().split()
        i_coords = [int(x) for x in line2[1:]]
        
        # Line 3: 0 <j1> <j2> ...
        line3 = f.readline().strip().split()
        j_coords = [int(x) for x in line3[1:]]
        
        # Line 4: 0 <k1> <k2> ...
        line4 = f.readline().strip().split()
        k_coords = [int(x) for x in line4[1:]]
        
        if not (len(field_ids) == len(i_coords) == len(j_coords) == len(k_coords)):
            # NOTE: C++ code loop:
            # for i.. for j.. for k..
            #    print Field1, Field2, Field3...
            # BUT the header printing loop does: 
            # for i.. for j.. for k..
            #    print ID1, ID2, ID3...
            # OR does it print ID for every point?
            # 
            # output.cpp: 
            # fprintf(file_fd,"0");
            # for (i...) for (j...) for (k...)
            #    if(fout[0]) fprintf("\t11\t12\t13")
            # 
            # So for ONE point (i,j,k), it expects MULTIPLE columns if multiple fields are enabled.
            # And the coordinate lines repeat i,j,k for EACH field column?
            # 
            # output.cpp line 66: if(fout[0]) fprintf("\t%d\t%d\t%d", i, i, i);
            # YES. The coordinate lines repeat the coordinate for each field component outputs.
            pass

    # Read the rest efficiently
    data_raw = np.loadtxt(filepath, skiprows=4)
    if data_raw.ndim == 1:
        data_raw = data_raw[np.newaxis, :]
        
    time = data_raw[:, 0]
    values = data_raw[:, 1:]
    
    # We need to restructure `values`.
    # `values` shape is (TimeSteps, N_columns).
    # N_columns matches length of i_coords.
    
    # Let's organize data into a DataFrame-like structure or a structured array would be best,
    # but for visualization, maybe a 3D grid is better.
    
    # Identify unique coordinates to determine Grid Size
    unique_i = sorted(list(set(i_coords)))
    unique_j = sorted(list(set(j_coords)))
    unique_k = sorted(list(set(k_coords)))
    
    nx, ny, nz = len(unique_i), len(unique_j), len(unique_k)
    
    # Map coordinates to indices
    i_map = {val: idx for idx, val in enumerate(unique_i)}
    j_map = {val: idx for idx, val in enumerate(unique_j)}
    k_map = {val: idx for idx, val in enumerate(unique_k)}
    
    # Identify unique Field IDs
    # e.g. 11 (Ex), 12 (Ey), 13 (Ez)...
    unique_fields = sorted(list(set(field_ids)))
    
    # Goal: Create a dictionary of 4D arrays: FieldID -> (Time, Nx, Ny, Nz)
    
    fields_data = {}
    for fid in unique_fields:
        fields_data[fid] = np.zeros((len(time), nx, ny, nz))
        
    # Populate
    # This loop is slow in pure Python. Vectorization is preferred.
    # We can create a mapping mask.
    
    # For each column 'col_idx' in 'values':
    # It corresponds to (i_coords[col], j_coords[col], k_coords[col]) and field_ids[col]
    
    for col_idx in range(len(field_ids)):
        fid = field_ids[col_idx]
        i = i_coords[col_idx]
        j = j_coords[col_idx]
        k = k_coords[col_idx]
        
        ix, iy, iz = i_map[i], j_map[j], k_map[k]
        
        fields_data[fid][:, ix, iy, iz] = values[:, col_idx]
        
    return {
        'time': time,
        'fields': fields_data,
        'grid': {'x': unique_i, 'y': unique_j, 'z': unique_k},
        'metadata': {'nx': nx, 'ny': ny, 'nz': nz}
    }
