import warnings
warnings.simplefilter('ignore')
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import joblib
import plotly.express as px


df = pd.read_csv('soru2/filled_data.csv')


df['ds'] = pd.to_datetime(df['TIME_STAMP'])


download_model = joblib.load('download_model.pkl')
upload_model = joblib.load('upload_model.pkl')


future_download = download_model.make_future_dataframe(periods=100, freq='T')
forecast_download = download_model.predict(future_download)
#gelecekteki tarih ve saat bilgilerini içeren bir veri çerçevesi oluşturur. 
# periods argümanı tahmin edilecek zaman dilimi sayısını, freq ise bu zaman 
# dilimlerinin frekansını belirtir 

future_upload = upload_model.make_future_dataframe(periods=200, freq='T')
forecast_upload = upload_model.predict(future_upload)


download_df = df[['ds', 'DOWNLOAD', 'SERVER_NAME']]
upload_df = df[['ds', 'UPLOAD', 'SERVER_NAME']]


download_merged = pd.merge(download_df, forecast_download[['ds', 'yhat', 'yhat_lower', 'yhat_upper']], on='ds')
upload_merged = pd.merge(upload_df, forecast_upload[['ds', 'yhat', 'yhat_lower', 'yhat_upper']], on='ds')


download_merged['anomaly'] = (download_merged['DOWNLOAD'] < download_merged['yhat_lower']/1.1) | (download_merged['DOWNLOAD'] > download_merged['yhat_upper']*1.1)
upload_merged['anomaly'] = (upload_merged['UPLOAD']< upload_merged['yhat_lower']/1.1) | (upload_merged['UPLOAD'] > upload_merged['yhat_upper']*1.1)


fig = make_subplots(rows=2, cols=1, subplot_titles=("Download Forecast", "Upload Forecast"))


fig.add_trace(go.Scatter(
    x=forecast_download['ds'], y=forecast_download['yhat'], mode='lines', name='Download Forecast', line=dict(color='black', width=1.5)
), row=1, col=1)
fig.add_trace(go.Scatter(
    x=download_merged['ds'], y=download_merged['DOWNLOAD'], mode='lines', name='Actual Download', line=dict(color='deeppink', width=1)
), row=1, col=1)
fig.add_trace(go.Scatter(
    x=download_merged[download_merged['anomaly']]['ds'], y=download_merged[download_merged['anomaly']]['DOWNLOAD'], mode='markers', 
    name='Anomaly Download', marker=dict(color='red', symbol='x'),
    hovertemplate='<b>Time:</b> %{x}<br><b>Server Name:</b> %{customdata[0]}<br><b>Download:</b> %{customdata[1]}',
    customdata=download_merged[['SERVER_NAME', 'DOWNLOAD']]
), row=1, col=1)


fig.add_trace(go.Scatter(
    x=forecast_upload['ds'], y=forecast_upload['yhat'], mode='lines', name='Upload Forecast', line=dict(color='black', width=1.5)
), row=2, col=1)
fig.add_trace(go.Scatter(
    x=upload_merged['ds'], y=upload_merged['UPLOAD'], mode='lines', name='Actual Upload', line=dict(color='deeppink', width=1)
), row=2, col=1)
fig.add_trace(go.Scatter(
    x=upload_merged[upload_merged['anomaly']]['ds'], y=upload_merged[upload_merged['anomaly']]['UPLOAD'], mode='markers', 
    name='Anomaly Upload', marker=dict(color='red', symbol='x'),
    hovertemplate='<b>Time:</b> %{x}<br><b>Server Name:</b> %{customdata[0]}<br><b>Upload:</b> %{customdata[1]}',
    customdata=upload_merged[['SERVER_NAME', 'UPLOAD']]
), row=2, col=1)


fig.update_layout(title_text="Download and Upload Forecasts with Anomalies", height=800)

fig.show()

# Add this line to keep the plot open if running as a script
input("Press Enter to close...")