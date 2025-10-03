# Project Plan: Bitcoin Price Swing Prediction with a Transformer Model

## 1. Project Objective

The primary goal of this project is to develop a terminal-based Python application that uses a transformer-based neural network to predict profitable Bitcoin price swings. The model will be trained on the last year of 1-minute or 5-minute BTC data and will aim to identify trading opportunities where the predicted price change is significant enough to cover transaction fees and yield a profit. The system will include a paper trading module to simulate and evaluate the model's performance in real-time.

## 2. Technology Stack

- **Programming Language:** Python 3.10+
- **Core Libraries:**
  - **Neural Network:** PyTorch
  - **Data Manipulation:** Pandas, NumPy
  - **Data Acquisition:** `requests`, `alpaca-py`
  - **Technical Indicators:** `ta` or similar
- **Hardware:** GPU (NVIDIA/CUDA) for training and inference, with a fallback to CPU.

## 3. Project Phases

### Phase 1: Data Acquisition and Preprocessing

- **Objective:** Collect, clean, and prepare one year of high-frequency Bitcoin data.
- **Tasks:**
  1.  **API Selection & Integration:**
      - Evaluate and choose a free data source. Recommended options:
        - **Alpaca API:** Provides a Python SDK (`alpaca-py`) and allows historical data access without an API key.
        - **CryptoCompare API:** Offers extensive historical data with a generous free tier, but requires an API key.
      - Develop a script (`data_loader.py`) to download and store at least one year of BTC/USD data at a 1-minute or 5-minute granularity.
  2.  **Feature Engineering:**
      - From the raw OHLCV (Open, High, Low, Close, Volume) data, generate a rich set of features, including:
        - **Moving Averages:** SMA (5, 10, 20, 50), EMA (12, 26)
        - **Oscillators:** RSI, MACD, Stochastic Oscillator
        - **Volatility Indicators:** Bollinger Bands, Average True Range (ATR)
        - **Volume-based Indicators:** On-Balance Volume (OBV)
  3.  **Data Cleaning and Normalization:**
      - Handle any missing data points (e.g., via forward-fill or interpolation).
      - Normalize all features to a consistent scale (e.g., using `MinMaxScaler` or `StandardScaler`) to improve model training stability.
  4.  **Target Variable Definition:**
      - This is a classification task, not simple price regression. Define three target classes for a future time window (e.g., the next 30 minutes):
        1.  `PROFITABLE_UP`: Price increases by more than `2 * fee_rate`.
        2.  `PROFITABLE_DOWN`: Price decreases by more than `2 * fee_rate`.
        3.  `NO_TRADE`: Price movement is not large enough to be profitable.
      - Assume a standard exchange fee (e.g., `fee_rate = 0.1%`). A profitable swing must be `> 0.2%`.
  5.  **Data Windowing:**
      - Create sequences (windows) of the feature data. For example, use 60 prior time steps (e.g., 60 minutes of data) to predict the label for the subsequent 30 minutes.

### Phase 2: Model Development

- **Objective:** Design and build a small transformer model for sequence classification.
- **Tasks:**
  1.  **Model Architecture (`model.py`):**
      - Implement a transformer encoder-based model in PyTorch.
      - **Input:** A sequence of feature vectors (e.g., shape: `[batch_size, 60, num_features]`).
      - **Core:**
        - Positional Encoding to give the model temporal awareness.
        - 2-3 Transformer Encoder Layers.
        - 2-4 Attention Heads per layer.
        - A feed-forward network dimension of ~128-256.
      - **Output:** A classification head (Linear layer + Softmax) that outputs a probability distribution over the three target classes (`PROFITABLE_UP`, `PROFITABLE_DOWN`, `NO_TRADE`).
  2.  **GPU/CPU Handling:**
      - Implement logic to automatically detect and use an available CUDA-enabled GPU. If no GPU is found, the code should default to using the CPU for all tensor operations.

### Phase 3: Training and Evaluation

- **Objective:** Train the model and rigorously evaluate its predictive power.
- **Tasks:**
  1.  **Training Script (`train.py`):**
      - Split the historical data into training, validation, and test sets (e.g., 70-15-15 split).
      - Use a Cross-Entropy Loss function, suitable for multi-class classification.
      - Implement an AdamW optimizer with a learning rate scheduler (e.g., `ReduceLROnPlateau`).
      - Log training and validation loss/accuracy after each epoch to monitor for overfitting.
  2.  **Evaluation:**
      - On the hold-out test set, evaluate the model's performance using:
        - **Classification Metrics:** Accuracy, Precision, Recall, and F1-score for each class.
        - **Confusion Matrix:** To visualize how the model confuses the classes.
        - **Simulated Profitability:** Run a backtest on the test set to calculate the hypothetical P&L based on the model's predictions.

### Phase 4: Real-time Inference and Paper Trading

- **Objective:** Use the trained model to make predictions on live data and simulate trades.
- **Tasks:**
  1.  **Inference Loop (`trade.py`):**
      - Develop a script that fetches the latest BTC data every minute.
      - Preprocess the incoming data and assemble a feature sequence matching the model's input format.
      - Load the trained model weights and run inference to get a prediction.
  2.  **Trading Logic:**
      - The core trading decision will be based on a confidence threshold.
      - **Entry Condition:** If the model predicts `PROFITABLE_UP` with a probability `> 0.75` (example threshold), execute a paper "BUY" order. If it predicts `PROFITABLE_DOWN` with probability `> 0.75`, execute a paper "SELL" order.
      - **Exit Condition:** Define a simple exit strategy, such as closing the position after the target time window (e.g., 30 minutes) has passed.
  3.  **Terminal Output (`main.py`):**
      - Create a main application loop that orchestrates the process.
      - Display real-time predictions, paper trade actions (BUY/SELL/HOLD), and a running summary of simulated P&L in a clean, readable terminal interface.

## 4. File Structure

```
/
├── .gitignore
├── main.py                 # Main application entry point
├── PROJECT_PLAN.md         # This file
├── requirements.txt        # Project dependencies
├── data_loader.py          # Scripts for downloading and preparing data
├── model.py                # Transformer model definition
├── train.py                # Script to train the model
├── trade.py                # Real-time inference and paper trading logic
└── data/
    └── btc_data_1min.csv   # Stored historical data
```
