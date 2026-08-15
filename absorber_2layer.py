# absorber_2layer.py - 
import math

eta_0 = 377.0
n_s   = 1.5
Y_0   = 1.0/eta_0
Y_s   = Y_0*n_s
c     = 3e8

tau     = 1.07e-13
alpha_1 = 2.0
alpha_2 = 1.8
f_01    = 1e12
f_02    = 2e12
d_1     = 30e-6
d_2     = 20e-6

R_1 = eta_0/alpha_1
L_1 = tau*R_1
C_1 = (1.0/(2*math.pi*f_01)**2)/L_1

R_2 = eta_0/alpha_2
L_2 = tau*R_2
C_2 = (1.0/(2*math.pi*f_02)**2)/L_2

print("Laye 1: R1=%.2f ohm, L1=%.2f pH, C1=%.3f fF" % (R_1, L_1*1e12, C_1*1e15))
print("Laye 2: R2=%.2f ohm, L2=%.2f pH, C2=%.3f fF" % (R_2, L_2*1e12, C_2*1e15))

def absorption(f):
    w = 2*math.pi*f
    Y_G1 = 1/(R_1 + 1j*w*L_1 + 1/(1j*w*C_1))
    Y_G2 = 1/(R_2 + 1j*w*L_2 + 1/(1j*w*C_2))
    beta_s = w*n_s/c
    t1 = math.tan(beta_s*d_1)
    if abs(t1) < 1e-12: t1 = 1e-12
    Y_1 = -1j*Y_s/t1
    Y_2 = Y_1 + Y_G1
    t2 = math.tan(beta_s*d_2)
    Y_3 = Y_s*(Y_2 + 1j*Y_s*t2)/(Y_s + 1j*Y_2*t2)
    Y_in = Y_3 + Y_G2
    Gamma = (Y_0 - Y_in)/(Y_0 + Y_in)
    return 1 - abs(Gamma)**2

N = 100
print("\nAbsorption Spectrum (2-layer disk absorber):")

with open("spectrum_2layer.csv", "w") as fh:
    fh.write("freq_THz,absorption\n")
    for i in range(N):
        f = (0.01 + 4.99*i/(N-1))*1e12
        A = absorption(f)
        fh.write("%.4f,%.4f\n" % (f/1e12, A))
        if i % 5 == 0:
            print("%5.2f THz |%s %.3f" % (f/1e12, '#'*int(A*50), A))

print("\n>>> spectrum_2layer.csv saved!")
input("Press Enter...")
