import os
from flask import Flask

def create_app(test_config=None):
    # 初始化 Flask 應用程式
    app = Flask(__name__, instance_relative_config=True)
    
    # 載入預設設定
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        DATABASE=os.path.join(app.instance_path, 'database.db'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # 確保 instance 資料夾存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 註冊所有 Blueprints
    from app.routes import register_blueprints
    register_blueprints(app)

    return app

def init_db():
    """負責初始化資料庫並匯入 schema.sql 設定"""
    import sqlite3
    db_path = os.path.join('instance', 'database.db')
    os.makedirs('instance', exist_ok=True)
    conn = sqlite3.connect(db_path)
    
    with open('database/schema.sql', 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
        
    conn.commit()
    conn.close()
    print('Initialized the database.')
