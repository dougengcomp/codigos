import pandas as pd
from prophet import Prophet
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def forecast_usd_brl(input_file: str, output_file: str, periods: int = 90):
    """
    Forecast USD/BRL exchange rate using Prophet and plot the results interactively with Plotly.
    Args:
        input_file (str): Path to the CSV file with required columns.
        output_file (str): Path to save the forecasted data.
        periods (int): Number of days to forecast (default is 90 for 3 months).
    """
    try:
        # Step 1: Load the data
        print("Loading data...")
        df = pd.read_csv(input_file)
        print(f"Data loaded: {df.shape[0]} rows")

        # Step 2: Prepare data for Prophet
        # Rename columns to 'ds' (date) and 'y' (target price)
        if 'date' not in df.columns or 'price' not in df.columns:
            raise ValueError("Input file must contain 'date' and 'price' columns.")
        df = df.rename(columns={'date': 'ds', 'price': 'y'})
        df_prophet = df[['ds', 'y']]

        # Step 3: Initialize and fit the Prophet model
        print("Fitting the Prophet model...")
        model = Prophet()
        model.fit(df_prophet)

        # Step 4: Make a dataframe for future predictions (next 90 days)
        print("Forecasting...")
        future = model.make_future_dataframe(periods=periods)
        forecast = model.predict(future)

        # Step 5: Save the forecasted data
        forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv(output_file, index=False)
        print(f"Forecast saved to {output_file}")

        # Step 6: Plot the forecast using Plotly
        print("Plotting forecast interactively...")
        fig = make_subplots(rows=1, cols=1, subplot_titles=("USD/BRL Exchange Rate Forecast",))

        # Actual values
        fig.add_trace(go.Scatter(x=df['ds'], y=df['y'], mode='markers', name='Actual Data', marker=dict(color='black')))

        # Forecasted values (next 90 days)
        forecast_trimmed = forecast[forecast['ds'] > df['ds'].max()]
        fig.add_trace(go.Scatter(x=forecast_trimmed['ds'], y=forecast_trimmed['yhat'], mode='lines', name='Forecast', line=dict(color='blue')))

        # Upper and lower bounds
        fig.add_trace(go.Scatter(x=forecast_trimmed['ds'], y=forecast_trimmed['yhat_upper'], mode='lines', name='Upper Bound', line=dict(dash='dot', color='lightblue')))
        fig.add_trace(go.Scatter(x=forecast_trimmed['ds'], y=forecast_trimmed['yhat_lower'], mode='lines', name='Lower Bound', line=dict(dash='dot', color='lightblue')))

        # Add layout details
        fig.update_layout(
            title="USD/BRL Exchange Rate Forecast (Next 90 Days)",
            xaxis_title="Date",
            yaxis_title="Exchange Rate",
            showlegend=True,
            template="plotly",
            height=600,
            width=1000
        )

        # Show interactive plot
        fig.show()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    input_csv = "USD_BRL_Historical_Data_Enhanced.csv"
    output_csv = "USD_BRL_Historical_Data_Forecast_90days.csv"
    forecast_usd_brl(input_csv, output_csv)
