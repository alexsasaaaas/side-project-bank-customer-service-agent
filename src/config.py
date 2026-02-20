# 知識庫參數
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
RETRIEVE_K = 3  # 檢索前K個相關chunk

# LLM模型 (Groq免費模型，效能好)
LLM_MODEL = "llama-3.1-8b-instant"

# 敏感關鍵字 (中英文)
SENSITIVE_KEYWORDS = ["遺失", "不見", "盜刷", "詐騙", "凍結", "無法登入", "lost", "stolen", "fraud", "frozen", "login issue"]

# 分類Prompt模板
CLASSIFICATION_PROMPT_TEMPLATE = """
你是一個嚴格的 JSON 輸出助手，專門分析銀行客服詢問。**絕對不要輸出任何額外文字、解釋、註解、前後描述或 markdown**，只能輸出以下格式的純 JSON，且必須完整、有效、可被解析。

客戶詢問：{user_input}

分析規則：
- 如果是純問候（如 "你好"、"嗨"、"吃飯了嗎"、"今天天氣真好"）或無具體金融需求 → category 設為 "其他"，urgency 設為 "low"，need_human 設為 false
- 如果涉及信用卡、帳戶、貸款等業務 → category 設為對應類別
- 如果涉及遺失卡片、盜刷、凍結、詐騙等高風險 → need_human 設為 true
- urgency 評估：low（一般問候/查詢）、medium（正常業務）、high（緊急或風險）

現在只輸出以下純 JSON（無前綴、無後綴、無空格多餘）：
{{
  "category": "信用卡 | 帳戶 | 貸款 | 其他",
  "urgency": "low | medium | high",
  "need_human": true/false
}}
"""

# 回覆生成Prompt模板
RESPONSE_PROMPT_TEMPLATE = """
你是銀行客服助手，只能根據以下公開FAQ內容回覆，絕不提供投資建議或具體操作步驟。
相關知識：
{context}

客戶問題：{question}

請生成中性、合規的回覆草稿，用中文回覆，結尾加上「如需進一步協助，請聯繫客服專線」。
"""