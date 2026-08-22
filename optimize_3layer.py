# optimize_3layer.py - 
# Cost = -mean(Absorption) 
import math

eta_0=377.0; n_s=1.5; Y_0=1.0/eta_0; Y_s=Y_0*n_s; c=3e8
tau=1.07e-13
f_01=1e12; f_02=1.5e12; f_03=2e12

def absorption(f, d1, d2, d3, a1, a2, a3):
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

freqs=[(0.8+(2.2-0.8)*i/29)*1e12 for i in range(30)]

best=None
for d1_um in range(10,41,5):
    for d2_um in range(10,31,5):
        for d3_um in range(5,21,5):
            for a1 in (1.5,2.0,2.5):
                for a2 in (1.4,1.8,2.2):
                    for a3 in (1.4,1.8,2.2):
                        m=sum(absorption(f,d1_um*1e-6,d2_um*1e-6,d3_um*1e-6,a1,a2,a3) for f in freqs)/30
                        if best is None or m>best[0]:
                            best=(m,d1_um,d2_um,d3_um,a1,a2,a3)
    print("d1=%2d um | best: d1=%d d2=%d d3=%d a1=%.1f a2=%.1f a3=%.1f meanA=%.3f"%(d1_um,best[1],best[2],best[3],best[4],best[5],best[6],best[0]))

m,d1u,d2u,d3u,a1,a2,a3=best
print("\n>>> BEST: d1=%d d2=%d d3=%d um | a1=%.1f a2=%.1f a3=%.1f | meanA(0.8-2.2)=%.3f"%(d1u,d2u,d3u,a1,a2,a3,m))
print(">>> Thesis 4-7-3-1 result: d1=25, d2=20, d3=10 um (99% at 0.9/1.5/2.1)")

d1=d1u*1e-6; d2=d2u*1e-6; d3=d3u*1e-6
N=100
rows=[]
with open("spectrum_3layer_opt.csv","w") as fh:
    fh.write("freq_THz,absorption\n")
    for i in range(N):
        f=(0.1+2.9*i/(N-1))*1e12
        A=absorption(f,d1,d2,d3,a1,a2,a3)
        rows.append((f/1e12,A))
        fh.write("%.4f,%.4f\n"%(f/1e12,A))

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
    print(">>> Bandwidth(A>=0.9): %.2f-%.2f THz | Bw=%.2f | fc=%.2f | FBW=%.0f%%"%(fmin,fmax,Bw,fc,FBW))
print(">>> spectrum_3layer_opt.csv saved")
input("Press Enter...")
