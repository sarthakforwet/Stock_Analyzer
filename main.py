import autogen
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import json

# Configure API key
with open('config.json') as config_file:
    config = json.load(config_file)

config_list = [{
    "model": "gpt-3.5-turbo",
    "api_key":config['api_key']
}]

# Configure LLM settings
llm_config = {
    "config_list": config_list,
    "temperature": 0.7,
    "request_timeout": 120,
}

# Create the agents
user_proxy = autogen.UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    llm_config=llm_config
)

stock_analyst = autogen.AssistantAgent(
    name="StockAnalyst",
    llm_config=llm_config,
    system_message="You are a stock market analyst. Analyze data and provide insights."
)

data_scientist = autogen.AssistantAgent(
    name="DataScientist",
    llm_config=llm_config,
    system_message="You are a data scientist. Create visualizations and perform statistical analysis."
)

# Create group chat
groupchat = autogen.GroupChat(
    agents=[user_proxy, stock_analyst, data_scientist],
    messages=[],
    max_round=10
)

manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config
)

def analyze_stock(symbol, period='1y'):
    '''
    Driver function to analyze stock prices for a given company.

    Inputs:
    symbol (str): the stock symbol to analyze.
    period (str): the duration for which to retrieve the stock data.

    Returns:
    dictionary containing stock summary metadata.
    '''

    stock = yf.Ticker(symbol)
    hist = stock.history(period=period)
    
    # Calculate basic metrics
    avg_volume = hist['Volume'].mean()
    daily_returns = hist['Close'].pct_change()
    volatility = daily_returns.std() * (252 ** 0.5)  # Annualized volatility
    
    # Add visualization
    plt.figure(figsize=(12, 6))
    plt.plot(hist.index, hist['Close'])
    plt.title(f'{symbol} Stock Price Over Time')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.savefig('stock_analysis.png')
    plt.close()

    return {
        'avg_volume': avg_volume,
        'volatility': volatility,
        'current_price': hist['Close'][-1],
        'price_change': (hist['Close'][-1] - hist['Close'][0]) / hist['Close'][0] * 100
    }

def main():
    
    # Analyze the stock
    stock_results = analyze_stock('MSFT')
    
    # Format the results for the agents
    initial_message = f"""
    Here is the analysis for MSFT (Microsoft):
    Current Price: ${stock_results['current_price']:.2f}
    Price Change: {stock_results['price_change']:.2f}%
    Average Volume: {stock_results['avg_volume']:.0f}
    Volatility: {stock_results['volatility']:.2f}
    
    Please analyze this data and provide:
    1. Analysis of the stock performance
    2. Review of the generated visualization (saved as 'stock_analysis.png')
    3. Investment recommendations based on these metrics
    """
    
    # Initiate the chat with the analyzed data
    user_proxy.initiate_chat(
        manager,
        message=initial_message
    )

if __name__ == "__main__":
    main()