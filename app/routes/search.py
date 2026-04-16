from flask import Blueprint, render_template, request

search_bp = Blueprint('search', __name__, url_prefix='/search')

@search_bp.route('', methods=['GET'])
def index():
    """
    搜尋首頁 / 冰箱尋寶輸入頁
    - 顯示可以輸入或選擇食材的表單介面
    - 渲染 search/index.html
    """
    pass

@search_bp.route('/results', methods=['GET'])
def results():
    """
    搜尋結果列表
    - 接收 Query String (如 ?ingredients=番茄,雞蛋 或 ?q=標題關鍵字)
    - 呼叫搜尋演算法比對並撈出符合的食譜清單
    - 渲染 search/results.html
    """
    pass
