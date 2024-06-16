from langchain.vectorstores import Chroma
from langchain.embeddings import GPT4AllEmbeddings


def create_vector_store(documents):
    return Chroma.from_documents(documents=documents, embedding=GPT4AllEmbeddings())
