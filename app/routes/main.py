from flask import Blueprint, render_template
from app.models import Recipe

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    """
    處理首頁
    - 取得最新推薦食譜清單
    - 渲染 index.html
    """
    # 取得最新的 6 筆食譜作為推薦
    recent_recipes = Recipe.get_all()[:6]
    return render_template('index.html', recipes=recent_recipes)
