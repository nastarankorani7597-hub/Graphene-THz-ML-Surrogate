# inverse_design_2layer.py - 
import math, time

t0 = time.time()

# 1. Load dataset
X_raw, Y = [], []
with open("dataset_2layer.csv") as fh:
    fh.readline()
    for line in fh:
        v = line.strip().split(",")
        if len(v) < 55: continue
        X_raw.append([float(v[i]) for i in range(5)]) # d1, d2, alpha1, alpha2, tau
        Y.append([float(x) for x in v[5:55]])
N = len(X_raw)
print(f"Loaded {N} samples (2-layer)")

# 2. Inverse KNN
def inverse_predict(target_spectrum, k=7):
    dists = []
    for i, y_tr in enumerate(Y):
        d = math.sqrt(sum((y_tr[f] - target_spectrum[f])**2 for f in range(50)))
        dists.append((d, X_raw[i]))
    dists.sort(key=lambda item: item[0])
    neighbors = dists[:k]
    pred_params = [0.0] * 5
    for _, params in neighbors:
        for p in range(5):
            pred_params[p] += params[p]
    return [p / k for p in pred_params], dists[0][0]

# 3. Target spectrum
print("\n" + "="*60)
print("INVERSE DESIGN: define")
print("="*60)

target = []
for i in range(50):
    f = 0.5 + 3.5 * i / 49
    A = 1.0 / (1 + ((f - 2.0)/1.2)**2)
    target.append(A)

print("\nTarget Spectrum:  ")
print("Visualizing target:")
for k_idx in range(0, 50, 6):
    f = 0.5 + 3.5 * k_idx / 49
    print(f"{f:5.2f} THz | target {'*'*int(target[k_idx]*40):<40s} {target[k_idx]:.2f}")

print("\n Inverse Model is calculating optimal 5 parameters...")
pred_params, min_dist = inverse_predict(target, k=7)

print("\n Optimal Fabrication Parameters Predicted:")
print(f"   -> Dielectric thickness 1 (d1) = {pred_params[0]:.1f} μm")
print(f"   -> Dielectric thickness 2 (d2) = {pred_params[1]:.1f} μm")
print(f"   -> Matching coeff 1 (alpha1)   = {pred_params[2]:.2f}")
print(f"   -> Matching coeff 2 (alpha2)   = {pred_params[3]:.2f}")
print(f"   -> Relaxation time (tau)       = {pred_params[4]:.3f} ps")
print(f"   (Confidence distance: {min_dist:.4f})")

print(f"\n Time taken: {(time.time()-t0)*1000:.1f} milliseconds")
print("="*60)
print(" >50!")
print("="*60)

input("\nPress Enter...")
