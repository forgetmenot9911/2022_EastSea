from turtle import update


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
    ax.add_feature(cf.LAND, linewidth=0.2, facecolor='#EFEFDB', edgecolor='black')
    ax.add_feature(cf.OCEAN, facecolor='#97DBF2')
    ax.add_feature(shp, linewidth=0.15, edgecolor='gray', facecolor='none')
    # ax.outline_patch.set_visible(False)#关闭GeoAxes框线
    # for i in ['left','bottom','right', 'top']:
    #     ax.spines[i].set_visible(True)#开启Axes框线
    #     ax.spines[i].set_color('black')
    #     ax.spines[i].set_linewidth(1)
    lb=ax.gridlines(draw_labels=True,x_inline=False, y_inline=False,xlocs=np.linspace(116,126,6), ylocs=range(26,38,2),
                    linewidth=0.2, color='black', alpha=0.8, linestyle='--',zorder=4)
    lb.top_labels = None
    lb.right_labels = None
    lb.rotate_labels = False

def plot_spots():
    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs 
    proj=ccrs.PlateCarree()
    plt.rcParams['axes.unicode_minus'] = False 
    plt.rcParams['font.sans-serif'] = ['Times New Roman']
    fig = plt.figure(figsize=(8, 8))
    ax = plt.axes(projection=proj)
    set_geo(ax)
    
    #提取数据
    # plt.scatter(spots.lon,spots.lat,s=0.2,c='black')
    plt.savefig('spots_20220528.png',dpi=600,bbox_inches='tight',pad_inches=0)

def plot_route(df,BCkey):
    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs 
    import datetime
    import pandas as pd 
    # plt.rcParams['axes.unicode_minus'] = False 
    plt.rcParams['font.sans-serif'] = ['Times New Roman']
    plt.rcParams['font.size']=9
    proj=ccrs.PlateCarree()
    fig = plt.figure(figsize=(4, 4))
    ax = plt.axes(projection=proj)
    set_geo(ax)
    scatter=ax.scatter(df.lon,df.lat,c=df[BCkey],s=2.5,cmap=plt.cm.jet,alpha=0.7,zorder=3)
    legend1 = ax.legend(*scatter.legend_elements(num=6),
                    loc='lower left', bbox_to_anchor=(1.005,0.005), frameon=False,
                    ncol=1, markerscale=0.5,
                    title="BC/(μg/m$^3$)")
    ax.add_artist(legend1)
    lon=df.lon
    lat=df.lat
    
    # ax.contourf()
    spots=pd.read_csv('./spots_corrected_1.csv',sep=' ',header=None)
    ## 在总的outliers中，选择若干点
    scatter2=ax.scatter(spots[0],spots[1],
                        facecolor='none',edgecolor='k', alpha=0.5)
    for i, lon  in enumerate(spots[0]):
        ax.text(spots[0][i]+0.25,
                spots[1][i]-0.25,'No.{}'.format(i+1))
    ## 可选：导出选择后的outliers
    # pd.concat([df.lon[added.index[[0,1,3,8,10,12,13]]], df.lat[added.index[[0,1,3,8,10,12,13]]]], axis=1).to_csv('outliers_selected.csv',index=False)
    # ax.text(0.95,0.95,'b)', 
    #     horizontalalignment='center',verticalalignment='center',transform=ax.transAxes)
        ### 可选：绘制同季节陆上近海站点BC分布图
    spotsOnland = ['Qingdao', 'Nanjing', 'Shanghai', 'Ningbo', 'Xiamen']
    spotslon = [120.68, 118.715, 121.59, 121.91, 118.05]
    spotslat = [36.35, 32.205, 31.18, 29.87, 24.6]
    # scatter3 = ax.scatter(spotslon,spotslat, s=5, marker='s',facecolors='orange',edgecolors='k')
    # for i, x in enumerate(spotsOnland):
    #     ax.text(spotslon[i]-1 ,spotslat[i]+0.25, x)
        ### 添加：海洋标记
    seaname = ['Yellow Sea', 'East China \n   Sea']
    sealon = [121.90, 123.0]
    sealat = [35.00, 26.]
    for i , x in enumerate(seaname):
        ax.text(sealon[i],sealat[i],seaname[i], style='italic', color='blue', fontsize=13, alpha=0.5)
        ### 可选：添加子图
    # img1=plt.imread(r'./pic/20221019_spotsOnland.png')#图片地址
    # ax_insert =fig.add_axes([0.2,0.18,0.2,0.37])#添加存放图片的子图
    # ax_insert.imshow(img1)#显示图片
    # ax_insert.axis('off')#去除框线

    today = datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d')
    plt.savefig('./pic/{}_bcRoute'.format(today),dpi=600,bbox_inches='tight', pad_inches=0)
    plt.close()
    

def plot_dere(df,**kw):
    '''
    航线示意图
    '''
    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs 
    import datetime
    from merra2 import plot_merra2
    # plt.rcParams['axes.unicode_minus'] = False 
    plt.rcParams['font.sans-serif'] = ['Times New Roman']
    plt.rcParams['font.size']=9
    proj=ccrs.PlateCarree()
    fig = plt.figure(figsize=(4, 4))
    ax = plt.axes(projection=proj)
    set_geo(ax)
    # 航线示意图 (with BC conc. and wind)
    # plot_merra2(fig, ax, proj, 'BCSMASS')# Black Carbon Surface Mass Concentration (μg m-3)
    # ax.plot(df.lon[:150],df.lat[:150],linewidth=0.5,color='black',zorder=2,label='Departing 1')
    # ax.plot(df.lon[150:204],df.lat[150:204],linewidth=0.25,color='tab:red',zorder=4,label='Departing 2')
    # ax.plot(df.lon[204:250],df.lat[204:250],linewidth=0.75,color='yellow',zorder=3,label='Departing 3')
    # ax.plot(df.lon[250:],df.lat[250:],'--',linewidth=0.5,ms=1,color='black',zorder=2,label='Returning')
    # ax.legend(loc='lower left', bbox_to_anchor=(1.005,0.005), frameon=False)
    # name = 'BC_Conc'

    # BC与离岸距离-散点图
    # ax.scatter(df.lon[30:38],df.lat[30:38], s=1, c='blue')
    # ax.scatter(df.lon[55:75],df.lat[55:75], s=1,c='orange')# 30 deg    
    # ax.scatter(df.lon[113:130],df.lat[113:130], s=1,c='green')
    # ax.scatter(df.lon[170:182],df.lat[170:182], s=1,c='red')
    
    #BB占比（%）-散点图
    sc = ax.scatter(df.lon, df.lat, c=df['BB(%)'], s=1, cmap='rainbow')
    legend1 = ax.legend(*sc.legend_elements(num=6),
                    loc="lower left",
                    # frameon=False,
                    ncol=1, markerscale=0.4,
                    title="BB contribution(%)")
    ax.add_artist(legend1)
    name = kw['name']
    
    today = datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d')
    plt.savefig('./pic/{}_cruiseRoute_{}.png'.format(today,name),dpi=800,bbox_inches='tight', pad_inches=0)
    plt.close()


def create_ani(x, y):
    '''
    制作动画【未完成】
    '''
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    fig, ax = plt.subplots()
    scatter = ax.scatter([], [], s=2)
    # plt.show()
    # line, = ax.scatter([], [], lw=1)
    ani = animation.FuncAnimation(fig, scatter.set_data(x,y),frames=200)
    ani.save('route.mp4')