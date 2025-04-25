import pandas as pd
from prophet import Prophet
from prophet.plot import plot_plotly
import plotly.io as pio

# Load the dataset
file_path = 'Enriched_Solana_Dataset_for_Prophet.csv'
enriched_data = pd.read_csv(file_path)

# Ensure the "Date" column is in datetime format
enriched_data['Date'] = pd.to_datetime(enriched_data['Date'], errors='coerce')

# Prepare data for Prophet
prophet_data = enriched_data.rename(columns={'Date': 'ds', 'Price': 'y'})[['ds', 'y']]

# Initialize and fit the Prophet model
model = Prophet()
model.fit(prophet_data)

# Create a dataframe for future dates (next 3 months)
future = model.make_future_dataframe(periods=90)  # 90 days = 3 months

# Predict future prices
forecast = model.predict(future)

# Create an interactive plot with a light theme
fig = plot_plotly(model, forecast)
fig.update_layout(
    title="Solana Price Prediction for the Next 3 Months",
    xaxis_title="Date",
    yaxis_title="Price",
    template="plotly_white",  # Use a light theme
    title_font=dict(size=20, color="black"),
    font=dict(color="black"),
)

# Render the interactive plot
pio.show(fig)
