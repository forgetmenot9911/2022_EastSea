from cProfile import label
from turtle import color
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

def plot_anal( x, y, yunits,  ytitle, y2):
    '''
    绘制分析折线图
    y1, y1title: [optional]
    y & y1: left & right
    '''
    from matplotlib.cbook import boxplot_stats 
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
    ax.set_ylabel(ytitle + ' (' + yunits + ')')
    ax.xaxis.set_major_formatter(DateFormatter('%b-%d'))
    ax.set_ylim((lim0-extra_space, lim1+extra_space))
    # 找到outliers:
    boxdict={
        # 'max':y.dropna().max(),  # 有问题，得到的是包含异常值的max
        'Q3':np.percentile(y.dropna(), 75),
        'median':np.median(y.dropna()),
        'Q1':np.percentile(y.dropna(), 25),
        'min':y.dropna().min()
    }
    QR=boxdict['Q3'] - boxdict['Q1']
    low_limit=boxdict['Q1'] - 1.5 * QR
    up_limit=boxdict['Q3'] + 1.5 * QR
    # outliers=y[(y < low_limit) + (y > up_limit)]
    spots = y2[y2['BC6'] > 3]
    # print('选择的高值点（已质控）：')
    # [print(x,y) for x,y in zip(spots['lon'],spots['lat'])]
    ## main Axe
    # scatter1 = ax.scatter(x[outliers.index],outliers,c='black',marker='o',edgecolor='k',alpha=0.75,zorder=2)
    line1 = ax.plot(x, y ,c='black',lw=0.5, zorder=1, label='$BC_{uncorrected}$')
    line2 = ax.plot(x[y2.index], y2['BC6'],c='red',lw=0.5, zorder=1, label='$BC_{corrected}$')
    scatter1 = ax.scatter(x[spots.index],spots['BC6'],c='black',marker='d')
    print('使用Taketani方法数据剩余：{:.2f}%'.format(len(y2['BC6'])/len(y)*100))
    ax.legend(loc='upper left')
    # quiver = ax.quiver(x[outliers.index], outliers, 
    #                 np.sin((y1[outliers.index]+180)/360*2*np.pi)*10, 
    #                 np.cos((y1[outliers.index]+180)/360*2*np.pi)*10,
    #                 color='blue')
    # # 可选：平滑处理（须在py39环境下）
    # import gma
    # ysmo = gma.math.Smooth(y, 5, 2)
    # ySG = ysmo.SavitzkyGolay(Polyorder=2, Delta=1, Mode='interp')
    # yME = ysmo.MovingAverage()
    # line_smooth = ax.plot(x, yME, c='tab:red')
    ## twinx
    # ax2=ax.twinx()
    # ax2.tick_params(axis='y',which='major',direction='in')
    # ax2.set_yticks([0,45,90,135,180,225,270,315,360])
    # ax2.set_yticklabels(['N','NE','E','SE','S','SW','W','NW','N'])
    # bar = ax2.bar(x[outliers.index], y1[outliers.index], width=0.05, alpha=0.5)
    ## the box plot:
    boxprops={"color":"red"}
    whiskerprops={"color":"red"}
    capprops={"color":"red"}
    medianprops={"color":"red"}
    ax_box.boxplot(y2['BC6'].dropna(), showfliers=False, 
        boxprops=boxprops,whiskerprops=whiskerprops,capprops=capprops,medianprops=medianprops)
    ax_box.set_ylim(ax.get_ylim())
    ax_box.set_yticks([0,1,2,3,4,5,6,7])
    ax_box.set_yticklabels([0,1,2,3,4,5,6,7])
    ax_box.yaxis.tick_right()

    [box_info] = boxplot_stats(y2['BC6'])
    # print(box_info)
    # print('无偏std: ',np.std(y, ddof = 1))
    median = box_info['med']#中位数
    mu = box_info['mean']#均值
    std = np.std(y2['BC6'], ddof = 1)#无偏标准差
    text = r'${:.2f} \pm {:.2f}$'.format(mu, std)
    ax_box.text(1, lim0 - extra_space/2, text, horizontalalignment="center", verticalalignment="center")
    # save the figure
    today = datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d')
    plt.savefig("./pic/{}_boxplot".format(today), dpi=600)
    plt.close()
    # return outliers

def main():
    df=read_ae33()
    lamda:int=880   # Select the wavelength to read
    BCkey = str(wavelengths.get(lamda))
    unit = units.get(BCkey) 
    outliers = plot_anal( x=df['Dateandtime'], y=df[BCkey], yunits=unit, ytitle="Equivalent Black Carbon")

if __name__ == '__main__':
    main()