from distutils.log import error
import pandas as pd 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime, os, warnings;  warnings.filterwarnings('ignore')
from meteo import read_meteo
from AE33 import read_ae33,plot_anal,wavelengths,units
from route import plot_route,plot_dere
plt.rcParams['axes.unicode_minus'] = False 
plt.rcParams['font.sans-serif'] = ['Times New Roman']

def plot_seaborn(x,y,mark):
    from scipy.stats import pearsonr
    '''
    mark:'reg','joint_reg'
    '''
    corr = pd.concat([x, y], axis=1).corr()
    print(corr)
    (r, p)=pearsonr(x, y)
    print('r= '+str(r)+', p= '+str(p))
    f, ax = plt.subplots(figsize=(4, 6))
    if mark == 'joint_reg':
        jg = sns.jointplot(x , y ,kind = 'reg')
        # ('r='+str(r)+'\n p='+str(p))
    if mark == 'reg':
        sns.regplot(x , y)
    today = datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d')
    plt.savefig('./pic/{}_{}Seaborn'.format(today,mark),dpi=600)
    plt.close()

def plot_barBConLAND():
    plt.rcParams['font.size']=5
    plt.rcParams.update({'figure.autolayout': True})
    plt.style.use('fivethirtyeight')
    fig, ax = plt.subplots(figsize=(8,4))
    # spotsOnland = ['Qingdao \n(spring, rural)', 
    #             'Nanjing \n(spring, suburb)', 
    #             'Shanghai \n(spring, edu. & commercial)', 
    #             'Ningbo \n(autumn, suburb)', 
    #             'Xiamen \n(annual, suburb)']
    spotsOnland = ['Qingdao', 'Nanjing', 'Shanghai', 'Ningbo', 'Xiamen','This cruise']
    conc = [1.53, 2.27, 2.16, 1.39, 4.27, 1.41]
    error = [1.33, 1.4, 0.97, 0, 1.875, 0.924]
    y_pos = np.arange(len(spotsOnland))
    errorbar = ax.errorbar( conc, y_pos, xerr=error, ecolor='k',elinewidth=0.5,marker='s',mfc='orange',
	                        mec='k',mew=1,ms=10,alpha=1,capsize=5,capthick=3,linestyle="none")
    # ax.bar_label(hbars, labels=['±%.2f' % e for e in error], padding=8)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels=spotsOnland, fontdict={'fontsize':12})
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Conc. [$\mu g \cdot m^{-3}$]')
    today = datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d')
    plt.savefig('./pic/{}_spotsOnland'.format(today),dpi=600, bbox_inches='tight', pad_inches=0)
    plt.close()
def scatterLinear(ax, model, x, y, c):
    '''
    散点图+线性回归
    '''
    from scipy.stats import pearsonr
    ax.scatter(x, y,c=c)
    model.fit(x, y)
    ax.plot(x, model.predict(x),color=c)
    # print(x.ravel().shape, np.array(y).shape)
    (r, p)=pearsonr(x.ravel(), np.array(y))
    text = '$R$ = {:.4f}{}$p$ = {:.3f}'.format(r, '\n', p)
    ax.text(0.7,0.9, text, transform=ax.transAxes)
def plot_BCandDistance(df):
    import proplot as pplt 
    from sklearn.linear_model import LinearRegression
    model = LinearRegression()
    pplt.rc['font.family'] = 'Times New Roman' 
    fig = pplt.figure(wspace=2, refwidth='20em')
    axs = fig.subplots(nrows=2, ncols=2)
    scatterLinear(axs[0], model, df.BC6[37:53, np.newaxis], df.lon[37:53],c='blue')
    scatterLinear(axs[1], model, df.BC6[70:103, np.newaxis], df.lon[70:103],c='orange')
    scatterLinear(axs[2], model, df.BC6[170:189, np.newaxis], df.lon[170:189],c='green')
    scatterLinear(axs[3], model, df.BC6[281:295, np.newaxis], df.lon[281:295],c='red')
    for ax in axs:
        ax.set_ylim([122, 126])
        ax.set_xlim([0, 6]) 
    axs.format(abc='a)', abcloc='ul',facecolor=None,xlabel='eBC',ylabel='Longitude [deg]')
    today = datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d')
    fig.save('./pic/{}_BCandDistance.png'.format(today), dpi=600)
def main():
    # ## 绘制陆上BC条状图
    # plot_barBConLAND()
    # quit()

    meteoinfo = read_meteo(markHour=True)
    ae33info  = read_ae33()

    # ### 绘制往返航线图
    # plot_dere(meteoinfo)
    # quit()
    df = pd.merge(meteoinfo,ae33info,on='Dateandtime')
    del meteoinfo,ae33info

    # 选取30 deg N附近的点，以便研究BC与离岸距离之间的关系
    # plot_dere(df)
    plot_BCandDistance(df)
    quit()

    lamda:int=880   # Select the wavelength to read
    BCkey = str(wavelengths.get(lamda))
    unit = units.get(BCkey) 

    # # 提取相对风向在90-270之间的数据，记为背风数据（Leeward, lw）
    # lw = df['orient_relative']
    # lw = lw[(lw>90) & (lw<270)]
    # # 提取船速为0的数据，记为s0
    # s0 = df['speed_zhenFeng']
    # s0 = s0[s0 == 0]
    # # 提取 1 min 真风速风向，记为ws1和wd1
    # ws1 = df['speed_true_1min']
    # wd1 = df['orient_true_1min']
    # # 提取相对风速小于7.5的数据，记为弱风（weak wind，ww）
    # ww = df['speed_relative']
    # ww = ww[ww<7.5]
   
    ## plot
    outliers = plot_anal(x=df['Dateandtime'], y=df[BCkey], yunits=unit, ytitle="Equivalent Black Carbon 880nm", y1=df['orient_relative'])
    # outliersInfo = pd.concat([df['Dateandtime'][outliers.index], df['lat'][outliers.index], df['lon'][outliers.index]], axis=1)
    # outliersInfo.to_excel('./output/outliers.xlsx')
    
    # 可选：剔除异常值（outliers）
    df = df.drop(index=outliers.index)
    
    # # 提取BC（880nm）,'press_1min','temp_1min','rh_1min','speed_true_1min'等物理量，并保存
    # df1 = df[['BC6','press_1min','temp_1min','rh_1min','speed_true_1min','lat','lon']]
    # df1.to_csv('df1.csv',index=False)

    # # 提取各波段BC：BC1(370nm)、BC2(470nm)、BC3(520nm)、BC4(590nm)、BC5(660nm)、BC6(880nm)、BC7(950nm), 并保存
    # df2 = df[['Dateandtime','BC1','BC2','BC3','BC4','BC5','BC6','BC7']]
    # print(df2)
    # df2.to_csv('BCx.csv',index=False)

    # 提取30 deg N的观测点
    # lat = df['lat']
    # print(min(lat, key=lambda x: abs(x - 30)))
    # n30 = df[df['lat']==30.000021666666665]
    # print(n30)


    # # 提取船速小于2.5的数据，记为低速航行（ls）
    # ls = df[df['speed_GPS']<1]
    # # 提取停船时刻数据（speed_GPS==0）
    # stp = df[df['speed_GPS']==0]
    # df_wwls = df[(df['speed_GPS']<0.6) & (df['speed_relative']<7.5)]
   
    ## 绘制随航BC浓度变化图
    # plot_route(df,BCkey,outliers)

    ### 回归绘图
    # plot_seaborn(x = df_wwls[BCkey], y = df_wwls['speed_GPS'], mark='reg')
    # plot_seaborn(x = df_wwls[BCkey], y = df_wwls['speed_GPS'], mark='joint_reg')
    # plot_seaborn(x = df[BCkey][outliers.index], y = df['orient_relative'][outliers.index], mark='joint_reg')
    # plot_seaborn(x = df[BCkey][lw.index], y = lw, mark='reg')
    # plot_seaborn(x = df[BCkey][outliers.index], y = wd1[outliers.index], mark='joint_reg')
    


if __name__ == '__main__':
    main()
    