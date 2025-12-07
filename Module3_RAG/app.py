import gradio as gr

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain_community.chains import ConversationalRetrievalChain

from config import EMBEDDING_MODEL, CHAT_MODEL, DB_DIR


#Embedding client
embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

#load FAISS vector store saved earlier
vectorstore = FAISS.load_local(
    DB_DIR,
    embeddings,
    allow_dangerous_deserialization=True,
)

#LLM client
llm = ChatOpenAI(
    temperature=0.7,
    model_name=CHAT_MODEL,
)

#conversation memory
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
)

#retriever over the vector store
retriever = vectorstore.as_retriever()

#RAG chain: question + retrieved docs -> LLM
conversation_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
)


#gradio ChatInterface wrapper
def chat(message, history):
    """
    Gradio passes current message and full history.
    We only need the message; history is already in LangChain memory.
    """
    result = conversation_chain.invoke({"question": message})
    return result["answer"]


demo = gr.ChatInterface(
    fn=chat,
    type="messages",
    title="InsureLLM RAG Demo",
    description="Ask questions about the knowledge base (products, employees, contracts, company).",
)


def run_app():
    demo.launch()


if __name__ == "__main__":
    run_app()
