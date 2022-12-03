from AE33 import read_ae33
import pandas as pd 
import datetime, os, warnings;  warnings.filterwarnings('ignore')

meteokeys = ['output_mark','yymmddhhmmss','0W1Bj','lat','SN','lon','EW',
                'speed_GPS','orient_GPS','GPS_situa',
                'speed_zhenFeng','speed_source','speed_valid',
                'orient_zhenFeng','orient_source','orient_valid',
               'speed_relative','orient_relative','speed_true','orient_true',
               'speed_true_1min','orient_true_1min','speed_true_10min','orient_true_10min',
               'press','press_1min','temp','temp_1min','rh','rh_1min']
def read_meteo(markHour:bool):
    file_dir = './meteoinfo/'
    files = os.listdir(file_dir)
    df1 = pd.read_table(os.path.join(file_dir, files[0]),sep=',',header=None,usecols=range(0,30))
    
    for file in files[1:]:# continue to read other files
        df2 = pd.read_table(os.path.join(file_dir, file),sep=',',header=None,usecols=range(0,30))
        df1 = pd.concat((df1, df2), axis=0, join='inner')
    df=df1
    del df2,df1
    df.columns=meteokeys    
    # remove lat&lon abnormal
    df = df[df['lon']!='XXXXX.XXXX']
    df = df[df['lat']!='XXXX.XXXX']
    # reset lat&lon 
    df['lon'] = df['lon'].astype('float')//100+df['lon'].astype('float')/100%1*100/60
    df['lat'] = df['lat'].astype('float')//100+df['lat'].astype('float')/100%1*100/60
    # reset index，remove origin index
    df = df.reset_index(drop=True)
    # reset timestamp
    df['yymmddhhmmss']=pd.to_datetime(df['yymmddhhmmss'],format='%y%m%d%H%M%S')
    # optional：use data on the hour
    if markHour == True:
        df = df[df['yymmddhhmmss'].apply(lambda x:x.minute==0 and x.second==0)]
    # true wind speed/direction per 1 min 
    df['speed_true_1min'] = df['speed_true_1min'].astype('float')
    df['orient_true_1min'] = df['orient_true_1min'].astype('float')
    # RH/temperature per 1 min
    df['temp_1min'] = df['temp_1min'].astype('float')
    df['rh_1min'] = df['rh_1min'].astype('float')
    # Relative wind speed/direction
    df['speed_relative'] = df['speed_relative'].astype('float')
    df['orient_relative'] = df['orient_relative'].astype('float')
    # GPS speed/direction
    df['speed_GPS'] = df['speed_GPS'].astype('float')
    df['orient_GPS'] = df['orient_GPS'].astype('float')
    # optional：change this column's name to fit AE33 data
    df.rename(columns={'yymmddhhmmss': 'Dateandtime'}, inplace=True)
    df = df.reset_index(drop=True)
    return df

def main():
    meteoinfo = read_meteo()
    ae33info  = read_ae33()
    df_combine = pd.merge(meteoinfo,ae33info,on='Dateandtime')
    del meteoinfo,ae33info
    df_combine


if __name__ == '__main__':
    main()