from sentence_transformers import SentenceTransformer


class NewsEmbedder:
    def __init__(self, embedding_model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(embedding_model_name)

    def embed(self, news: list[str]):
        return self.model.encode(news)

    def calculate_common_embedding(self, news: list[str]):
        if len(news) == 0:
            # retrun zero vector if no news
            return [0] * self.model.get_sentence_embedding_dimension()
        embeddings = self.embed(news)
        return embeddings.mean(axis=0)

    def calculate_common_embeddings(self, list_news: list[list[str]]):
        return [self.calculate_common_embedding(news) for news in list_news]
