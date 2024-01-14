def get_news(ticker, page, date_from, date_to, display_output="full"):
    news = paper.news(company_tickers=ticker, display_output=display_output, date_from=date_from, date_to=date_to, page=page, pagesize=100)
    if (len(news) == 0):
        return []
    df = pd.DataFrame(news)
    df['teaser'] = df['teaser'].apply(remove_html_tags)
    df['body'] = df['body'].apply(remove_html_tags)
    return df
