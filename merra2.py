import numpy as np    
from netCDF4 import Dataset

units={
    'BCSMASS':'$\mu g\cdot m^{-3}$',
    'SO2SMASS':'$\mu g\cdot m^{-3}$',
    'SO2CMASS':'$\mu g\cdot m^{-2}$',
    'DUSMASS25':'$\mu g\cdot m^{-3}$',
    'DUSMASS':'$\mu g\cdot m^{-3}$',
    'BCEXTTAU':' ',
    'BCSCATAU':' ',
    'ColumnAmountNO2':'molec/cm$^2$',
    'ColumnAmountNO2Trop':'$molec/cm^2$'
}
def readNC(varname):
    data = Dataset("E:\MERRA2-AAE\MERRA2_400.tavgM_2d_aer_Nx.202204.nc4", mode='r')
    lons = data.variables['lon'][:]
    lats = data.variables['lat'][:]
    lon, lat = np.meshgrid(lons, lats)
    fv= unit = data.variables[varname]._FillValue
    if varname in ['BCSMASS', 'SO2SMASS','SO2CMASS','DUSMASS25','DUSMASS']:
        var = data.variables[varname][0,:,:]*1e9 # 取第一层，并转换单位：（kg m-3）->（μg m-3）,（kg m-2）->（μg m-2）
        var[var==fv] = np.nan
    else:
        var = data.variables[varname][0,:,:]
    unit = data.variables[varname].units 
    return (lon,lat,var,unit)
def readOMI(varname):
    data = Dataset('./OMI_NO2/OMI-Aura_L3-OMNO2d_2022m0409_v003-2022m0812t170851.he5.nc4', mode='r')
    lons = data.variables['lon'][:]
    lats = data.variables['lat'][:]
    lon, lat = np.meshgrid(lons, lats)
    var = data.variables[varname][:,:]
    return (lon,lat,var)
def set_geo(ax):
    import cartopy.feature as cf
    from cartopy.io.shapereader import Reader
    import cartopy.crs as ccrs 
    shp_dir='E:/official_shapefiles/'
    shp_name='province.shp'
    proj=ccrs.PlateCarree()
    shp = cf.ShapelyFeature(Reader(shp_dir+shp_name).geometries(), ccrs.PlateCarree())
    extent=[115, 127, 24, 38]
    ax.set_extent(extent, crs=proj) 
    ax.add_feature(cf.LAND, linewidth=0.2, edgecolor='black', facecolor='none',zorder=4)
    # ax.add_feature(cf.OCEAN, facecolor='#97DBF2')
    # ax.add_feature(shp,  linewidth=0.15, edgecolor='gray', facecolor='none',zorder=4)
    
    ax.outline_patch.set_visible(False)#关闭GeoAxes框线
    for i in ['top','bottom','right', 'left']:
        ax.spines[i].set_visible(True)#开启Axes框线
        ax.spines[i].set_color('black')
        ax.spines[i].set_linewidth(1)
    lb=ax.gridlines(draw_labels=True,x_inline=False, y_inline=False,xlocs=np.linspace(116,126,6), ylocs=range(26,38,2),
                    linewidth=0.2, color='black', alpha=0.8, linestyle='--',zorder=4)
    lb.top_labels = None
    lb.right_labels = None
    lb.rotate_labels = False


def plot_merra2(fig, ax, proj, varname):
    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs 
    import datetime, cmaps
    (lon,lat,var,unit) = readNC(varname)
    # levels = np.arange(1,6,5e-2)
    levels = np.arange(0,6,6e-2)
    cm = ax.contourf(lon, lat, var,
                      levels, 
                      linewidths=0.5, transform=proj, cmap='rainbow', zorder=1)
    # ax.clabel(cm, fontsize=9, inline=True)
    cax1=fig.add_axes([0.89,0.35,0.03,0.4])
    cb = fig.colorbar(cm, 
                    #   orientation="vertical", 
                    #   pad=0.0005,  shrink=0.4, 
                      extend=None, cax=cax1)
    ## cb.set_label(unit,rotation=270,labelpad=10)
    ax2=cb.ax # 调出colorbar的ax属性
    ax2.tick_params(direction='in')
    # ax2.set_title('$\mu g /m^{3}$')
    (lon,lat,u,unit) = readNC('BCFLUXU')
    (lon,lat,v,unit) = readNC('BCFLUXV')
    flux = np.sqrt(u**2 + v**2)
    # lw = flux / flux.max()
    strm = ax.streamplot(lon,lat,u,v, 
                        #  color=lw, 
                        color=flux*1e3*1e2,#kg m-1 s-1 -> g m-1 s-1 -> 10^-2 g m-1 s-1
                         arrowsize=0.6, cmap='binary', linewidth=0.1, zorder=1)
    cax2=fig.add_axes([0.99,0.35,0.03,0.4])
    cb_strm = fig.colorbar(strm.lines, 
                        #    ticks=np.linspace(0,0.6,7),
                        #    shrink=0.4, pad=0.04, 
                           format='%.2g', extend=None, cax=cax2)
    ax_strm=cb_strm.ax # 调出colorbar的ax属性
    ax_strm.tick_params(direction='in')
    # ax_strm.set_title('$\  g/(m\;s)$')

def plot_omi(varname, titlename, unit):
    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs 
    import numpy as np
    import datetime
    plt.rcParams['axes.unicode_minus'] = False 
    plt.rcParams['font.sans-serif'] = ['Times New Roman']
    plt.rcParams['font.size']=5
    proj=ccrs.PlateCarree()
    fig = plt.figure(figsize=(4, 4))
    ax = plt.axes(projection=proj)
    ax.set_global()
    set_geo(ax)
    (lon,lat,var) = readOMI(varname)
    plt.pcolormesh(lon, lat, var, 
                # levels=np.linspace(0,1.5*1e16,5),
                vmin=0,
                transform=proj, cmap=plt.cm.cool, zorder=3)
    plt.title(titlename)
    cb = plt.colorbar(ax=ax, orientation="vertical", pad=0.01, aspect=16, shrink=0.8)
    cb.set_label(unit,rotation=270,labelpad=15)
    cb.ax.tick_params(direction='in')
    today = datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d')
    plt.savefig('./OMI_NO2/pic/{}_{}.png'.format(today, varname),dpi=600,bbox_inches='tight', pad_inches=0.05)
    plt.close()
def main():
    
    plot_merra2(varname='BCCMASS', titlename='BC Column Mass Density, Apr 2022')
    
    # plot_merra2(varname='SO2SMASS',unit=units['SO2SMASS'],titlename='SO$_{2}$ Surface Mass Concentration, April 2022')

    # plot_merra2(varname='SO2CMASS',unit=units['SO2CMASS'],titlename='SO$_{2}$ Columne Mass Density, April 2022')

    # plot_merra2(varname='BCEXTTAU', titlename='BC Extinction AOT [550 nm], Apr 2022')

    # plot_omi(varname='ColumnAmountNO2', unit=units['ColumnAmountNO2'], titlename='NO2 vertical column density')

    # plot_omi(varname='ColumnAmountNO2Trop', unit=units['ColumnAmountNO2Trop'], titlename='NO2 tropospheric column density')

if __name__ == '__main__':
    main()