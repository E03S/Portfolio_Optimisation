# Benzinga News Parser

The Benzinga News Parser is a Python class designed to retrieve news articles from the Benzinga website for specified tickers. It allows users to retrieve news articles for a given list of tickers within a specified date range.

## Getting Started

1. Sign up for an account on Benzinga and obtain an API key.
2. Replace `YOUR_API_KEY` in the script with your actual Benzinga API key.

## Usage

1. Instantiate the `BenzingaNewsParser` class with your API key, tickers, start date, and end date.
2. Use the `run_concurrent()` method to fetch news articles for the specified tickers.
3. Use the `save_dataset()` method to save the dataset to a CSV file.

### Example

```python
from BenzingaNewsParser import BenzingaNewsParser

# Example usage:
tickers = ["AAPL", "GOOGL", "MSFT"]  # Example list of tickers
start_date = "2024-01-01"  # Example start date
end_date = "2024-03-01"  # Example end date
api_key = "YOUR_API_KEY"  # Replace with your actual API key

benzinga_fetcher = BenzingaNewsParser(api_key, tickers, start_date, end_date)
benzinga_fetcher.run_concurrent()
benzinga_fetcher.save_dataset()
```

# S&P 500 Parser

This Python class, `SP500Parser`, is designed to make it easy to retrieve and work with data related to S&P 500 companies. It provides functions to obtain the list of S&P 500 company tickers, download historical data for these companies, and save the data to a CSV file.

## Features

- Retrieve the list of S&P 500 company tickers.
- Download historical data for S&P 500 companies.
- Save the downloaded data to a CSV file.

## Usage

### Import the Class
Import the SP500Parser class in your Python script:

```python
from SP500Parser import SP500Parser
```
### Create an Instance
Create an instance of the SP500Parser class:

```python
parser = SP500Parser()
```
### Retrieve S&P 500 Tickers
To retrieve the list of S&P 500 company tickers, use the `get_sp500_tickers` method:
```python
tickers = parser.get_sp500_tickers()
```
### Download Historical Data
To download historical data for S&P 500 companies, use the `download_sp500_data method`. You can specify the date range for data retrieval and time interval:

```python
start_date = datetime(2008, 1, 1)
end_date = date.today()
data = parser.download_sp500_data(start_date, end_date, interval)
```
### Save Data to CSV
You can save the downloaded data to a CSV file using the save_data_to_csv method:

```python
parser.save_data_to_csv('sp500_data.csv')
```
### Download Custom Data:
To download historical data specific companies, use the `download_custom_data method`. You can specify the date range for data retrieval and time interval:
```python
parser.download_custom_data(custom_tickers, start_date, end_date)
```
### Example
Here's an example of how to use the `SP500Parser` class:

```python
from SP500Parser import SP500Parser
from datetime import datetime, date

# Create an instance of the parser
parser = SP500Parser()

# Retrieve the list of S&P 500 company tickers
tickers = parser.get_sp500_tickers()

# Download historical data
start_date = datetime(2008, 1, 1)
end_date = date.today()
data = parser.download_sp500_data(start_date, end_date)

# Save the data to a CSV file
parser.save_data_to_csv('sp500_data.csv')
```
### Acknowledgments
This project uses data from [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies) to retrieve the list of S&P 500 company tickers.
It utilizes the [Yahoo Finance package](https://pypi.org/project/yfinance/) to download historical stock data.
