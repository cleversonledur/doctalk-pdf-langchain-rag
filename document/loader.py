from langchain.document_loaders import PyPDFLoader
from colorama import Fore, Style


def load_document(file_path):
    print(f"Loading document from {Fore.LIGHTGREEN_EX}{file_path}{Style.RESET_ALL}")
    loader = PyPDFLoader(file_path)
    content = loader.load()
    print(f"{Fore.LIGHTGREEN_EX}Document loaded successfully.{Style.RESET_ALL}")
    return content
