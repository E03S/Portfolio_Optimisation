# Portfolio_Optimisation
A repo for an annual group project for ML and High Load Systems course in Higher School of Economics.
Optimising portfolio earnings with nueral networks

# How to use News Parser
Description: this parser get news for specified ticker from benzinga site from 2008 year to our days.

1. Create account on benzinga
2. Get API key
3. Replace YOUR_API_KEY to benzinga api key
4. use ```run_concurent()``` to run first 100 tickers from SP 500 or paste your desired tickers in tickers list
5. You will get dataset for each ticker in datasets folder in csv format
6. Run ```merge_all_in_one_file()``` to get final .csv dataset 
7. Run ```zip_all_datasets()``` to get .zip file with all datasets

Link to example of such dataset from 30 October of 2023 https://drive.google.com/file/d/1sM2s-W7hVqB5dITH38xiWI3dvB019uDn/view?usp=sharing

# S&P 500 Parser

This Python class, `SP500Parser`, is designed to make it easy to retrieve and work with data related to S&P 500 companies. It provides functions to obtain the list of S&P 500 company tickers, download historical data for these companies, and save the data to a CSV file.

## Features

- Retrieve the list of S&P 500 company tickers.
- Download historical data for S&P 500 companies.
- Save the downloaded data to a CSV file.

## Getting Started

### Installation

Make sure you have the necessary packages installed. You can install them using `pip`:

```bash
pip install requirements.txt
```
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
data = parser.download_sp500_data(start_date, end_date, '1h)

# Save the data to a CSV file
parser.save_data_to_csv('sp500_data.csv')
```
### Acknowledgments
This project uses data from [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies) to retrieve the list of S&P 500 company tickers.
It utilizes the [Yahoo Finance package](https://pypi.org/project/yfinance/) to download historical stock data.
