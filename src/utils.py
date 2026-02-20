import os
from .config import SENSITIVE_KEYWORDS

def is_sensitive(text: str) -> bool:
    """
    檢查輸入是否包含敏感關鍵字（忽略大小寫）
    """
    return any(word.lower() in text.lower() for word in SENSITIVE_KEYWORDS)

def load_faq_text() -> str:
    """
    載入結構化的 bank_faq.txt 檔案，返回完整文字內容
    """
    faq_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "bank_faq.txt")
    
    if not os.path.exists(faq_path):
        raise FileNotFoundError(f"FAQ TXT 檔案未找到：{faq_path}")
    
    with open(faq_path, "r", encoding="utf-8") as f:
        return f.read()