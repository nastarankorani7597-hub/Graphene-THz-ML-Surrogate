# absorber.py  -  Single-Layer Graphene Disk Absorber
# Thesis Eqs. 148-158  (pure Python, no packages needed)
import math

eta0 = 377.0
n_s  = 1.5
Y0   = 1.0/eta0
Ys   = Y0*n_s
c    = 3e8

d     = 50e-6
tau   = 1.07e-13
alpha = 1.75
f0    = 1e12

R1 = eta0/alpha
L1 = tau*R1
C1 = (1.0/(2*math.pi*f0)**2)/L1
print("R1 = %.2f ohm | L1 = %.2f pH | C1 = %.3f fF" % (R1, L1*1e12, C1*1e15))

def absorption(f, d_val):
    w  = 2*math.pi*f
    ZG = R1 + 1j*w*L1 + 1/(1j*w*C1)     
        YG = 1.0/ZG
    beta = w*n_s/c
    t = math.tan(beta*d_val)
    if abs(t) < 1e-12: t = 1e-12
    YAu = -1j*Ys/t                       
    Yin = YAu + YG                    
    G   = (Y0-Yin)/(Y0+Yin)                
    return 1-abs(G)**2                   

N = 60
rows = []
print("\nAbsorption Spectrum (d=50um):")
for i in range(N):
    f = (0.05 + 1.90*i/(N-1))*1e12
    A = absorption(f, d)
    rows.append((f/1e12, A))
    print("%5.2f THz |%s %.3f" % (f/1e12, '#'*int(A*50), A))

fp, Ap = max(rows, key=lambda r: r[1])
print("\n>>> PEAK: %.2f THz , Absorption = %.3f" % (fp, Ap))

with open("spectrum.csv", "w") as fh:
    fh.write("freq_THz,absorption\n")
    for ft, A in rows:
        fh.write("%.4f,%.4f\n" % (ft, A))
print(">>> spectrum.csv saved (open it in Excel -> Insert Line Chart)")

print("\nTunability test:")
for d_test in (40e-6, 50e-6, 60e-6):
    rr = [(0.05+1.90*i/(N-1), absorption((0.05+1.90*i/(N-1))*1e12, d_test)) for i in range(N)]
    pf, pa = max(rr, key=lambda r: r[1])
    print("d = %d um -> peak %.2f THz (A=%.3f)" % (d_test/1e-6, pf, pa))

input("\nPress Enter to exit...")
