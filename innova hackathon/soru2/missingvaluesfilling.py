import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import numpy as np

# Veriyi yükleyin
file_path = 'hackathon 2024 - Yapay Zeka.csv'  # CSV dosya yolunuzu buraya girin
data = pd.read_csv(file_path)

# Zaman damgasını datetime formatına çevirin ve indeks olarak kullanın
data['TIME_STAMP'] = pd.to_datetime(data['TIME_STAMP'])
data.set_index('TIME_STAMP', inplace=True)

# Eksik değerleri tespit et
print("Eksik değerler (indeksler):")
print(data[data.isnull().any(axis=1)])

# Eksik değerleri doldurmak için yardımcı fonksiyon
def fill_missing_values(series):
    # Eksik değerlerin indekslerini alın
    missing_indices = series[series.isna()].index
    if not missing_indices.empty:
        # ARIMA modelini oluştur ve eğit
        model = ARIMA(series.dropna(), order=(5, 1, 0))
        model_fit = model.fit()
        
        # Eksik değerleri tahmin et ve doldur
        for idx in missing_indices:
            start = max(0, series.index.get_loc(idx) - 1)  # Bir önceki indeks
            end = start + 2  # Bir sonraki iki indeks
            forecast = model_fit.predict(start=start, end=end)
            series[idx] = forecast.iloc[-1]
    return series

# DOWNLOAD serisi için eksik değerleri doldurun
data['DOWNLOAD'] = fill_missing_values(data['DOWNLOAD'])

# UPLOAD serisi için eksik değerleri doldurun
data['UPLOAD'] = fill_missing_values(data['UPLOAD'])

# Eksik değerlerin doldurulduğunu kontrol edin
print("Doldurulmuş veri:")
print(data)

# Doldurulan veri setini kaydetmek için
data.to_csv('filled_data.csv')
