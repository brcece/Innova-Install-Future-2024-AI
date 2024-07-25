import pandas as pd
from datetime import datetime
import holidays

# Veriyi oku
df = pd.read_excel('exceldeğişiklikler\hackathon 2024 - Yapay Zeka.xlsx')

# Türkiye için tatil günlerini al
tr_holidays = holidays.Turkey()

# datetime formatına çevir
df['TIME_STAMP'] = pd.to_datetime(df['TIME_STAMP'])

# sütun ekle ve gün türünü belirle
def gun_turu(timestamp):
    date = timestamp.date()
    if date in tr_holidays:
        return 'Tatil'
    elif date.weekday() >= 5:
        return 'Hafta Sonu'
    else:
        return 'Hafta İçi'

df['Gün_Tipi'] = df['TIME_STAMP'].apply(gun_turu)

# Kaydet
df.to_excel('exceldeğişiklikler\guncellenmis_veri_seti.xlsx', index=False)

# Sonucu kontrol et
print(df.head())
print(df[df['Gün_Tipi'] == 'Tatil'])  # Tatil günlerini kontrol et
print(df[df['Gün_Tipi'] == 'Hafta Sonu'])  # Hafta sonlarını kontrol et
print(df[df['Gün_Tipi'] == 'Hafta İçi'])  # Hafta içi günlerini kontrol et
