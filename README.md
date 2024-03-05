# Portfolio_Optimisation
A repo for an annual group project for ML and High Load Systems course in Higher School of Economics.
Optimising portfolio earnings with nueral networks


##  Result of research at checkpoint 5
| model                                             | mean_absolute_error | mean_squared_error |        r2 | full_train_min | full_train_sec | train_size |
|---------------------------------------------------|----------------------|--------------------|-----------|----------------|----------------|------------|
| metrics_financial_data_only                      |             0.016942 |           0.000640 |  0.665110 |        0      |     10.02   |    946211  |
| metrics_titles_embedding_financial_data           |             0.017106 |           0.000689 |  0.824685 |        0    |     20.25  |     60358  |
| metrics_news_tfidf_title_embedding_financial_data|             0.019028 |           0.000883 |  0.775300 |       45   |     42.97   |     60358  |
| metrics_nlp_news_financial_data                  |             0.019148 |           0.000893 |  0.772712 |       43    |     19.21   |     60358  |
