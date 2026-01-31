import numpy as np

def compute_fft(time, signal):
    """
    Computes the standard FFT of a time-domain signal.
    
    Args:
        time (np.array): Time array.
        signal (np.array): Signal value array.
        
    Returns:
        tuple: (freq_axis, fft_result)
    """
    dt = time[1] - time[0]
    n = len(time)
    
    fft_vals = np.fft.fft(signal)
    freqs = np.fft.fftfreq(n, d=dt)
    
    return freqs, fft_vals

def compute_dtft(time, signal, freq_range_hz=None):
    """
    Computes the Discrete Time Fourier Transform (DTFT) at specific frequencies.
    Replicates the logic of the legacy 'dtft.m' script.
    
    Args:
        time (np.array): Time array.
        signal (np.array): Signal value array.
        freq_range_hz (tuple or np.array): Array of frequencies (Hz) to evaluate, 
                                           or tuple (start, stop, step) to generate them.
                                           If None, defaults to logic similar to legacy code.
                                           
    Returns:
        tuple: (freq_axis_hz, dtft_result)
    """
    dt = time[1] - time[0]
    
    if freq_range_hz is None:
        # Default behavior mimicking legacy VIZ_plot.m roughly
        # w = pi*2*dt*0.5e6 : 0.00001 : pi*2*dt*10e6;
        # implied freq range ~ 0.5 MHz to 10 MHz with high resolution
        # Let's define a sensible default if not provided
        f_start = 0.5e6
        f_stop = 10e6
        f_step = 10e3 # Coarser than legacy 0.00001 rad normalized step for speed
        freqs = np.arange(f_start, f_stop, f_step)
    elif isinstance(freq_range_hz, (list, np.ndarray)):
        freqs = freq_range_hz
    elif isinstance(freq_range_hz, tuple):
        freqs = np.arange(*freq_range_hz)
    else:
        raise ValueError("Invalid freq_range_hz format")

    w = 2 * np.pi * freqs * dt # Normalized angular frequency (rad/sample)
    
    # Legacy DTFT: Y = X * exp(-i * k' * W)
    # X is 1xN, k is 0..N-1
    # W is 1xM
    # Result Y is 1xM
    
    n = np.arange(len(signal))
    
    # Vectorized computation: Y[w] = sum_n (x[n] * exp(-j * w * n))
    # Using matrix broadcasting
    # E_wk = exp(-j * n[:, None] * w[None, :]) 
    # This can be large matrix: N x M. 
    # If N=8000, M=1000, that's 8M elements -> complex128 -> 128MB. Fine.
    
    # Optimized: Y = signal @ exp(...)
    exponent = -1j * np.outer(n, w)
    exp_matrix = np.exp(exponent)
    dtft_vals = signal @ exp_matrix
    
    return freqs, dtft_vals

def compute_impedance(voltage_fft, current_fft):
    """
    Computes Impedance Z = V / I in frequency domain.
    
    Args:
        voltage_fft (np.array): FFT/DTFT of voltage.
        current_fft (np.array): FFT/DTFT of current.
        
    Returns:
        np.array: Complex impedance.
    """
    # Avoid division by zero
    with np.errstate(divide='ignore', invalid='ignore'):
        impedance = voltage_fft / current_fft
        impedance[current_fft == 0] = 0 
        
    return impedance
