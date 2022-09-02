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
    file_dir = './AE33 0409-0426/'# 存放AE33文件（.dat）的目录
    files = os.listdir(file_dir)
    df1 = pd.read_table(os.path.join(file_dir, files[0]),skiprows=8,header=None,sep='\s+')  #先读取第一个

    for file in files[1:]:#再拼接其余的
        df2 = pd.read_table(os.path.join(file_dir, file),skiprows=8,header=None,sep='\s+')
        df1 = pd.concat((df1, df2), axis=0, join='inner')
    df=df1
    del df2,df1
    df=df.reset_index(drop=True)
    df.columns=ae33keys
    df['Dateandtime']=df['Date']+' '+df['Time'] # 合并日期与时刻，方便后续计算
    pd.to_datetime(df['Dateandtime'],format='%Y/%m/%d %H:%M:%S')
    # optional：取用整点时刻数据
    df = df[df['Dateandtime'].apply(lambda x:x[-6:]==':00:00')]
    
    df=df.reset_index(drop=True)
    for i in range(len(df)):
        df['Dateandtime'][i]=datetime.datetime.strptime(str(df['Dateandtime'][i]),'%Y/%m/%d %H:%M:%S')
    return df

def create_plot( x, y, yunits, title, ytitle):
    plt.style.use('ggplot')
    register_matplotlib_converters()
    
    # definitions for the axes
    left, width = 0.1, 0.7
    bottom, height = 0.15, 0.75
    spacing = 0.005
    box_width = 1 - (1.5*left + width + spacing)

    rect_scatter = [left, bottom, width, height]
    rect_box = [left + width + spacing, bottom, box_width, height]

    # start with a rectangular Figure
    box = plt.figure(figsize=(12, 6))

    ax_scatter = plt.axes(rect_scatter)
    ax_scatter.tick_params(direction='in', top=False, right=True)
    ax_box = plt.axes(rect_box)
    ax_box.tick_params(direction='in', labelleft=False, labelbottom=False)

    # now determine nice limits by hand:
    lim0 = y.min()
    lim1 = y.max()
    extra_space = (lim1 - lim0)/10
    # the scatter plot:
    ax_scatter.plot( x, y )
    ax_scatter.set_xlabel('date')
    ax_scatter.set_ylabel(ytitle + ' (' + yunits + ')')
    ax_scatter.set(title=title)
    ax_scatter.xaxis.set_major_formatter(DateFormatter('%b-%d'))
    ax_scatter.set_ylim((lim0-extra_space, lim1+extra_space))
    # the box plot:
    meanpointprops = dict(marker='D')
    medianlineprops = dict(color='black')
    ax_box.boxplot(y.dropna(), showmeans=True, meanprops=meanpointprops, medianprops=medianlineprops)
    boxdict={
        # 'max':y.dropna().max(),  # 有问题，得到的是包含异常值的max
        'Third quartile':np.percentile(y.dropna(), 75),
        'median':np.median(y.dropna()),
        'First quartile':np.percentile(y.dropna(), 25),
        'min':y.dropna().min()
    }
    print(boxdict)
    ax_box.set_ylim(ax_scatter.get_ylim())
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
    lamda:int=880   # 选取分析的波长（拼写错误是因为lambda是关键字）
    # 目标数据（挑选范围为：BCXX,BCX,BB）
    # BCkey = 'BB'
    BCkey = str(wavelengths.get(lamda))
    if BCkey!='BB':
        y = df[BCkey]/1000  # 单位转换: ng/m3->μg/m3     
    # 单位
    unit = units.get(BCkey) 
    # 图题                 
    plotTitle = "Aethalometer Model AE33"
    if BCkey!='BB':
        plotTitle = plotTitle + " ($\lambda=$" + str(lamda) + "nm)"
    # y轴标题
    if BCkey=='BB':
        ytitle = "Biomass Burning Fraction"
    else:
        ytitle="Equivalent Black Carbon"
    x = df.Dateandtime
    create_plot( x, y, yunits=unit, title=plotTitle, ytitle=ytitle)

if __name__ == '__main__':
    main()