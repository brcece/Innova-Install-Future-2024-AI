import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import plotly.express as px


file_path = 'exceldeğişiklikler/tatil1.xlsx'  
df = pd.read_excel(file_path, sheet_name='Sheet1')


print("Data read from Excel:")
print(df)


df['TIME_STAMP'] = pd.to_datetime(df['TIME_STAMP'])
df.set_index('TIME_STAMP', inplace=True)


print("\nData types after conversion:")
print(df.dtypes)


df_numeric = df.drop(columns=['SERVER_NAME', 'Gün_Tipi'])


scaler = StandardScaler()
df_scaled = scaler.fit_transform(df_numeric)


iso_forest = IsolationForest(n_estimators=100, max_samples='auto', contamination=0.4, max_features=1.0, bootstrap=False, n_jobs=None, random_state=None, verbose=0, warm_start=False)
iso_forest.fit(df_scaled)


anomaly_scores = iso_forest.decision_function(df_scaled)


df['Anomaly_Score'] = anomaly_scores


df['Anomaly'] = iso_forest.predict(df_scaled)
df['Anomaly'] = df['Anomaly'].apply(lambda x: 'Anomaly' if x == -1 else 'Normal')

print("\nResults with anomaly scores and labels:")
print(df[['SERVER_NAME', 'DOWNLOAD', 'UPLOAD', 'Gün_Tipi', 'Anomaly_Score', 'Anomaly']])

# Plot the results
fig = px.scatter(df, x=df.index, y='DOWNLOAD', color='Anomaly',
                 title='Anomaly Detection in holiday data',
                 labels={'TIME_STAMP': 'Time', 'DOWNLOAD': 'Download (kB)'},
                 color_discrete_map={'Anomaly': 'green', 'Normal': 'blue'})

fig.update_traces(marker=dict(size=6))
fig.show()

# Add this line to keep the plot open if running as a script
input("Press Enter to close...")