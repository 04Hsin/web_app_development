from flask import Blueprint, render_template, request, redirect, url_for, session

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    顯示註冊表單 (GET) 與處理註冊邏輯 (POST)
    - 驗證並儲存新使用者，成功後重導向至登入頁面。
    - 錯誤時提供訊息並重新渲染 auth/register.html
    """
    pass

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    顯示登入表單 (GET) 與處理登入邏輯 (POST)
    - 驗證使用者帳密，設定 session。
    - 成功登入後重導至首頁或 auth/profile.html
    """
    pass

@auth_bp.route('/logout', methods=['GET'])
def logout():
    """
    清除目前的登入 session，並重導向回首頁。
    """
    pass

@auth_bp.route('/profile', methods=['GET'])
def profile():
    """
    會員中心
    - 需先驗證登入。
    - 列出使用者建立的個人食譜清單。
    - 渲染 auth/profile.html
    """
    pass
