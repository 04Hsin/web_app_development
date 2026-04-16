from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    """
    處理首頁
    - 取得最新推薦食譜清單
    - 渲染 index.html
    """
    pass
