from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort
from app.models import Recipe, Ingredient

recipe_bp = Blueprint('recipe', __name__, url_prefix='/recipes')

@recipe_bp.route('', methods=['GET'])
def index():
    recipes = Recipe.get_all()
    return render_template('recipe/index.html', recipes=recipes)

@recipe_bp.route('/new', methods=['GET', 'POST'])
def new_recipe():
    user_id = session.get('user_id')
    if not user_id:
        flash('請先登入才能新增食譜', 'error')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        steps = request.form.get('steps')
        image_url = request.form.get('image_url')
        category = request.form.get('category')
        ingredients_raw = request.form.get('ingredients', '')

        if not title or not steps:
            flash('標題與步驟為必填項目', 'error')
            return render_template('recipe/new.html')

        try:
            recipe_id = Recipe.create(user_id, title, steps, description, image_url, category)
            if ingredients_raw:
                ings = [i.strip() for i in ingredients_raw.split(',') if i.strip()]
                for ing_name in ings:
                    ing = Ingredient.get_by_name(ing_name)
                    if not ing:
                        ing_id = Ingredient.create(ing_name)
                    else:
                        ing_id = ing.id
                    Ingredient.add_to_recipe(recipe_id, ing_id)

            flash('成功新增食譜！', 'success')
            return redirect(url_for('recipe.detail', recipe_id=recipe_id))
        except Exception as e:
            flash(f'新增失敗：{str(e)}', 'error')

    return render_template('recipe/new.html')

@recipe_bp.route('/<int:recipe_id>', methods=['GET'])
def detail(recipe_id):
    recipe = Recipe.get_by_id(recipe_id)
    if not recipe:
        abort(404)

    ingredients = Ingredient.get_by_recipe(recipe_id)
    return render_template('recipe/detail.html', recipe=recipe, ingredients=ingredients)

@recipe_bp.route('/<int:recipe_id>/edit', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    recipe = Recipe.get_by_id(recipe_id)
    if not recipe:
        abort(404)

    user_id = session.get('user_id')
    if recipe.user_id != user_id:
        flash('您沒有權限編輯此食譜', 'error')
        return redirect(url_for('recipe.detail', recipe_id=recipe_id))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        steps = request.form.get('steps')
        image_url = request.form.get('image_url')
        category = request.form.get('category')

        if not title or not steps:
            flash('標題與步驟為必填項目', 'error')
            return render_template('recipe/edit.html', recipe=recipe)

        Recipe.update(recipe_id, title, description, steps, image_url, category)
        flash('更新食譜成功！', 'success')
        return redirect(url_for('recipe.detail', recipe_id=recipe_id))

    return render_template('recipe/edit.html', recipe=recipe)

@recipe_bp.route('/<int:recipe_id>/delete', methods=['POST'])
def delete_recipe(recipe_id):
    recipe = Recipe.get_by_id(recipe_id)
    if not recipe:
        abort(404)

    user_id = session.get('user_id')
    if recipe.user_id != user_id:
        flash('您沒有權限刪除此食譜', 'error')
        return redirect(url_for('recipe.index'))

    Recipe.delete(recipe_id)
    flash('食譜已刪除', 'success')
    return redirect(url_for('auth.profile'))
