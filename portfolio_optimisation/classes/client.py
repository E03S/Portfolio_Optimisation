import requests

class Client:
    def __init__(self, base_url):
        self.base_url = base_url

    def make_api_call(self, endpoint, method='GET', params=None, json=None, headers=None):
        url = self.base_url + endpoint
        response = requests.request(method, url, params=params, json=json, headers=headers)
        return response

    def make_prediction(self, ticker):
        response = self.make_api_call('/predictor/predict_weekly_return_batch', method='POST', json=ticker)
        return response.json()
    
    def make_batch_prediction(self, tickers):
        response = self.make_api_call('/predictor/predict_weekly_return_batch', method='POST', json=tickers)
        return response.json()