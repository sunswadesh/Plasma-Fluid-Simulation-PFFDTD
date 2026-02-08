import numpy as np

def generate_test_fd(filename="test_field.fd"):
    # Grid: 10x10x5
    ni, nj, nk = 10, 10, 5
    
    # 2 Fields: 11 (Ex), 12 (Ey)
    field_ids = [11, 12]
    
    # We need to construct the header columns.
    # For every point (i, j, k), we output 2 columns.
    # Total columns = ni * nj * nk * 2
    
    cols_field_id = []
    cols_i = []
    cols_j = []
    cols_k = []
    
    # Order matched output.cpp: i loop, j loop, k loop
    for i in range(ni):
        for j in range(nj):
            for k in range(nk):
                # For each point, append columns for each field
                for fid in field_ids:
                    cols_field_id.append(fid)
                    cols_i.append(i)
                    cols_j.append(j)
                    cols_k.append(k)
                    
    # Write Header
    with open(filename, 'w') as f:
        f.write("0\t" + "\t".join(map(str, cols_field_id)) + "\n")
        f.write("0\t" + "\t".join(map(str, cols_i)) + "\n")
        f.write("0\t" + "\t".join(map(str, cols_j)) + "\n")
        f.write("0\t" + "\t".join(map(str, cols_k)) + "\n")
        
        # Write Data
        # 5 Time steps
        for t_idx in range(5):
            time = t_idx * 1e-9
            row_data = [time]
            
            # Generate field data
            # Gaussian pulse centered at (5, 5, 2)
            for idx in range(len(cols_field_id)):
                i = cols_i[idx]
                j = cols_j[idx]
                k = cols_k[idx]
                fid = cols_field_id[idx]
                
                dist_sq = (i-5)**2 + (j-5)**2 + (k-2)**2
                val = np.exp(-dist_sq / 4.0)
                
                if fid == 12: val *= -0.5 # Ey different
                
                row_data.append(val)
                
            f.write("\t".join(map(lambda x: f"{x:.4e}", row_data)) + "\n")
            
    print(f"Generated {filename}")

if __name__ == "__main__":
    generate_test_fd("visualization/test_field.fd")
