# dataset_3layer.py - 
import math, random

eta_0=377.0; n_s=1.5; Y_0=1.0/eta_0; Y_s=Y_0*n_s; c=3e8
f_01=1e12; f_02=1.5e12; f_03=2e12

def absorption(f, d1, d2, d3, a1, a2, a3, tau):
    w=2*math.pi*f
    R_1=eta_0/a1; L_1=tau*R_1; C_1=(1.0/(2*math.pi*f_01)**2)/L_1
    R_2=eta_0/a2; L_2=tau*R_2; C_2=(1.0/(2*math.pi*f_02)**2)/L_2
    R_3=eta_0/a3; L_3=tau*R_3; C_3=(1.0/(2*math.pi*f_03)**2)/L_3
    Y_G1=1/(R_1+1j*w*L_1+1/(1j*w*C_1))
    Y_G2=1/(R_2+1j*w*L_2+1/(1j*w*C_2))
    Y_G3=1/(R_3+1j*w*L_3+1/(1j*w*C_3))
    beta_s=w*n_s/c
    t1=math.tan(beta_s*d1)
    if abs(t1)<1e-12: t1=1e-12
    Y_1=-1j*Y_s/t1
    Y_2=Y_1+Y_G1
    t2=math.tan(beta_s*d2)
    Y_3=Y_s*(Y_2+1j*Y_s*t2)/(Y_s+1j*Y_2*t2)
    Y_4=Y_3+Y_G2
    t3=math.tan(beta_s*d3)
    Y_5=Y_s*(Y_4+1j*Y_s*t3)/(Y_s+1j*Y_4*t3)
    Y_in=Y_5+Y_G3
    G=(Y_0-Y_in)/(Y_0+Y_in)
    return 1-abs(G)**2

random.seed(42)
N_samples=1500
N_freq=50
freqs=[(0.1+(3.0-0.1)*i/(N_freq-1))*1e12 for i in range(N_freq)]

with open("dataset_3layer.csv","w") as fh:
    hdr=["d1_um","d2_um","d3_um","alpha1","alpha2","alpha3","tau_ps"]+["A_%03d"%i for i in range(N_freq)]
    fh.write(",".join(hdr)+"\n")
    for k in range(N_samples):
        d1=random.uniform(5,40)*1e-6
        d2=random.uniform(5,30)*1e-6
        d3=random.uniform(5,30)*1e-6
        a1=random.uniform(1.5,3.0)
        a2=random.uniform(1.2,2.5)
        a3=random.uniform(1.0,2.2)
        tau=random.uniform(0.05,0.5)*1e-12
        vals=[absorption(f,d1,d2,d3,a1,a2,a3,tau) for f in freqs]
        fh.write(",".join(["%.2f"%(d1*1e6),"%.2f"%(d2*1e6),"%.2f"%(d3*1e6),"%.3f"%a1,"%.3f"%a2,"%.3f"%a3,"%.3f"%(tau*1e12)]+["%.4f"%v for v in vals])+"\n")
        if (k+1)%300==0:
            print("Progress: %d/%d"%(k+1,N_samples))

print(">>> dataset_3layer.csv saved: %d samples x %d freq"%(N_samples,N_freq))
input("Press Enter...")
