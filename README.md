# 🪙 CryptoCurrency Price Predictor

A Flask-based web application that uses deep learning to predict cryptocurrency prices. This project combines data visualization (Plotly), financial data extraction (yfinance), and machine learning (TensorFlow/Keras) for interactive price forecasting.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-v2.0+-green.svg)
![TensorFlow](https://img.shields.io/badge/tensorflow-v2.0+-orange.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## 🌟 Features

- **Interactive Web Interface**: User-friendly UI for selecting cryptocurrency and prediction parameters
- **Real-time Data Fetching**: Uses `yfinance` to retrieve up-to-date historical price data
- **Deep Learning Predictions**: LSTM neural network model for accurate price forecasting
- **Data Visualization**: Interactive charts and graphs powered by Plotly
- **Containerized Deployment**: Fully Dockerized for easy deployment and scaling
- **Multiple Cryptocurrencies**: Support for various cryptocurrency symbols

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|-------------|
| **Backend** | Flask, Python |
| **Machine Learning** | TensorFlow, Keras (LSTM) |
| **Frontend** | HTML, Jinja2, Plotly.js |
| **Data Source** | yfinance API |
| **Containerization** | Docker |
| **Model Format** | HDF5 |

---

## 📂 Project Structure

```
arpitkadam-ai-stock-predictor/
├── app.py                                    # Main Flask application
├── CrypoCurrency_Price_Prediction.ipynb     # Jupyter notebook for model training
├── model.h5                                 # Pre-trained LSTM model
├── requirements.txt                         # Python dependencies
├── Dockerfile                               # Docker configuration
├── README.md                                # Project documentation
└── templates/                               # HTML templates
    ├── base.html                           # Base template
    ├── index.html                          # Home page
    └── result.html                         # Results page
```

---

## 🚀 Quick Start

### 🐳 Docker Deployment (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/arpitkadam/arpitkadam-ai-stock-predictor.git
   cd arpitkadam-ai-stock-predictor
   ```

2. **Build the Docker image**
   ```bash
   docker build -t arpitkadam/stock-predictor-app .
   ```

3. **Run the container**
   ```bash
   docker run -p 5000:5000 arpitkadam/stock-predictor-app
   ```

4. **Access the application**
   Open your browser and navigate to: `http://localhost:5000`

### 💻 Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/arpitkadam/arpitkadam-ai-stock-predictor.git
   cd arpitkadam-ai-stock-predictor
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   Visit `http://localhost:5000` in your browser

---

## 📊 Usage

1. **Select Cryptocurrency**: Choose from available cryptocurrency symbols (BTC, ETH, etc.)
2. **Set Prediction Window**: Define the time period for prediction
3. **View Results**: Analyze the predicted prices with interactive charts
4. **Historical Data**: Review historical price trends and patterns

---

## 🧠 Model Information

- **Architecture**: LSTM (Long Short-Term Memory) Sequential Neural Network
- **Framework**: TensorFlow/Keras
- **Input Features**: Historical price data, volume, and technical indicators
- **Output**: Future price predictions
- **Model File**: `model.h5` (HDF5 format)
- **Training Data**: Historical cryptocurrency data from yfinance

### Model Performance
- Trained on multiple cryptocurrency datasets
- Optimized for short to medium-term price predictions
- Includes data preprocessing and normalization

---

## 🔧 Configuration

### Environment Variables
```bash
FLASK_ENV=development  # or production
FLASK_DEBUG=True       # for development
PORT=5000             # application port
```

### Supported Cryptocurrencies
- Bitcoin (BTC-USD)
- Ethereum (ETH-USD)
- And many more supported by yfinance

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Arpit Kadam**

- 📧 Email: arpitkadam922@gmail.com
- 🔬 Portfolio: [Profile](https://arpit-kadam.netlify.app/)
- 🐙 GitHub: [@arpitkadam](https://github.com/arpitkadam)
- 💼 LinkedIn: [Arpit Kadam](https://linkedin.com/in/arpitkadam)

---

## 🙏 Acknowledgements

- [yfinance](https://github.com/ranaroussi/yfinance) - For financial data API
- [TensorFlow](https://tensorflow.org) - For machine learning framework
- [Plotly](https://plotly.com) - For interactive data visualization
- [Flask](https://flask.palletsprojects.com) - For web framework
- [Docker](https://docker.com) - For containerization

---

## 📈 Future Enhancements

- [ ] Add more cryptocurrency symbols
- [ ] Implement real-time price updates
- [ ] Add technical indicators analysis
- [ ] Include sentiment analysis from news/social media
- [ ] Add user authentication and portfolio tracking
- [ ] Implement API endpoints for external integration

---

## ⚠️ Disclaimer

This application is for educational and research purposes only. Cryptocurrency investments are highly volatile and risky. Always do your own research and consult with financial advisors before making investment decisions.

---

<div align="center">
  <p>Made with ❤️ by Arpit Kadam</p>
  <p>⭐ Star this repo if you found it helpful!</p>
</div>

