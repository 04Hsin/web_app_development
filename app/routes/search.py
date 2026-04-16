from flask import Blueprint, render_template, request
from app.models import Recipe, Ingredient

search_bp = Blueprint('search', __name__, url_prefix='/search')

@search_bp.route('', methods=['GET'])
def index():
    return render_template('search/index.html')

@search_bp.route('/results', methods=['GET'])
def results():
    query_ingredients = request.args.get('ingredients', '')
    recipes = []
    
    if query_ingredients:
        ings = [i.strip() for i in query_ingredients.split(',') if i.strip()]
        all_recipes = Recipe.get_all()
        for r in all_recipes:
            r_ings = Ingredient.get_by_recipe(r.id)
            r_ing_names = [i['name'] for i in r_ings]
            if set(ings) & set(r_ing_names):
                recipes.append(r)
                
    return render_template('search/results.html', recipes=recipes, query=query_ingredients)
