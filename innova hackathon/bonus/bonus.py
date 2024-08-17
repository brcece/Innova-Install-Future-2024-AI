import warnings
warnings.simplefilter('ignore')
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


df = pd.read_csv('soru2/filled_data.csv')


df['ds'] = pd.to_datetime(df['TIME_STAMP'])


df['hour'] = df['ds'].dt.hour


hourly_traffic = df.groupby('hour')[['DOWNLOAD', 'UPLOAD']].sum().reset_index()
# Verileri saat dilimlerine göre gruplayarak, her saat diliminde 'DOWNLOAD' ve 'UPLOAD' sütunlarının toplamını hesaplar.

hourly_traffic['TOTAL_TRAFFIC'] = hourly_traffic['DOWNLOAD'] + hourly_traffic['UPLOAD']


peak_hours = hourly_traffic.sort_values(by='TOTAL_TRAFFIC', ascending=False).head(3)  # En yoğun 3 saat dilimi
#hourly_traffic veri çerçevesindeki saat dilimlerini toplam trafik miktarına göre sıralar 
peak_hours_text = '\n'.join([f"- {row['hour']}:00 - {row['hour']+1}:00 -" for index, row in peak_hours.iterrows()])


fig = px.bar(hourly_traffic, x='hour', y='TOTAL_TRAFFIC', title='Saat Dilimlerine Göre Toplam Trafik', labels={'hour': 'Saat', 'TOTAL_TRAFFIC': 'Toplam Trafik'})


fig.add_annotation(
    xref="paper", yref="paper",
    x=0.5, y=1.1,
    showarrow=False,
    text=f"En Yoğun Saat Dilimleri:\n{peak_hours_text}",
    font=dict(size=12)
)

fig.update_layout(
    title={
        'text': "Saat Dilimlerine Göre Toplam Trafik",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'}
)



print("En Yoğun Saat Dilimleri:")
print(peak_hours)
fig.show()

# Add this line to keep the plot open if running as a script
input("Press Enter to close...")
