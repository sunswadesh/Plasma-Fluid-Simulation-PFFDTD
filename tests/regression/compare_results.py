import argparse
import numpy as np
import os
import sys

def parse_vc(filepath):
    try:
        # Assuming .vc format is handled by numpy loadtxt
        # If headers/indices exist, loadtxt might fail unless skipprows is used
        # VIZ_plot.m implies first row is index.
        data = np.loadtxt(filepath, skiprows=1)
        return data
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

def parse_fd(filepath):
    try:
        # .fd files have 4 lines of header
        data = np.loadtxt(filepath, skiprows=4)
        return data
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

def compare_file(golden_path, new_path, tolerance=1e-6):
    if not os.path.exists(golden_path):
        print(f"FAILED: Golden file {golden_path} missing.")
        return False
    if not os.path.exists(new_path):
        print(f"FAILED: New file {new_path} missing.")
        return False
        
    ext = os.path.splitext(golden_path)[1]
    
    if ext == '.vc':
        d1 = parse_vc(golden_path)
        d2 = parse_vc(new_path)
    elif ext == '.fd':
        d1 = parse_fd(golden_path)
        d2 = parse_fd(new_path)
    else:
        # Fallback binary/text comparison
         with open(golden_path, 'rb') as f1, open(new_path, 'rb') as f2:
             if f1.read() == f2.read():
                 print(f"PASS: {os.path.basename(golden_path)} (Binary Match)")
                 return True
             else:
                 print(f"FAIL: {os.path.basename(golden_path)} (Binary Mismatch)")
                 return False

    if d1 is None or d2 is None:
        return False
        
    if d1.shape != d2.shape:
        print(f"FAIL: {os.path.basename(golden_path)} Shape Mismatch {d1.shape} vs {d2.shape}")
        return False
        
    diff = np.abs(d1 - d2)
    max_diff = np.max(diff)
    
    if max_diff > tolerance:
        print(f"FAIL: {os.path.basename(golden_path)} Max Diff {max_diff:.2e} > {tolerance}")
        return False
    else:
        print(f"PASS: {os.path.basename(golden_path)} Max Diff {max_diff:.2e}")
        return True

def main():
    parser = argparse.ArgumentParser(description="PFFDTD Regression Tester")
    parser.add_argument("--golden_dir", required=True, help="Directory containing golden truth files")
    parser.add_argument("--new_dir", required=True, help="Directory containing new run files")
    args = parser.parse_args()
    
    files = os.listdir(args.golden_dir)
    all_passed = True
    
    print(f"comparing results...")
    print(f"Golden: {args.golden_dir}")
    print(f"New:    {args.new_dir}")
    print("-" * 40)
    
    count = 0
    for f in files:
        if f.endswith('.vc') or f.endswith('.fd'):
            count += 1
            golden_f = os.path.join(args.golden_dir, f)
            new_f = os.path.join(args.new_dir, f)
            
            if not compare_file(golden_f, new_f):
                all_passed = False
    
    if count == 0:
        print("Warning: No .vc or .fd files found in golden directory.")
    
    print("-" * 40)
    if all_passed and count > 0:
        print("REGRESSION TEST PASSED")
        sys.exit(0)
    else:
        print("REGRESSION TEST FAILED")
        sys.exit(1)

if __name__ == "__main__":
    main()
