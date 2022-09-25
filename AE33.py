from matplotlib.dates import DateFormatter
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
from pandas.plotting import register_matplotlib_converters
import datetime, os, warnings;  warnings.filterwarnings('ignore')
ae33keys=['Date','Time','Timebase',
        'RefCh1','Sen1Ch1','Sen2Ch1','RefCh2','Sen1Ch2','Sen2Ch2','RefCh3','Sen1Ch3','Sen2Ch3','RefCh4','Sen1Ch4','Sen2Ch4','RefCh5','Sen1Ch5','Sen2Ch5','RefCh6','Sen1Ch6','Sen2Ch6','RefCh7','Sen1Ch7','Sen2Ch7',
        'Flow1','Flow2','FlowC',
        'Pressure(Pa)','Temperature(°C)','BB(%)',
        'ContTemp','SupplyTemp',
        'Status','ContStatus','DetectStatus','LedStatus','ValveStatus','LedTemp',
        'BC11','BC12','BC1','BC21','BC22','BC2','BC31','BC32','BC3','BC41','BC42','BC4','BC51','BC52','BC5','BC61','BC62','BC6','BC71','BC72','BC7',
        'K1','K2','K3','K4','K5','K6','K7',
        'TapeAdvCount','ID_com1','ID_com2','ID_com3']
wavelengths = {
            370: 'BC1',
            470: 'BC2',
            520: 'BC3',
            590: 'BC4',
            660: 'BC5',
            880: 'BC6',
            950: 'BC7'
            }
units = {
            'Timebase': 'seconds',
            'Flow1': 'cc/min',
            'Flow2': 'cc/min',
            'FlowC': 'cc/min',
            'Pressure': 'Pa',
            'Temperature': '$^\circ$C',
            'BB': '%',
            'ContTemp': '$^\circ$C',
            'SupplyTemp': '$^\circ$C',
            'BC11': 'ng/m$^3$',
            'BC12': 'ng/m$^3$',
            'BC1': 'ng/m$^3$',
            'BC21': 'ng/m$^3$',
            'BC22': 'ng/m$^3$',
            'BC2': 'ng/m$^3$',
            'BC31': 'ng/m$^3$',
            'BC32': 'ng/m$^3$',
            'BC3': 'ng/m$^3$',
            'BC41': 'ng/m$^3$',
            'BC42': 'ng/m$^3$',
            'BC4': 'ng/m$^3$',
            'BC51': 'ng/m$^3$',
            'BC52': 'ng/m$^3$',
            'BC5': 'ng/m$^3$',
            'BC61': 'ng/m$^3$',
            'BC62': 'ng/m$^3$',
            'BC6': '$\mu$g/m$^3$',
            'BC71': 'ng/m$^3$',
            'BC72': 'ng/m$^3$',
            'BC7': 'ng/m$^3$',
            }
def read_ae33():
    file_dir = './AE33 0409-0426/'# where to read AE33 (.dat)
    files = os.listdir(file_dir)
    df1 = pd.read_table(os.path.join(file_dir, files[0]),skiprows=8,header=None,sep='\s+')  #read the first

    for file in files[1:]:# continue to read other files
        df2 = pd.read_table(os.path.join(file_dir, file),skiprows=8,header=None,sep='\s+')
        df1 = pd.concat((df1, df2), axis=0, join='inner')
    df=df1
    del df2,df1
    df=df.reset_index(drop=True)
    df.columns=ae33keys
    df['Dateandtime']=df['Date']+' '+df['Time'] # connect date and time
    pd.to_datetime(df['Dateandtime'],format='%Y/%m/%d %H:%M:%S')
    # optional：use data on the hour
    df = df[df['Dateandtime'].apply(lambda x:x[-6:]==':00:00')]
    
    df=df.reset_index(drop=True)
    df['Dateandtime']=pd.to_datetime(df['Dateandtime'],format='%Y/%m/%d %H:%M:%S')
    # deal with BCX (unit conversion: ng/m3->μg/m3)
    for i in ['BC1','BC2','BC3','BC4','BC5','BC6','BC7']:
        df[i]=df[i]/1000     
    return df

def create_plot( x, y, yunits,  ytitle, y1):
    '''
    y1, y1title: [optional]
    y & y1: left & right
    '''
    plt.style.use('bmh')
    plt.rcParams['axes.unicode_minus'] = False 
    plt.rcParams['font.sans-serif'] = ['Times New Roman']
    register_matplotlib_converters()
    
    # definitions for the axes
    left, width = 0.1, 0.7
    bottom, height = 0.15, 0.75
    spacing = 0.025
    box_width = 1 - (1.5*left + width + spacing)

    rect_scatter = [left, bottom, width, height]
    rect_box = [left + width + spacing, bottom, box_width, height]

    # start with a rectangular Figure
    box = plt.figure(figsize=(12, 6))

    ax = plt.axes(rect_scatter)
    ax.tick_params(direction='in', top=False, right=True)
    ax_box = plt.axes(rect_box)
    ax_box.tick_params(direction='in', labelleft=False, labelbottom=False)

    # now determine nice limits by hand:
    lim0 = y.min()
    lim1 = y.max()
    extra_space = (lim1 - lim0)/10
    # the line plot:
    line1 = ax.plot( x, y ,c='black',lw=0.5)
    ax.set_ylabel(ytitle + ' (' + yunits + ')')
    ax.xaxis.set_major_formatter(DateFormatter('%b-%d'))
    ax.set_ylim((lim0-extra_space, lim1+extra_space))
    # the scatter(outlier) plot:
    boxdict={
        # 'max':y.dropna().max(),  # 有问题，得到的是包含异常值的max
        'Q3':np.percentile(y.dropna(), 75),
        'median':np.median(y.dropna()),
        'Q1':np.percentile(y.dropna(), 25),
        'min':y.dropna().min()
    }
    # print(boxdict)
    QR=boxdict['Q3'] - boxdict['Q1']
    low_limit=boxdict['Q1'] - 1.5 * QR
    up_limit=boxdict['Q3'] + 1.5 * QR
    outliers=y[(y < low_limit) + (y > up_limit)]
    ## print('outliers:',outliers)
    scatter1 = ax.scatter(x[outliers.index],outliers,c='black',marker='o',edgecolor='k',alpha=0.75,zorder=2)
    # twinx
    ax2=ax.twinx()
    ax2.tick_params(axis='y',which='major',direction='in')
    ax2.set_yticks([0,45,90,135,180,225,270,315,360])
    ax2.set_yticklabels(['N','NE','E','SE','S','SW','W','NW','N'])
    # for ticklabel in ax2.yaxis.get_ticklabels():
    #     ticklabel.set_position([-1,-1])

    scatter2 = ax2.scatter( x, y1 ,c='black',marker='D',s=4)
    ax.legend([scatter1,scatter2],['outliers','Relative wind orient'],loc='upper left')
    # the box plot:
    meanpointprops = dict(marker='D')
    medianlineprops = dict(color='black')
    ax_box.boxplot(y.dropna(), showmeans=True, meanprops=meanpointprops, medianprops=medianlineprops)
    ax_box.set_ylim(ax.get_ylim())
    mu = y.mean()
    sigma = y.std()
    text = r'$\mu={0:.2f},\ \sigma={1:.3f}$'.format(mu, sigma)
    ax_box.text(1, lim1 + extra_space/2, text, horizontalalignment="center", verticalalignment="center")
    # save the figure
    today = datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d')
    plt.savefig("./pic/{}_boxplot".format(today), dpi=600)
    plt.close()

def main():
    df=read_ae33()
    lamda:int=880   # Select the wavelength to read
    BCkey = str(wavelengths.get(lamda))
    unit = units.get(BCkey) 
    create_plot( x=df['Dateandtime'], y=df[BCkey], yunits=unit, ytitle="Equivalent Black Carbon")

if __name__ == '__main__':
    main()