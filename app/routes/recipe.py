from flask import Blueprint, render_template, request, redirect, url_for, session, abort

recipe_bp = Blueprint('recipe', __name__, url_prefix='/recipes')

@recipe_bp.route('', methods=['GET'])
def index():
    """
    列出所有系統內或公開的食譜總覽
    - 渲染 recipe/index.html
    """
    pass

@recipe_bp.route('/new', methods=['GET', 'POST'])
def new_recipe():
    """
    新增食譜
    - GET: 渲染 recipe/new.html 表單
    - POST: 接收表單，呼叫 Model 儲存食譜及食材關聯。
    - 成功後重導至 /recipes/<id>
    """
    pass

@recipe_bp.route('/<int:recipe_id>', methods=['GET'])
def detail(recipe_id):
    """
    顯示單一食譜詳情
    - 依據 recipe_id 撈出食譜、作者與食材資訊。
    - 找不到時 abort(404)
    - 渲染 recipe/detail.html
    """
    pass

@recipe_bp.route('/<int:recipe_id>/edit', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    """
    編輯食譜
    - GET: 確認身分為擁有者後，帶出舊資料渲染 recipe/edit.html
    - POST: 更新資料庫中的資料，重新導向回 /recipes/<id>
    """
    pass

@recipe_bp.route('/<int:recipe_id>/delete', methods=['POST'])
def delete_recipe(recipe_id):
    """
    刪除食譜
    - 僅接受 POST 防止預取(Prefetch) 或直連網址誤刪
    - 判斷身分為擁有者後，將資料從 DB 中刪除
    - 成功後導回 /auth/profile
    """
    pass
