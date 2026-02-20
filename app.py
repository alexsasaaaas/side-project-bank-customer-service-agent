import streamlit as st
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from src.config import LLM_MODEL
from src.utils import is_sensitive, load_faq_text
from src.rag_pipeline import build_rag_chain
from src.classification import build_classification_chain

# 載入環境變數
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# 初始化 LLM (用 Groq)
llm = ChatGroq(model=LLM_MODEL, temperature=0)

# 建 chain (使用 cache 避免重複建構)
@st.cache_resource
def get_chains():
    classification_chain = build_classification_chain(llm)
    rag_chain = build_rag_chain(llm)
    return classification_chain, rag_chain

classification_chain, rag_chain = get_chains()

# Streamlit UI
st.title("模擬銀行客服 Agent (RAG-based)")

# 聊天歷史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 顯示歷史訊息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 用戶輸入
if prompt := st.chat_input("輸入您的問題（支援中文）"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Step 1: Rule-based 敏感檢測
            if is_sensitive(prompt):
                response = "偵測到敏感問題，請直接聯繫人工客服處理。"
            else:
                # Step 2: 分類
                classification = classification_chain.invoke({"user_input": prompt})
                
                if classification.get("need_human", False):
                    response = "此問題需人工介入，請聯繫客服專線。"
                else:
                    # Step 3-4: RAG + 生成回覆
                    rag_result = rag_chain.invoke(prompt)  # 直接傳 string，讓 chain 處理 question
                    response = rag_result.content  # Groq 回傳 AIMessage，內容在 .content

        except Exception as e:
            # 防 crash 處理
            response = f"抱歉，系統目前無法處理您的問題（錯誤：{str(e)}），請直接聯繫人工客服專線。"

        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# 側邊欄：顯示 FAQ 載入狀態
with st.sidebar:
    st.header("系統狀態")
    faq_content = load_faq_text()
    if faq_content:
        st.success("FAQ 知識庫已載入")
    else:
        st.error("FAQ 檔案未找到，請檢查 data/bank_faq.txt")