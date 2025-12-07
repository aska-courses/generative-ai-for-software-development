import glob
import os

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from config import EMBEDDING_MODEL, KNOWLEDGE_BASE_DIR, DB_DIR


def load_documents(base_dir: str):
    """
    Load all .md files from subfolders of base_dir.
    Each subfolder name becomes metadata['doc_type'] (as in the notebook).
    """
    folders = glob.glob(os.path.join(base_dir, "*"))
    text_loader_kwargs = {"encoding": "utf-8"}

    documents = []
    for folder in folders:
        if not os.path.isdir(folder):
            continue
        doc_type = os.path.basename(folder)
        loader = DirectoryLoader(
            folder,
            glob="**/*.md",
            loader_cls=TextLoader,
            loader_kwargs=text_loader_kwargs,
        )
        folder_docs = loader.load()
        for doc in folder_docs:
            doc.metadata["doc_type"] = doc_type
            documents.append(doc)

    print(f"Loaded {len(documents)} documents from {base_dir}")
    return documents


def build_and_save_vectorstore():
    #load docs
    documents = load_documents(KNOWLEDGE_BASE_DIR)

    #split into chunks 
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    print(f"Total number of chunks: {len(chunks)}")
    print(f"Document types: {set(doc.metadata['doc_type'] for doc in documents)}")

    #create embeddings client  FAISS vector store
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    vectorstore = FAISS.from_documents(chunks, embedding=embeddings)

    total_vectors = vectorstore.index.ntotal
    dimensions = vectorstore.index.d
    print(f"There are {total_vectors} vectors with {dimensions:,} dimensions in the vector store")

    # 5) Save to disk
    vectorstore.save_local(DB_DIR)
    print(f"Vector store saved to directory: {DB_DIR}")


if __name__ == "__main__":
    build_and_save_vectorstore()
