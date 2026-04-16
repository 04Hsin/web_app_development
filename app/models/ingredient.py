from app.database import get_db_connection

class Ingredient:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def _from_row(cls, row):
        if row:
            return cls(**dict(row))
        return None

    @staticmethod
    def create(name):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO ingredients (name) VALUES (?)', (name,))
            conn.commit()
            ingredient_id = cursor.lastrowid
            return ingredient_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def get_all():
        conn = get_db_connection()
        rows = conn.execute('SELECT * FROM ingredients').fetchall()
        conn.close()
        return [Ingredient._from_row(row) for row in rows]

    @staticmethod
    def get_by_id(ingredient_id):
        conn = get_db_connection()
        row = conn.execute('SELECT * FROM ingredients WHERE id = ?', (ingredient_id,)).fetchone()
        conn.close()
        return Ingredient._from_row(row)

    @staticmethod
    def get_by_name(name):
        conn = get_db_connection()
        row = conn.execute('SELECT * FROM ingredients WHERE name = ?', (name,)).fetchone()
        conn.close()
        return Ingredient._from_row(row)

    @staticmethod
    def update(ingredient_id, name):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('UPDATE ingredients SET name = ? WHERE id = ?', (name, ingredient_id))
            success = cursor.rowcount > 0
            conn.commit()
            return success
        finally:
            conn.close()

    @staticmethod
    def delete(ingredient_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM ingredients WHERE id = ?', (ingredient_id,))
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success

    @staticmethod
    def add_to_recipe(recipe_id, ingredient_id, quantity=None):
        """將食材加入特定食譜"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES (?, ?, ?)',
            (recipe_id, ingredient_id, quantity)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_by_recipe(recipe_id):
        """取得特定食譜的食材清單"""
        conn = get_db_connection()
        rows = conn.execute(
            '''SELECT i.id, i.name, ri.quantity 
               FROM ingredients i
               JOIN recipe_ingredients ri ON i.id = ri.ingredient_id
               WHERE ri.recipe_id = ?''',
            (recipe_id,)
        ).fetchall()
        conn.close()
        # Return dicts combining ingredient info and quantity
        return [dict(row) for row in rows]
