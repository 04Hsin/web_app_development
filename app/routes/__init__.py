from .main import main_bp
from .auth import auth_bp
from .recipe import recipe_bp
from .search import search_bp

def register_blueprints(app):
    """
    將所有 Blueprint 註冊至 Flask App 實例中
    """
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(recipe_bp)
    app.register_blueprint(search_bp)
