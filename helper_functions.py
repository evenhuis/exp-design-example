import numpy as np

'''sets transparancey for violin plots'''
import matplotlib as mpl
def setAlpha(ax,a):
    ''' sets alpha for violinplots'''
    for art in ax.get_children():
        if isinstance(art, mpl.collections.PolyCollection):
            art.set_alpha(a)

''' read in the size data'''
import glob
import pandas as pd
def group_files( time ):
    files = glob.glob("data/series*_t={}.csv".format(time))
    df_from_each_file = (pd.read_csv(f) for f in files)
    df = pd.concat(df_from_each_file, ignore_index=True)
    df["Time"]=time
    return df

def plot_bars( df, ax, ):
    ind = range(len(df))
    ax.bar(ind,df['neg'],label="neg")
    ax.bar(ind,df['pos'],bottom=df['neg'], label="pos")

def plot_bar_comp(df,axs):
    ax=axs[0]
    plot_bars(df[df['code']=='C'],ax)
    ax.set_ylabel("Number of cells")
    ax.text(0.1,0.9,"Control",transform=ax.transAxes,fontsize=12)

    ax=axs[1]
    plot_bars(df[df['code']=='T'],ax)
    ax.set_ylabel("Number of cells")
    ax.set_xlabel("Field of view")
    ax.text(0.1,0.9,"Treatment",transform=ax.transAxes,fontsize=12);
    ax.legend()
    ax.set_ylim(0,1.2*np.max(df['pos']+df['neg']))

def read_data():
    df1 = group_files(1)
    df4 = group_files(4)

    df = pd.concat([df1,df4])
    df['Time']=pd.Categorical(df['Time'])
    return df

def plot_pval( pvals ,ax, plot_pvals=True,alpha=0.05,**kwargs):
    tmp=np.reshape( pvals,[-1,2])
    chance_under_thresh = list(map( lambda vec : sum(vec<alpha)/len(vec), pvals[:,:,1]))
    if(plot_pvals): ax.plot(tmp[:,0]+1*(0.5-np.random.rand(len(tmp[:,0]))),tmp[:,1],'.',color='b' )
    ax.plot( pvals[:,0,0], chance_under_thresh, '-o',color='r')
    ax.axhline(0.05,dashes=(5,5),color='red')
    ax.set_ylabel('p-values',color='b')
    ax.tick_params('y', colors='b')
    ax.set_ylim(0,1)
    
    ax2=ax.twinx()
    ax2.set_ylim(0,100)
    ax2.set_ylabel('Chance of sig',color='r')
    ax2.tick_params('y', colors='r')
