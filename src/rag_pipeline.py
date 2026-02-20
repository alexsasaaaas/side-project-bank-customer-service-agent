import streamlit as st
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings  # 免費、本地 embedding
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from .config import CHUNK_SIZE, CHUNK_OVERLAP, RETRIEVE_K, RESPONSE_PROMPT_TEMPLATE
from .utils import load_faq_text

@st.cache_resource
def build_vectorstore():
    """
    建置向量資料庫（使用 Chroma 本地儲存）
    從 TXT 載入後切割成 chunks
    """
    faq_text = load_faq_text()
    if not faq_text:
        raise ValueError("FAQ 文字未載入，請檢查 data/bank_faq.txt")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    docs = text_splitter.split_text(faq_text)

    # 使用免費的 HuggingFace embedding 模型（支援中英，輕量）
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}  # 如果有 GPU 可改 'cuda'
    )

    vectorstore = Chroma.from_texts(
        docs,
        embeddings,
        collection_name="bank_faq"
    )
    return vectorstore

def get_retriever():
    """
    取得檢索器
    """
    vectorstore = build_vectorstore()
    return vectorstore.as_retriever(search_kwargs={"k": RETRIEVE_K})

def build_rag_chain(llm):
    """
    建置 RAG chain (使用 LCEL 寫法)
    """
    retriever = get_retriever()
    qa_prompt = PromptTemplate.from_template(RESPONSE_PROMPT_TEMPLATE)

    # 格式化檢索到的文件
    def format_docs(docs):
        return "\n\n".join([d.page_content for d in docs])

    # LCEL pipeline
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | qa_prompt
        | llm
    )
    return rag_chain