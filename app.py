from app import create_app
from dotenv import load_dotenv

# 讀取 .env 中的環境變數
load_dotenv()

app = create_app()

if __name__ == '__main__':
    # 啟動 Flask 開發伺服器
    app.run(debug=True)
