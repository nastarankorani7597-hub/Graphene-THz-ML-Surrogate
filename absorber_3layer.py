# absorber_3layer.py 
import math

eta_0=377.0; n_s=1.5; Y_0=1.0/eta_0; Y_s=Y_0*n_s; c=3e8

tau     = 1.07e-13
alpha_1 = 2.0
alpha_2 = 1.8
alpha_3 = 1.8
f_01    = 1e12      
f_02    = 1.5e12    
f_03    = 2e12     
d_1     = 30e-6
d_2     = 20e-6
d_3     = 10e-6

R_1=eta_0/alpha_1; L_1=tau*R_1; C_1=(1.0/(2*math.pi*f_01)**2)/L_1
R_2=eta_0/alpha_2; L_2=tau*R_2; C_2=(1.0/(2*math.pi*f_02)**2)/L_2
R_3=eta_0/alpha_3; L_3=tau*R_3; C_3=(1.0/(2*math.pi*f_03)**2)/L_3

print("L1: R=%.2f ohm | L2: R=%.2f ohm | L3: R=%.2f ohm" % (R_1, R_2, R_3))

def absorption(f):
    w=2*math.pi*f
    Y_G1=1/(R_1+1j*w*L_1+1/(1j*w*C_1))    
    Y_G2=1/(R_2+1j*w*L_2+1/(1j*w*C_2))      
    Y_G3=1/(R_3+1j*w*L_3+1/(1j*w*C_3))      
    beta_s=w*n_s/c                           
    t1=math.tan(beta_s*d_1)
    if abs(t1)<1e-12: t1=1e-12
    Y_1=-1j*Y_s/t1                           
    Y_2=Y_1+Y_G1                            
    t2=math.tan(beta_s*d_2)
    Y_3=Y_s*(Y_2+1j*Y_s*t2)/(Y_s+1j*Y_2*t2)
    Y_4=Y_3+Y_G2                             
    t3=math.tan(beta_s*d_3)
    Y_5=Y_s*(Y_4+1j*Y_s*t3)/(Y_s+1j*Y_4*t3)
    Y_in=Y_5+Y_G3                          
    G=(Y_0-Y_in)/(Y_0+Y_in)                 
    return 1-abs(G)**2                     

N=100
rows=[]
with open("spectrum_3layer.csv","w") as fh:
    fh.write("freq_THz,absorption\n")
    for i in range(N):
        f=(0.1+2.9*i/(N-1))*1e12
        A=absorption(f)
        rows.append((f/1e12,A))
        fh.write("%.4f,%.4f\n"%(f/1e12,A))

print("\nAbsorption Spectrum (3-layer disk absorber):")
for ft,A in rows[::2]:
    print("%5.2f THz |%s %.3f" % (ft, '#'*int(A*50), A))

thr=0.9
best_run,cur=[],[]
for ft,A in rows:
    if A>=thr: cur.append(ft)
    else:
        if len(cur)>len(best_run): best_run=cur
        cur=[]
if len(cur)>len(best_run): best_run=cur
if best_run:
    fmin,fmax=best_run[0],best_run[-1]
    Bw=fmax-fmin; fc=(fmax+fmin)/2; FBW=Bw/fc*100
    print("\n>>> Bandwidth(A>=0.9): %.2f-%.2f THz | Bw=%.2f | fc=%.2f | FBW=%.0f%%"%(fmin,fmax,Bw,fc,FBW))
    print(">>> Thesis target (Fig 4-64): band ~0.8-2.2 THz, peaks 99%% at 0.9/1.5/2.1")
print(">>> spectrum_3layer.csv saved")
input("Press Enter...")
