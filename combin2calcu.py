import pandas as pd 
import datetime, os, warnings;  warnings.filterwarnings('ignore')
from meteo import read_meteo
from AE33 import read_ae33,create_plot,wavelengths,units

def nv2plot():
    '''
    new variable to plot
    '''
    
    return 
def main():
    meteoinfo = read_meteo()
    ae33info  = read_ae33()
    df = pd.merge(meteoinfo,ae33info,on='Dateandtime')
    del meteoinfo,ae33info

    lamda:int=880   # Select the wavelength to read
    BCkey = str(wavelengths.get(lamda))
    unit = units.get(BCkey) 
    create_plot(x=df['Dateandtime'], y=df[BCkey], yunits=unit, ytitle="Equivalent Black Carbon 880nm", y1=df['orient_relative'])

if __name__ == '__main__':
    main()