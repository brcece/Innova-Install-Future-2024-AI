import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import numpy as np
from datetime import datetime
import holidays
import plotly.express as px
import plotly.graph_objects as go


file_path = 'exceldeğişiklikler/hackathon 2024 - Yapay Zeka.xlsx'
data = pd.read_excel(file_path)


data['TIME_STAMP'] = pd.to_datetime(data['TIME_STAMP'])
data.set_index('TIME_STAMP', inplace=True)


print("Eksik değerler (indeksler):")
print(data[data.isnull().any(axis=1)])
#series.isna(): Series'deki eksik (NaN) değerleri belirler.İNDEX ALIYORUZ


def fill_missing_values(series):
    
    missing_indices = series[series.isna()].index
    if not missing_indices.empty:
        
        model = ARIMA(series.dropna(), order=(5, 1, 0))
        model_fit = model.fit()
        
        
        for idx in missing_indices:
            start = max(0, series.index.get_loc(idx) - 1)  
            end = start + 2  
            forecast = model_fit.predict(start=start, end=end)
            series[idx] = forecast.iloc[-1]
    return series
#ARIMA(series.dropna(), order=(5, 1, 0)): ARIMA modelini oluşturur.
#5: AR (AutoRegressive) teriminin p değeri.modelin geçmiş gözlemlerine ne kadar dayalı olduğu
#1: I (Integrated) teriminin d değeri.ne kadar farklılaştırılacağı
#0: MA (Moving Average) teriminin q değeri.hata terimlerine ne kadar dayalı olduğu
#model.fit(): Modeli verilen eksiksiz veri üzerinde eğitir.

data['DOWNLOAD'] = fill_missing_values(data['DOWNLOAD'])


data['UPLOAD'] = fill_missing_values(data['UPLOAD'])


print("Doldurulmuş veri:")
print(data)


data.to_csv('filled_data.csv')


tr_holidays = holidays.Turkey()


def gun_turu(timestamp):
    date = timestamp.date()
    if date in tr_holidays:
        return 'Tatil'
    elif date.weekday() >= 5:
        return 'Hafta Sonu'
    else:
        return 'Hafta İçi'

data['Gün_Tipi'] = data.index.to_series().apply(gun_turu)


hafta_ici = data[data['Gün_Tipi'] == 'Hafta İçi']
hafta_sonu = data[data['Gün_Tipi'] == 'Hafta Sonu']
tatil = data[data['Gün_Tipi'] == 'Tatil']


data.reset_index().to_excel('exceldeğişiklikler/guncellenmis_veri_seti.xlsx', index=False)


hafta_ici.reset_index().to_excel('exceldeğişiklikler/hafta_ici.xlsx', index=False)
hafta_sonu.reset_index().to_excel('exceldeğişiklikler/hafta_sonu.xlsx', index=False)
tatil.reset_index().to_excel('exceldeğişiklikler/tatil.xlsx', index=False)


print(data.head())
print(data[data['Gün_Tipi'] == 'Tatil'])  
print(data[data['Gün_Tipi'] == 'Hafta Sonu'])  
print(data[data['Gün_Tipi'] == 'Hafta İçi'])  


