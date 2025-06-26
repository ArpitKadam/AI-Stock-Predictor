from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import numpy as np
import yfinance as yf
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import plotly.graph_objs as go
from datetime import datetime, timedelta
import json
import plotly.utils 

app = Flask(__name__)
model = load_model("model.h5")

def plot_to_json(fig):
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        stock = request.form.get("stock")
        no_of_days = int(request.form.get("no_of_days"))
        
        # Validate days range
        if no_of_days < 1 or no_of_days > 60:
            return render_template("index.html", error="Please enter between 1-60 days for prediction.")
        
        return redirect(url_for("predict", stock=stock, no_of_days=no_of_days))
    return render_template("index.html")

@app.route("/predict")
def predict():
    stock = request.args.get("stock", "BTC-USD")
    no_of_days = int(request.args.get("no_of_days", 10))
    
    # Validate days range
    if no_of_days < 1 or no_of_days > 60:
        return render_template("result.html", error="Invalid prediction range. Please enter between 1-60 days.")

    try:
        # Fetch stock data
        end = datetime.now()
        start = datetime(end.year - 10, end.month, end.day)
        stock_data = yf.download(stock, start=start, end=end)

        if stock_data.empty:
            return render_template("result.html", error="Invalid stock ticker or no data available.")

        # Extract logo and info
        try:
            info = yf.Ticker(stock).info
            logo_url = info.get("logo_url", "")
            long_name = info.get("longName", stock)
        except:
            logo_url = ""
            long_name = stock

        # Stats summary - use .item() to extract scalar values properly
        stats = {
            "Highest": stock_data['Close'].max().item(),
            "Lowest": stock_data['Close'].min().item(),
            "Mean": stock_data['Close'].mean().item(),
            "Latest": stock_data['Close'].iloc[-1].item()
        }

        # Round the stats
        for key in stats:
            stats[key] = round(stats[key], 2)

        # Preprocessing
        split_len = int(len(stock_data) * 0.9)
        x_test = stock_data[['Close']][split_len:]
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(x_test)

        x_data, y_data = [], []
        for i in range(100, len(scaled_data)):
            x_data.append(scaled_data[i - 100:i])
            y_data.append(scaled_data[i])

        if len(x_data) == 0:
            return render_template("result.html", error="Insufficient data for prediction. Need at least 100 data points.")

        x_data, y_data = np.array(x_data), np.array(y_data)

        # Predictions on test data
        predictions = model.predict(x_data, verbose=0)
        inv_predictions = scaler.inverse_transform(predictions)
        inv_y = scaler.inverse_transform(y_data)

        # DataFrame for plotting model accuracy
        plotting_df = pd.DataFrame({
            "Original": inv_y.flatten(),
            "Predicted": inv_predictions.flatten()
        }, index=x_test.index[100:])

        # Interactive plot 1 - Actual Close Prices
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=stock_data.index, 
            y=stock_data['Close'], 
            mode='lines', 
            name='Close Price',
            line=dict(color='#2563eb', width=2)
        ))
        fig1.update_layout(
            title="Historical Close Prices",
            xaxis_title="Date",
            yaxis_title="Price ($)",
            hovermode='x unified',
            showlegend=True
        )

        # Interactive plot 2 - Original vs Predicted (FIXED)
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=plotting_df.index, 
            y=plotting_df["Original"], 
            name="Actual Prices",
            line=dict(color='#2563eb', width=2),
            mode='lines'
        ))
        fig2.add_trace(go.Scatter(
            x=plotting_df.index, 
            y=plotting_df["Predicted"], 
            name="Model Predictions", 
            line=dict(color='#ef4444', width=2, dash="dot"),
            mode='lines'
        ))
        fig2.update_layout(
            title="Model Predictions vs Actual Prices",
            xaxis_title="Date",
            yaxis_title="Price ($)",
            hovermode='x unified',
            showlegend=True
        )

        # Future Predictions
        last_100 = stock_data[['Close']].tail(100)
        last_100_scaled = scaler.transform(last_100)
        future_predictions = []
        input_seq = last_100_scaled.reshape(1, -1, 1)

        print(f"Generating {no_of_days} future predictions...")

        for day in range(no_of_days):
            pred = model.predict(input_seq, verbose=0)
            future_price = scaler.inverse_transform(pred)[0, 0].item()
            future_predictions.append(future_price)
            input_seq = np.append(input_seq[:, 1:, :], pred.reshape(1, 1, -1), axis=1)

        print(f"Future predictions generated: {len(future_predictions)} values")
        print(f"Future predictions: {future_predictions}")

        # Create future dates starting from tomorrow
        last_date = stock_data.index[-1]
        future_dates = []
        for i in range(1, no_of_days + 1):
            future_date = last_date + timedelta(days=i)
            future_dates.append(future_date.strftime("%Y-%m-%d"))

        print(f"Future dates: {future_dates}")

        # Interactive plot 3 - Future Predictions (COMPLETELY FIXED)
        fig3 = go.Figure()

        # Add the future predictions trace
        fig3.add_trace(go.Scatter(
            x=future_dates,
            y=future_predictions,
            mode='lines+markers',
            name='Future Predictions',
            line=dict(color='#10b981', width=3),
            marker=dict(size=8, color='#10b981', symbol='circle'),
            hovertemplate='<b>Date: %{x}</b><br>Predicted Price: $%{y:.2f}<extra></extra>'
        ))

        # Update layout
        fig3.update_layout(
            title=f"Future Price Predictions ({no_of_days} Days)",
            xaxis_title="Date",
            yaxis_title="Predicted Price ($)",
            hovermode='closest',
            showlegend=True,
            xaxis=dict(
                type='category',
                title_font=dict(size=14),
                tickfont=dict(size=12)
            ),
            yaxis=dict(
                tickformat='$,.2f',
                title_font=dict(size=14),
                tickfont=dict(size=12)
            ),
            margin=dict(l=50, r=50, t=60, b=50),
            height=400
        )

        print(f"Chart 3 created successfully with {len(future_predictions)} data points")

        # Calculate prediction details for table
        prediction_details = []
        current_price = stats["Latest"]
        
        for i, price in enumerate(future_predictions):
            day = i + 1
            
            # Calculate change from previous day
            if i == 0:
                day_change = price - current_price
                change_percent = (day_change / current_price) * 100
            else:
                previous_price = future_predictions[i - 1]
                day_change = price - previous_price
                change_percent = (day_change / previous_price) * 100
            
            # Determine trend
            trend = "Bullish" if day_change >= 0 else "Bearish"
            trend_class = "success" if day_change >= 0 else "danger"
            change_class = "success" if day_change >= 0 else "danger"
            
            prediction_details.append({
                "day": day,
                "price": round(price, 2),
                "change": round(day_change, 2),
                "change_percent": round(change_percent, 2),
                "trend": trend,
                "trend_class": trend_class,
                "change_class": change_class
            })

        # Calculate summary
        final_price = future_predictions[-1]
        total_change = final_price - current_price
        total_change_percent = (total_change / current_price) * 100
        
        summary = {
            "current_price": current_price,
            "final_price": round(final_price, 2),
            "total_change": round(total_change, 2),
            "total_change_percent": round(total_change_percent, 2),
            "change_class": "success" if total_change >= 0 else "danger"
        }

        # Convert charts to JSON
        fig1_json = plot_to_json(fig1)
        fig2_json = plot_to_json(fig2)
        fig3_json = plot_to_json(fig3)

        print("All charts converted to JSON successfully")
        print(f"Chart data lengths - Fig1: {len(fig1.data)}, Fig2: {len(fig2.data)}, Fig3: {len(fig3.data)}")

        return render_template(
            "result.html",
            stock=stock,
            long_name=long_name,
            logo_url=logo_url,
            stats=stats,
            future_predictions=[round(p, 2) for p in future_predictions],
            prediction_details=prediction_details,
            summary=summary,
            fig1_json=fig1_json,
            fig2_json=fig2_json,
            fig3_json=fig3_json
        )

    except Exception as e:
        # Log the error for debugging
        print(f"Error in predict function: {str(e)}")
        import traceback
        traceback.print_exc()
        return render_template("result.html", error=f"An error occurred while processing your request: {str(e)}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
