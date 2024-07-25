import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import plotly.graph_objects as go

# Read data from Excel file
file_path = 'exceldeğişiklikler/hafta_ici1.xlsx'  # Path to your Excel file
df = pd.read_excel(file_path, sheet_name='Sheet1')

# Convert TIME_STAMP to datetime and set as index
df['TIME_STAMP'] = pd.to_datetime(df['TIME_STAMP'])
df.set_index('TIME_STAMP', inplace=True)

# Drop non-numeric columns
df_numeric = df.drop(columns=['SERVER_NAME', 'Gün_Tipi'])

# Standardize the data
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df_numeric)

# Initialize Isolation Forest
iso_forest = IsolationForest(n_estimators=100, max_samples='auto', contamination='auto', max_features=1.0, bootstrap=False, n_jobs=None, random_state=None, verbose=0, warm_start=False)
iso_forest.fit(df_scaled)

# Predict anomaly scores
anomaly_scores = iso_forest.decision_function(df_scaled)

# Convert to DataFrame for easier handling
df['Anomaly_Score'] = anomaly_scores

# Mark anomalies (1 for anomaly, -1 for normal)
df['Anomaly'] = iso_forest.predict(df_scaled)
df['Anomaly'] = df['Anomaly'].apply(lambda x: 'Anomaly' if x == -1 else 'Normal')

# Create the plot
fig = px.scatter(df, x=df.index, y='DOWNLOAD', color='Anomaly',
                 hover_data={'SERVER_NAME': True, 'DOWNLOAD': True, 'UPLOAD': True, 'Gün_Tipi': True, 'Anomaly_Score': True, 'Anomaly': True},
                 title='Data with Anomalies Highlighted')

# Highlight anomalies with a different marker
anomalies = df[df['Anomaly'] == 'Anomaly']
fig.add_trace(go.Scatter(x=anomalies.index, y=anomalies['DOWNLOAD'],
                         mode='markers', name='Anomaly',
                         marker=dict(color='red', size=10, symbol='x'),
                         hoverinfo='text',
                         hovertext=anomalies.apply(lambda row: f"SERVER_NAME: {row['SERVER_NAME']}<br>DOWNLOAD: {row['DOWNLOAD']}<br>UPLOAD: {row['UPLOAD']}<br>Gün_Tipi: {row['Gün_Tipi']}<br>Anomaly_Score: {row['Anomaly_Score']}", axis=1)))

fig.update_layout(
    xaxis_title='Time Stamp',
    yaxis_title='Download',
    showlegend=True
)

fig.show()
