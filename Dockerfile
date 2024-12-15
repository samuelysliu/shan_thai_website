# 使用 Python 基礎鏡像
FROM python:3.11-slim

# 設置工作目錄
WORKDIR /app

# 複製代碼和依賴文件
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# 啟動 FastAPI 應用
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
