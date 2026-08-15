# train_knn_2layer.py 
import math, random, time

random.seed(7)
t0 = time.time()

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

ranges = [(10,40),(10,40),(1.5,3.0),(1.0,2.5),(0.05,0.5)]
X = [[(p[i]-ranges[i][0])/(ranges[i][1]-ranges[i][0]) for i in range(5)] for p in X_raw]

# 3. Train/Test Split
idx = list(range(N)); random.shuffle(idx)
te, tr = idx[:100], idx[100:]
X_tr = [X[i] for i in tr]
Y_tr = [Y[i] for i in tr]

def knn_predict(x_test, k=7):
    dists = []
    for i, x_tr in enumerate(X_tr):
        d = math.sqrt(sum((x_tr[j] - x_test[j])**2 for j in range(5)))
        dists.append((d, Y_tr[i]))
    dists.sort(key=lambda item: item[0])
    neighbors = dists[:k]
    n_freq = len(Y_tr[0])
    pred = [0.0] * n_freq
    for _, y in neighbors:
        for f in range(n_freq):
            pred[f] += y[f]
    return [p / k for p in pred]

print("\nEvaluating KNN Surrogate (k=7)...")
ss_res = ss_tot = 0.0
ymean = sum(Y[si][k] for si in te for k in range(50))/(len(te)*50)

preds = []
for i, si in enumerate(te):
    p = knn_predict(X[si], k=7)
    preds.append(p)
    for k in range(50):
        ss_res += (p[k]-Y[si][k])**2
        ss_tot += (Y[si][k]-ymean)**2
    if (i+1)%20 == 0:
        print(f"  Processed {i+1}/{len(te)} test samples... ({time.time()-t0:.1f}s)")

R2 = 1-ss_res/ss_tot if ss_tot > 0 else 0
print(f"\n>>> KNN TEST R^2 = {R2:.4f}   (1.000 = Perfect!)")

for i, si in enumerate(te[:2]):
    p = preds[i]
    print(f"\nSample: d1={X_raw[si][0]:.1f}um, d2={X_raw[si][1]:.1f}um, a1={X_raw[si][2]:.2f}, a2={X_raw[si][3]:.2f}, tau={X_raw[si][4]:.3f}ps")
    for k in range(0, 50, 6):
        f = 0.5 + 3.5*k/49
        print(f"{f:5.2f} THz | true {'#'*int(Y[si][k]*40):<40s} {Y[si][k]:.2f}")
        print(f"          | pred {'+'*int(p[k]*40):<40s} {p[k]:.2f}")

print(f"\nTotal time: {time.time()-t0:.1f}s")
input("Press Enter...")
