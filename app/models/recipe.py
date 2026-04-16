from app.database import get_db_connection
from datetime import datetime

class Recipe:
    def __init__(self, id, user_id, title, description, steps, image_url=None, category=None, created_at=None, updated_at=None):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.steps = steps
        self.image_url = image_url
        self.category = category
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def _from_row(cls, row):
        if row:
            return cls(**dict(row))
        return None

    @staticmethod
    def create(user_id, title, steps, description=None, image_url=None, category=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        now = datetime.now().isoformat()
        try:
            cursor.execute(
                '''INSERT INTO recipes (user_id, title, description, steps, image_url, category, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                (user_id, title, description, steps, image_url, category, now, now)
            )
            conn.commit()
            recipe_id = cursor.lastrowid
            return recipe_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def get_all():
        conn = get_db_connection()
        rows = conn.execute('SELECT * FROM recipes').fetchall()
        conn.close()
        return [Recipe._from_row(row) for row in rows]

    @staticmethod
    def get_by_id(recipe_id):
        conn = get_db_connection()
        row = conn.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
        conn.close()
        return Recipe._from_row(row)
        
    @staticmethod
    def get_by_user_id(user_id):
        conn = get_db_connection()
        rows = conn.execute('SELECT * FROM recipes WHERE user_id = ?', (user_id,)).fetchall()
        conn.close()
        return [Recipe._from_row(row) for row in rows]

    @staticmethod
    def update(recipe_id, title=None, description=None, steps=None, image_url=None, category=None):
        conn = get_db_connection()
        current = conn.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
        if not current:
            conn.close()
            return False
            
        new_title = title if title is not None else current['title']
        new_desc = description if description is not None else current['description']
        new_steps = steps if steps is not None else current['steps']
        new_img = image_url if image_url is not None else current['image_url']
        new_cat = category if category is not None else current['category']
        updated_at = datetime.now().isoformat()
        
        cursor = conn.cursor()
        cursor.execute(
            '''UPDATE recipes 
               SET title = ?, description = ?, steps = ?, image_url = ?, category = ?, updated_at = ? 
               WHERE id = ?''',
            (new_title, new_desc, new_steps, new_img, new_cat, updated_at, recipe_id)
        )
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def delete(recipe_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
