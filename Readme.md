# Stock Analysis Chatbot

This project leverages a combination of natural language processing (NLP) agents and financial data to provide stock analysis, visualizations, and investment recommendations. The system fetches real-time stock data using Yahoo Finance and uses AI agents to interpret and analyze the data.

## Features

- **Stock Data Retrieval**: Fetch stock data from Yahoo Finance using the `yfinance` Python package.
- **Statistical Analysis**: Calculate key metrics such as average volume, volatility, current price, and price change.
- **Data Visualization**: Generate visualizations of stock price over time using `matplotlib`.
- **AI-Based Analysis**: Utilize GPT-3.5 powered agents to analyze the stock data and provide insights.
- **Investment Recommendations**: Based on the analysis, agents provide investment recommendations.

## Requirements

- Python 3.7 or higher
- Required libraries:
  - `autogen`
  - `yfinance`
  - `pandas`
  - `matplotlib`
  - `json`
  
You can install the required libraries using pip:

```bash
pip install autogen yfinance pandas matplotlib
