import json

# print(json.loads("\n[\n  {\n    \"ticker\": \"SPX\",\n    \"sentiment\": 0.5,\n    \"expected_return\": 0.3,\n    \"risk_percentage\": 1.5\n  },\n  {\n    \"ticker\": \"STOXX600\",\n    \"sentiment\": 0.5,\n    \"expected_return\": 0.3,\n    \"risk_percentage\": 1.5\n  },\n  {\n    \"ticker\": \"NXT\",\n    \"sentiment\": 1.0,\n    \"expected_return\": 2.0,\n    \"risk_percentage\": 0.5\n  },\n  {\n    \"ticker\": \"Brent\",\n    \"sentiment\": 0.8,\n    \"expected_return\": 1.5,\n    \"risk_percentage\": 1.0\n  },\n  {\n    \"ticker\": \"WTI\",\n    \"sentiment\": 0.8,\n    \"expected_return\": 1.5,\n    \"risk_percentage\": 1.0\n  }\n]"))

import json
str = '```json\n[\n    {\n        "ticker": "BIDU",\n        "sentiment": 0.76,\n        "expected_return": 7.6,\n        "risk_percentage": 4.8\n    },\n    {\n        "ticker": "LVS",\n        "sentiment": 0.71,\n        "expected_return": 7.1,\n        "risk_percentage": 51.3\n    },\n    {\n        "ticker": "VZ",\n        "sentiment": 0.07,\n        "expected_return": 0.7,\n        "risk_percentage": 15.1\n    },\n    {\n        "ticker": "AAPL",\n        "sentiment": 1.3,\n        "expected_return": 1.3,\n        "risk_percentage": 15.6\n    },\n    {\n        "ticker": "PFE",\n        "sentiment": 0.2,\n        "expected_return": 2.0,\n        "risk_percentage": 50.9\n    },\n    {\n        "ticker": "COF",\n        "sentiment": 0.8,\n        "expected_return": 8.0,\n        "risk_percentage": 24.1\n    },\n    {\n        "ticker": "AMZN",\n        "sentiment": -0.78,\n        "expected_return": -7.8,\n        "risk_percentage": 19.2\n    },\n    {\n        "ticker": "TXN",\n        "sentiment": 0.11,\n        "expected_return": 1.1,\n        "risk_percentage": 15.0\n    },\n    {\n        "ticker": "SPWRA",\n        "sentiment": 2.89,\n        "expected_return": 28.9,\n        "risk_percentage": 14.4\n    },\n    {\n        "ticker": "CSCO",\n        "sentiment": 0,\n        "expected_return": 0,\n        "risk_percentage": 0\n    },\n    {\n        "ticker": "MSFT",\n        "sentiment": 0,\n        "expected_return": 0,\n        "risk_percentage": 0\n    }\n]\n```\nThe output is a JSON array with elements that contain the `ticker`, `sentiment`, `expected_return`, and `risk_percentage` for each mentioned S&P 500 stock in the provided articles. Notably, companies such as Petroleum Consolidators of America Inc (PCAI), Green Planet Bioengineering Co. Ltd., and EarthFirst Canada Inc. are not listed as they are not part of the S&P 500.\n'

print(extract_json_from_text(str))