
import math, time

t0 = time.time()

# 1. Load dataset
X_raw, Y = [], []
with open("dataset.csv") as fh:
    fh.readline()
    for line in fh:
        v = line.strip().split(",")
        if len(v) < 55: continue
        X_raw.append([float(v[0]), float(v[3]), float(v[4])]) # d, tau, alpha
        Y.append([float(x) for x in v[5:55]])
N = len(X_raw)
print(f"Loaded {N} samples")

def inverse_predict(target_spectrum, k=7):
    
    dists = []
    for i, y_tr in enumerate(Y):
        d = math.sqrt(sum((y_tr[f] - target_spectrum[f])**2 for f in range(50)))
        dists.append((d, X_raw[i]))
    
    dists.sort(key=lambda item: item[0])
    neighbors = dists[:k]
    
    pred_params = [0.0, 0.0, 0.0]
    for _, params in neighbors:
        for p in range(3):
            pred_params[p] += params[p]
            
    return [p / k for p in pred_params], dists[0][0]

print("\n" + "="*60)
print("INVERSE DESIGN: find")
print("="*60)


target = []
for i in range(50):
    f = 0.5 + 1.5 * i / 49
    A = 1.0 / (1 + ((f - 1.2)/0.15)**2) 
    target.append(A)

print("\nTarget Spectrum: maximum the absorption of 1.20THz")
print("Visualizing target:")
for k_idx in range(0, 50, 6):
    f = 0.5 + 1.5 * k_idx / 49
    print(f"{f:5.2f} THz | target {'*'*int(target[k_idx]*40):<40s} {target[k_idx]:.2f}")

print("\n Inverse Model is calculating optimal parameters...")
pred_params, min_dist = inverse_predict(target, k=7)

print("\n Optimal Fabrication Parameters Predicted:")
print(f"   -> Dielectric thickness (d) = {pred_params[0]:.1f} μm")
print(f"   -> Relaxation time (tau)    = {pred_params[1]:.3f} ps")
print(f"   -> Matching coeff (alpha)   = {pred_params[2]:.2f}")
print(f"   (Confidence distance: {min_dist:.4f})")

print(f"\n Time taken: {(time.time()-t0)*1000:.1f} milliseconds")
print("="*60)
print("result!")
print("="*60)

input("\nPress Enter...")
