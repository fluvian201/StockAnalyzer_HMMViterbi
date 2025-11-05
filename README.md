# Stock Stochastic Analyzer: Hidden Markov Model (HMM) Comparison

## 💡 Project Overview

This project provides a sophisticated tool for **dual-stock market state analysis** using the **Hidden Markov Model (HMM)** and the **Viterbi Algorithm**.

The goal is to determine the most likely sequence of *hidden market states* (e.g. "Bullish" or "Bearish") that led to the observed stock price movements for two different assets. This is a powerful, data-driven approach for comparative financial analysis.

### ✨ Key Features

* **Dual-Stock HMM Analysis:** Simultaneously models the hidden states of two distinct stock tickers.
* **Viterbi Path Determination:** Uses the Viterbi algorithm to efficiently find the single most likely sequence of hidden states. 
* **Customizable Sequences:** Features an adjustable **$n$-Sequence** parameter, allowing the user to control the complexity and lookback depth of the HMM's state calculation.
* **Look-Ahead Forecasting (`Shift Data`):** A unique feature that allows for comparing current stock data with projected data $n$ days into the future, enabling prospective analysis (e.g., comparing today's state to where the model predicts the state will be next week).
* **Data Source Integrity:** Stock data is sourced directly using the popular `yfinance` library. **NOTE:** All ticker symbols must match those provided by Yahoo Finance.

## ⚙️ Getting Started

### 1. Prerequisites

Ensure you have Python installed (version 3.6 or higher recommended).

### 2. Setup

It is highly recommended to use a virtual environment to manage dependencies:

```bash
# Create and activate environment (example for Linux/macOS)
python3 -m venv venv
source venv/bin/activate

# For Windows, use:
# .\venv\Scripts\activate
```

### 3. Installation

Install all required Python packages from the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4. Execution

```bash
python main.py
```
### NOTE: THE STOCK 2 IS BEING THE OBSERVATION, SO THE STOCK 1 IS THE TARGET FOR THE HIDDEN PATH
