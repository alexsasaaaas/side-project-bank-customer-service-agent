@echo off
title 金融客服 RAG Agent - Streamlit Launcher

echo [INFO] 正在檢查環境...

:: 如果你有虛擬環境，可以加這段（取消註解）
:: if exist venv (
::     echo [INFO] 找到虛擬環境，啟動中...
::     call venv\Scripts\activate
:: ) else (
::     echo [WARN] 沒有找到 venv 資料夾，將使用全域 Python
:: )

echo [INFO] 啟動 Streamlit...
python -m streamlit run app.py --server.port 8501

echo.
echo [結束] 應用程式已關閉，按任意鍵離開...
pause