import glob
import os
import argparse
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

from config import EMBEDDING_MODEL, KNOWLEDGE_BASE_DIR, DB_DIR, DB_DIR_OVERLAP


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
    text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=False)
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


def build_and_save_vectorstore_overlap():
    documents = load_documents(KNOWLEDGE_BASE_DIR)

    # Markdown-aware splitter with smaller, overlapping chunks
    splitter = RecursiveCharacterTextSplitter.from_language(
        language="markdown",
        chunk_size=600,      # smaller chunks
        chunk_overlap=300,   # more overlap than baseline
    )
    chunks = splitter.split_documents(documents)
    print(f"[overlap] Total chunks: {len(chunks)}")

    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    vectorstore = FAISS.from_documents(chunks, embedding=embeddings)

    total_vectors = vectorstore.index.ntotal
    dimensions = vectorstore.index.d
    print(f"[overlap] There are {total_vectors} vectors with {dimensions:,} dimensions")

    vectorstore.save_local(DB_DIR_OVERLAP)
    print(f"[overlap] Saved FAISS index to: {DB_DIR_OVERLAP}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=["baseline", "overlap"],
        default="baseline",
        help="Which index to build",
    )
    args = parser.parse_args()

    if args.mode == "baseline":
        build_and_save_vectorstore()
    else:
        build_and_save_vectorstore_overlap()
