#!/usr/bin/env python3
"""Generate all PNG plots from wrdata files"""
import numpy as np, os
try:
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt; HAS=True
except: HAS=False; print("No matplotlib")

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def load(f):
    try: return np.loadtxt(f)
    except: return None

if HAS:
    # Id vs Vds
    fig,ax=plt.subplots(figsize=(8,6))
    for f,l in [('idvds_vgs1','Vgs=-1V'),('idvds_vgs3','Vgs=-3V'),('idvds_vgs5p4','Vgs=-5.4V')]:
        d=load(f)
        if d is not None and d.ndim==2:
            ax.plot(5.4-d[:,0], d[:,1]*1000, label=l)
    ax.set_xlabel('|Vds| (V)'); ax.set_ylabel('Id (mA)'); ax.set_title('Id vs Vds'); ax.legend(); ax.grid(True,alpha=0.3)
    fig.savefig('idvds_family.png',dpi=150); plt.close(); print("idvds_family.png")

    # Id vs Vgs
    fig,ax=plt.subplots(figsize=(8,6))
    for f,l in [('idvgs_dropout_tt27','TT 27C'),('idvgs_dropout_ss150','SS 150C')]:
        d=load(f)
        if d is not None and d.ndim==2:
            ax.plot(5.4-d[:,0], d[:,1], label=l)
    ax.axhline(50,color='r',ls='--',label='50mA spec'); ax.set_xlabel('|Vgs| (V)'); ax.set_ylabel('Id (mA)')
    ax.set_title('Id vs Vgs at Dropout'); ax.legend(); ax.grid(True,alpha=0.3)
    fig.savefig('idvgs_dropout.png',dpi=150); plt.close(); print("idvgs_dropout.png")

    # PVT bar chart
    pvt={}
    if os.path.exists('run.log'):
        for l in open('run.log'):
            for p in ['pvt_tt_m40','pvt_tt_27','pvt_tt_150','pvt_ss_m40','pvt_ss_27','pvt_ss_150','pvt_ff_m40','pvt_ff_27','pvt_ff_150']:
                if l.strip().startswith(p+':'):
                    try: pvt[p]=float(l.strip().split(':')[1].strip().split()[0])
                    except: pass
    if pvt:
        fig,ax=plt.subplots(figsize=(10,6))
        labels=[]; vals=[]; colors=[]
        cm={'tt':'steelblue','ss':'indianred','ff':'seagreen'}
        for c in ['ss','tt','ff']:
            for t,s in [(-40,'m40'),(27,'27'),(150,'150')]:
                k=f'pvt_{c}_{s}'
                if k in pvt: labels.append(f'{c.upper()} {t}C'); vals.append(pvt[k]); colors.append(cm.get(c,'gray'))
        ax.bar(range(len(labels)),vals,color=colors,alpha=0.8); ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels,rotation=45,ha='right'); ax.axhline(50,color='r',ls='--',label='50mA')
        ax.set_ylabel('Id (mA)'); ax.set_title('PVT Corners'); ax.legend(); ax.grid(True,alpha=0.3,axis='y')
        fig.tight_layout(); fig.savefig('pvt_id_dropout.png',dpi=150); plt.close(); print("pvt_id_dropout.png")

    # Cgs
    d=load('cgs_vs_freq')
    if d is not None and d.ndim==2:
        fig,ax=plt.subplots(figsize=(8,6))
        ax.semilogx(d[:,0],d[:,1]); ax.set_xlabel('Freq (Hz)'); ax.set_ylabel('Cgs (pF)')
        ax.set_title('Gate Capacitance'); ax.grid(True,alpha=0.3)
        fig.savefig('cgs_vs_vgs.png',dpi=150); plt.close(); print("cgs_vs_vgs.png")

    # gm
    d=load('gm_vs_id')
    if d is not None and d.ndim==2:
        fig,ax=plt.subplots(figsize=(8,6))
        mask=d[:,1]>0.1; ax.plot(d[mask,1],np.abs(d[mask,2]))
        ax.set_xlabel('Id (mA)'); ax.set_ylabel('gm (mA/V)'); ax.set_title('Transconductance')
        ax.grid(True,alpha=0.3)
        fig.savefig('gm_vs_id.png',dpi=150); plt.close(); print("gm_vs_id.png")

    # SOA
    d=load('soa_data')
    if d is not None and d.ndim==2:
        fig,ax=plt.subplots(figsize=(8,6))
        ax.plot(np.abs(d[:,2]),d[:,1],'b-',lw=2,label='Operating')
        ax.set_xlabel('|Vds| (V)'); ax.set_ylabel('Id (mA)'); ax.set_title('SOA')
        ax.legend(); ax.grid(True,alpha=0.3)
        fig.savefig('soa_overlay.png',dpi=150); plt.close(); print("soa_overlay.png")

print("Done")
