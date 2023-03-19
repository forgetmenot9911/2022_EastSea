import pandas as pd
import proplot as pplt 
import numpy as np 
import datetime
from sklearn.linear_model import LinearRegression
from scipy.stats import pearsonr
def scatterLinear(ax, model, x, y, color, label):
    '''
    散点图+线性回归
    '''
    ax.scatter(x, y,s=1,c=color)
    x_2d=np.array(x).reshape(-1, 1)
    model.fit(x_2d, y)
    ax.plot(x, model.predict(x_2d),color=color, label=label)
    x=np.array(x).tolist()
    (r, p)=pearsonr(x, y)
    text = label+'\n'+'$R$ = {:.4f}{}$p$ = {:.3f}'.format(r, '\n', p)
    if color=='blue':
        ax.text(0.7,0.8, text, weight="bold", transform=ax.transAxes, color=color)
    else:
        ax.text(0.7,0.1, text, weight="bold", transform=ax.transAxes, color=color)
def set_geo(ax):
    import cartopy.feature as cf
    import cartopy.crs as ccrs
    from cartopy.io.shapereader import Reader
    import numpy as np
    shp_dir='E:/official_shapefiles/'
    shp_name='province.shp'
    proj=ccrs.PlateCarree()
    shp = cf.ShapelyFeature(Reader(shp_dir+shp_name).geometries(), ccrs.PlateCarree())
    extent=[115, 127, 24, 38]
    ax.set_extent(extent, crs=proj) 
    ax.add_feature(cf.LAND)
    ax.add_feature(cf.OCEAN, facecolor='#97DBF2')
    ax.add_feature(shp,  linewidth=0.15, edgecolor='gray', facecolor='none',zorder=4)
    ax.outline_patch.set_visible(False)#关闭GeoAxes框线
    for i in ['left','bottom','right', 'top']:
        ax.spines[i].set_visible(True)#开启Axes框线
        ax.spines[i].set_color('black')
        ax.spines[i].set_linewidth(1)
    lb=ax.gridlines(draw_labels=True,x_inline=False, y_inline=False,xlocs=np.linspace(116,126,6), ylocs=range(26,38,2),
                    linewidth=0.2, color='black', alpha=0.8, linestyle='--',zorder=4)
    lb.top_labels = None
    lb.right_labels = None
    lb.rotate_labels = False
def main():
    df = pd.read_csv('./BCvsMeteo.csv',header=0)
    # print(df)
    facts = ['press_1min' , 'temp_1min' , 'rh_1min' , 'speed_true_1min']
    labels = ['Pressure [hPa]' , 'Air temperature [deg]' , 'RH [%]', 'Wind speed [m/s]']
    
    ## 提取YS
    ys  = df[ (df['lat']<=37) & (df['lat']>=33) & (df['lon']>=120) & (df['lon']<=126.25)]
    ## 提取ECS
    ecs = df[ (df['lat']<=32) & (df['lat']>=25) & (df['lon']>=120) & (df['lon']<=126.875) ]
    ## 建立线性回归模型
    model = LinearRegression()


    pplt.rc['font.family'] = 'Times New Roman' 
    fig = pplt.figure(wspace=3.5, refwidth='20em', sharey=False)
    axs = fig.subplots(nrows=2, ncols=2)
    for ax,fact,label in zip(axs,facts,labels):

        # ax.scatter(df.BC6, df[fact],s=1,c='k')
        scatterLinear(ax, model, ys['BC6'].tolist(), ys[fact].tolist(), color='red', label='YS')
        scatterLinear(ax, model, ecs['BC6'].tolist(), ecs[fact].tolist(), color='blue', label='ECS')

        ax.set_ylim([df[fact].min(), df[fact].max()])
        ax.set_ylabel(label)
    axs.format(abc='a)', abcloc='ul',facecolor=None,xlabel='BC [$\mu g/m^{3}$]')
    today = datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d')
    fig.save('./pic/{}_BCvsMeteo.png'.format(today), dpi=600)

def main1():
    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs 
    import datetime
    plt.rcParams['axes.unicode_minus'] = False 
    plt.rcParams['font.sans-serif'] = ['Times New Roman']
    plt.rcParams['font.size']=5
    proj=ccrs.PlateCarree()
    fig = plt.figure(figsize=(4, 4))
    ax = plt.axes(projection=proj)
    set_geo(ax)
    plot_squ(ax, target=[33,45, 120,126])
    plot_squ(ax, target=[25,33, 120,131])
    today = datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d')
    plt.savefig('./pic/{}_YSandECS.png'.format(today),dpi=600,bbox_inches='tight', pad_inches=0)
    plt.close()
if __name__ == '__main__':
    main()