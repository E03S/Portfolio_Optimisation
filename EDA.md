1. Проведен анализ данных текстов новостей и заголовков которые мы собрали.
2. Основная работа проводилась с LLM и возможностями их файнтюна

Пример вывода зайфантюненной модели chatgpt 3.5 на одной из новостей нашего датасета.

{
  "recommendations": [
    {
      "company": "Euro Stoxx 50",
      "action": "sell",
      "signal_strength": 0.6,
      "reason": "Contracts fell 0.6% indicating a potential downtrend."
    },
    {
      "company": "S&P 500",
      "action": "hold",
      "signal_strength": 0.5,
      "reason": "Futures were little changed, suggesting stability."
    },
    {
      "company": "Allianz",
      "action": "buy",
      "signal_strength": 0.7,
      "reason": "Reported third-quarter operating profit that beat estimates."
    },
    {
      "company": "SoftBank Group Corp.",
      "action": "sell",
      "signal_strength": 0.8,
      "reason": "Shares tumbled due to losses in its flagship Vision Fund."
    },
    {
      "company": "Meta Platforms Inc.",
      "action": "buy",
      "signal_strength": 0.65,
      "reason": "Struck a tentative deal in China, indicating potential growth."
    },
    {
      "commodity": "Bitcoin",
      "action": "buy",
      "signal_strength": 0.6,
      "reason": "Edged closer to $37,000, showing upward momentum."
    },
    {
      "commodity": "West Texas Intermediate",
      "action": "hold",
      "signal_strength": 0.55,
      "reason": "Rose to trade around $76 per barrel, indicating stability."
    },
    {
      "commodity": "Gold",
      "action": "hold",
      "signal_strength": 0.5,
      "reason": "Little changed, suggesting current stability."
    }
  ],
  "disclaimer": "This analysis is based solely on the provided news article and does not constitute financial advice. Recommendations are subject to change based on market conditions."
}

Выводы: собранные датасеты новостей недостаточно для файнтюнинга моделей необходимо собрать новый датасет в формате вопрос ответ, для каждого из планируемого User Agent. Для этого необходимо провести разметку датасета вручную или с помощью синтетических данных.

Собранный датасет из исторических данных по ценам акций индекса S&P 500 достаточен для использования как долговременной памяти User agent.
