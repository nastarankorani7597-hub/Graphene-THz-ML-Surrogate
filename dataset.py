
import math
import random

eta_0 = 377.0        
n_s   = 1.5          
Y_0   = 1.0 / eta_0
Y_s   = Y_0 * n_s
c     = 3e8          

def calc_absorption(freq, d, a, E_F, tau, alpha):
    
    w = 2 * math.pi * freq
  
    R_1 = (eta_0 / alpha) * (1.0 / E_F)  # scaling با E_F
    
    # L_1 = tau * R_1
    L_1 = tau * R_1
    
    f_0 ≈ 1 THz 
    # LC = 1/(2πf_0)^2 => C_1 = 1/(L_1 * (2πf_0)^2)
    f_0 = 1e12  
    LC_target = 1.0 / (2 * math.pi * f_0) ** 2
    C_1 = LC_target / L_1
    
    Z_G = R_1 + 1j * w * L_1 + 1 / (1j * w * C_1)
    Y_G = 1.0 / Z_G
    
    beta_s = w * n_s / c
    t = math.tan(beta_s * d)
    if abs(t) < 1e-12:
        t = 1e-12
    Y_Au = -1j * Y_s / t
    
    Y_in = Y_Au + Y_G
    
    Gamma = (Y_0 - Y_in) / (Y_0 + Y_in)
    
    A = 1 - abs(Gamma) ** 2
    return A

random.seed(42)  

N_samples = 1000      
N_freq = 50           
freq_min = 0.5e12     
freq_max = 2.0e12     

freqs = [freq_min + (freq_max - freq_min) * i / (N_freq - 1) for i in range(N_freq)]

param_ranges = {
    'd_um':   (20, 80),      
    'a_um':   (20, 80),     
    'E_F':    (0.3, 1.0),   
    'tau_ps': (0.05, 0.5),   
    'alpha':  (1.0, 2.5),    
}

print("=" * 60)
print("Graphene THz Absorber - Dataset Generator")
print("=" * 60)
print(f"Generating {N_samples} samples × {N_freq} frequency points")
print(f"Frequency range: {freq_min/1e12:.2f} - {freq_max/1e12:.2f} THz")
print("=" * 60)


with open("dataset.csv", "w") as fh:
    header = ["d_um", "a_um", "E_F", "tau_ps", "alpha"]
    header += [f"A_{freq/1e12:.3f}THz" for freq in freqs]
    fh.write(",".join(header) + "\n")
    
    for k in range(N_samples):
        d_um   = random.uniform(*param_ranges['d_um'])
        a_um   = random.uniform(*param_ranges['a_um'])
        E_F    = random.uniform(*param_ranges['E_F'])
        tau_ps = random.uniform(*param_ranges['tau_ps'])
        alpha  = random.uniform(*param_ranges['alpha'])
        
        d = d_um * 1e-6
        a = a_um * 1e-6
        tau = tau_ps * 1e-12
        
        spectrum = []
        for freq in freqs:
            A = calc_absorption(freq, d, a, E_F, tau, alpha)
            spectrum.append(A)
        
        row = [f"{d_um:.2f}", f"{a_um:.2f}", f"{E_F:.3f}", f"{tau_ps:.3f}", f"{alpha:.3f}"]
        row += [f"{A:.4f}" for A in spectrum]
        fh.write(",".join(row) + "\n")
        
        if (k + 1) % 100 == 0:
            print(f"Progress: {k+1}/{N_samples} samples generated")

print("=" * 60)
print(f" dataset.csv saved: {N_samples} samples × {N_freq} frequencies")
print(f"File size: ~{N_samples * (N_freq + 5) * 10 / 1024:.1f} KB")
print("=" * 60)

print("\n Sample #1 (first row):")
with open("dataset.csv", "r") as fh:
    fh.readline()  # skip header
    line = fh.readline().strip().split(",")
    params = line[:5]
    spectrum = [float(x) for x in line[5:]]
    peak_idx = spectrum.index(max(spectrum))
    peak_freq = freqs[peak_idx] / 1e12
    peak_abs = spectrum[peak_idx]
    
    print(f"Parameters: d={params[0]} μm, a={params[1]} μm, E_F={params[2]} eV, τ={params[3]} ps, α={params[4]}")
    print(f"Peak absorption: {peak_abs:.3f} at {peak_freq:.2f} THz")
    print("\nText plot of absorption spectrum:")
    for i, A in enumerate(spectrum):
        if i % 5 == 0:  
            bar = "#" * int(A * 40)
            print(f"{freqs[i]/1e12:5.2f} THz |{bar:<40s}| {A:.3f}")

print("\n" + "=" * 60)
print(" Next step: Train a Forward Model (neural network) to predict these spectra!")
print("=" * 60)

input("\nPress Enter to exit...")
