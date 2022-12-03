import numpy as np
import pandas as pd 
from pandas.plotting import register_matplotlib_converters
from matplotlib.dates import DateFormatter
import proplot as pplt 
import datetime
df = pd.read_csv('./BCx.csv', header=0)
# print(df)
wavelengths = {370:'BC1',470:'BC2',520:'BC3',590:'BC4',660:'BC5',880:'BC6',950:'BC7'}
mac = {'BC1':18.47,'BC2':14.54,'BC3':13.14,'BC4':11.58,'BC5':10.35,'BC6':7.77,'BC7':7.19}


def main():
    for i in [370,470,520,590,660,880,950]:
        df['abs_{}'.format(i)] = df[wavelengths[i]] * mac[wavelengths[i]]
    # print(df)
    df['AAE_660950']=calc_aae(660,950)
    df['AAE_470660']=calc_aae(470,660) 
    df['AAE_470950']=calc_aae(470,950)
    df['AAE_370950']=calc_aae(370,950)
    df['AAE_370520']=calc_aae(370,520)
    df['Dateandtime']=pd.to_datetime(df['Dateandtime'],format='%Y-%m-%d %H:%M:%S')
    # pd.set_option('display.max_rows', None)
    plot_anal()
def calc_aae(lamda1, lamda2):# lamda1 < lamda2, unit:μm
    sigma1, sigma2 = df['abs_{}'.format(lamda1)], df['abs_{}'.format(lamda2)]
    return np.log10(sigma2/sigma1)/np.log10(lamda1/lamda2)
def plot_anal():
    '''
    绘制分析折线图
    '''
    pplt.rc['font.family'] = 'Times New Roman'     
    pplt.rc['axes.unicode_minus'] = False 
    fig, axs = pplt.subplots(figsize=(6, 6), nrows=5, ncols=1, sharex=True, sharey=False)
    register_matplotlib_converters()

    varnames=['AAE_660950','AAE_470660','AAE_470950', 'AAE_370950', 'AAE_370520']
    ylabels =['AAE$_{660-950}$','AAE$_{470-660}$','AAE$_{470-950}$','AAE$_{370-950}$','AAE$_{370-520}$']
    for ax,varname,ylabel in zip(axs,varnames,ylabels):
        y=df[varname]
        # y[np.isinf(y)]=np.nan

        ax.plot(df['Dateandtime'], y)
        ax.xaxis.set_major_formatter(DateFormatter('%b-%d'))
        ax.set_ylabel(ylabel)
        ax.set_xlabel(' ')
        ax.tick_params(direction='in', top=False, right=True)
        ax.format(xrotation=0,xminorlocator='day')
        
        y[np.isinf(y)] = np.nan
        std = np.std(y, ddof = 1) # 无偏std
        mu = np.nanmean(y)
        text = r'$\mu:{:.2f}, S:{:.2f}$'.format(mu, std)
        ax.text(0.8,0.9, text, transform=ax.transAxes)
    # print(box_info)
    # print('无偏std: ',np.std(y, ddof = 1))

    # save the figure
    today = datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d')
    fig.save("./pic/{}_BCx&AAE.png".format(today), dpi=600)

if __name__ == '__main__':
    main()