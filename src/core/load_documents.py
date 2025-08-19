import os
from src.core.document_processor import DocumentProcessor
from src.core.retrieval import RAGService

def load_fitness_documents():
    processor = DocumentProcessor()
    rag_service = RAGService()

    pdf_folder = "data/pdfs"

    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder, exist_ok=True)
        return

    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]

    if not pdf_files:
        return

    all_documents = []
    for pdf_file in pdf_files:
        file_path = os.path.join(pdf_folder, pdf_file)
        documents = processor.load_pdf(file_path)
        all_documents.extend(documents)

    rag_service.add_documents(all_documents)

if __name__ == "__main__":
    load_fitness_documents()
