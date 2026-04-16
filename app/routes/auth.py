from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, Recipe

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not username or not email or not password:
            flash('請填寫所有必填欄位', 'error')
            return render_template('auth/register.html')

        if User.get_by_email(email):
            flash('該信箱已經被註冊過了', 'error')
            return render_template('auth/register.html')

        try:
            password_hash = generate_password_hash(password, method='pbkdf2:sha256')
            User.create(username, email, password_hash)
            flash('註冊成功！請登入', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(f'註冊發生錯誤：{str(e)}', 'error')

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('請輸入信箱與密碼', 'error')
            return render_template('auth/login.html')

        user = User.get_by_email(email)
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('登入成功', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('信箱或密碼錯誤', 'error')

    return render_template('auth/login.html')

@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    flash('您已成功登出', 'success')
    return redirect(url_for('main.index'))

@auth_bp.route('/profile', methods=['GET'])
def profile():
    user_id = session.get('user_id')
    if not user_id:
        flash('請先登入以查看會員中心', 'error')
        return redirect(url_for('auth.login'))

    user_recipes = Recipe.get_by_user_id(user_id)
    return render_template('auth/profile.html', recipes=user_recipes)
