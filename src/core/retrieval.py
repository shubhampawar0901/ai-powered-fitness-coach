from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from pinecone import Pinecone
import os
from .emeddings import EmbeddingService

class RAGService:
    def __init__(self):
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.embedding_service = EmbeddingService()
        self.embeddings = self.embedding_service.get_embeddings()
        self.llm = ChatOpenAI(
            model ="gpt-3.5-turbo",
            temperature = 0.6 ,
            openai_api_key = os.getenv("OPENAI_API_KEY")
        )
        self.vectorstore = None

    def setup_vectorstore(self, index_name: str = "fitness-chatbot"):
        self.vectorstore = PineconeVectorStore(
            index_name=index_name,
            embedding=self.embeddings
        )

    def add_documents(self, documents, index_name: str = "fitness-chatbot"):
        if not self.vectorstore:
            self.setup_vectorstore(index_name)
        self.vectorstore.add_documents(documents)

    def query(self, question: str) -> str:
        if not self.vectorstore:
            raise ValueError("Vector store not initialized")

        docs = self.vectorstore.similarity_search(question, k=3)
        context = "\n".join([doc.page_content for doc in docs])

        prompt = f"""Based on the following fitness knowledge context, answer the question: 
                    Context:{context} 
                    Question: {question} 
                    Answer: """

        response = self.llm.invoke(prompt)
        return response.content