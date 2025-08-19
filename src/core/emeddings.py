from langchain_openai import OpenAIEmbeddings
import os

class EmbeddingService:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

    def get_embeddings(self):
        return self.embeddings
