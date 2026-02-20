# 模擬銀行客服 Agent (RAG-based)

這是一個使用 LangChain + Groq LLM + HuggingFace Embeddings + Streamlit 建置的銀行客服 AI Agent。
- 功能：敏感詞檢測、分類詢問、使用 RAG 從 FAQ 知識庫生成合規回覆。
- 支援中文輸入，輸出中文。

## 線上 Demo
點這裡直接試用：https://[你的app-name].streamlit.app  (部署後再填)

## 技術亮點
- RAG 架構：從 TXT FAQ 知識庫檢索相關內容，降低 hallucination。
- Prompt Engineering：處理問候、閒聊、敏感問題。
- LLM：Groq (llama-3.3-70b-versatile) 免費快速。
- Embedding：HuggingFace (all-MiniLM-L6-v2) 本地免費。
- UI：Streamlit 聊天介面。

## 本地執行步驟
1. git clone https://github.com/[你的username]/bank-customer-service-agent.git
2. cd bank-customer-service-agent
3. pip install -r requirements.txt
4. 在 .env 填入 GROQ_API_KEY=你的key
5. streamlit run app.py

## 資料夾結構
- app.py: 主程式
- src/: 模組 (config.py, utils.py, rag_pipeline.py, classification.py)
- data/: FAQ 知識庫 (bank_faq.txt)
- requirements.txt: 依賴套件

