import warnings
warnings.simplefilter('ignore')
import pandas as pd
from prophet import Prophet
import joblib


df = pd.read_csv('soru2/filled_data.csv')


df['ds'] = pd.to_datetime(df['TIME_STAMP'])


download_df = df[['ds', 'DOWNLOAD']].rename(columns={'DOWNLOAD': 'y'})

#GÜVEN ARALIĞI VE TATİL BAYRAM GÜNLERİNE GÖRE TAHMİN
download_model = Prophet(interval_width=0.95, daily_seasonality=True)
download_model.fit(download_df)


joblib.dump(download_model, 'soru2/download_model.pkl')


upload_df = df[['ds', 'UPLOAD']].rename(columns={'UPLOAD': 'y'})


upload_model = Prophet(interval_width=0.95, daily_seasonality=True)
upload_model.fit(upload_df)


joblib.dump(upload_model, 'soru2/upload_model.pkl')
