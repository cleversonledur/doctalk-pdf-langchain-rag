from langchain import PromptTemplate
from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import RetrievalQA

from colorama import Fore, Style

from document.loader import load_document
from text.splitter import split_text
from vector.store import create_vector_store
import argparse

def main():

    parser = argparse.ArgumentParser(
        description="PDF Question Answering using Ollama and Llama3"
    )
    parser.add_argument("-f", "--file", required=True, help="Path to the PDF file")
    args = parser.parse_args()
    file_path = args.file

    data = load_document(file_path)
    all_splits = split_text(data)
    vectorstore = create_vector_store(all_splits)

    while True:
        file_name = file_path.split("/")
        file_name = file_name[-1] if len(file_name) > 1 else file_name[0]
        query = input(
            f"\n\n{Fore.LIGHTYELLOW_EX}[DOCTALK] Ask your question ({file_name}): {Style.RESET_ALL}"
        ).strip()
        if query == "exit":
            break
        if not query:
            continue

        template = """Use the following pieces of context to answer the question. {context}. Question: {question}. Helpful Answer:"""

        QA_CHAIN_PROMPT = PromptTemplate(
            input_variables=["context", "question"],
            template=template,
        )

        llm = Ollama(
            model="llama3",
            callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
        )
        qa_chain = RetrievalQA.from_chain_type(
            llm,
            retriever=vectorstore.as_retriever(),
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
        )

        qa_chain({"query": query})


if __name__ == "__main__":
    main()
