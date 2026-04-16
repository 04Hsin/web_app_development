from app.database import get_db_connection
from datetime import datetime

class Recipe:
    """
    Recipe 資料模型，對應 recipes 資料表。
    負責處理食譜的 CRUD 與業務邏輯。
    """
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
        """
        新增一筆食譜記錄。
        :param user_id: 擁有者 ID
        :param title: 標題
        :param steps: 製作步驟步驟
        :param description: 介紹說明
        :param image_url: 圖片位址
        :param category: 分類
        :return: 新增的 recipe_id
        """
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
        """
        取得所有食譜記錄。
        :return: 包含多個 Recipe 實例的列表
        """
        conn = get_db_connection()
        try:
            rows = conn.execute('SELECT * FROM recipes ORDER BY id DESC').fetchall()
            return [Recipe._from_row(row) for row in rows]
        except Exception as e:
            raise e
        finally:
            conn.close()

    @staticmethod
    def get_by_id(recipe_id):
        """
        依據 ID 取得單筆食譜記錄。
        :param recipe_id: 食譜 ID
        :return: Recipe 實例或 None
        """
        conn = get_db_connection()
        try:
            row = conn.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
            return Recipe._from_row(row)
        except Exception as e:
            raise e
        finally:
            conn.close()
        
    @staticmethod
    def get_by_user_id(user_id):
        """
        依據使用者 ID 取得其所有食譜記錄。
        :param user_id: 使用者 ID
        :return: 包含多個 Recipe 實例的列表
        """
        conn = get_db_connection()
        try:
            rows = conn.execute('SELECT * FROM recipes WHERE user_id = ? ORDER BY id DESC', (user_id,)).fetchall()
            return [Recipe._from_row(row) for row in rows]
        except Exception as e:
            raise e
        finally:
            conn.close()

    @staticmethod
    def update(recipe_id, title=None, description=None, steps=None, image_url=None, category=None):
        """
        更新食譜記錄。
        :param recipe_id: 食譜 ID
        :param title: 新標題 (可選)
        :param description: 新說明 (可選)
        :param steps: 新步驟 (可選)
        :param image_url: 新圖片位址 (可選)
        :param category: 新分類 (可選)
        :return: 成功與否 (boolean)
        """
        conn = get_db_connection()
        try:
            current = conn.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
            if not current:
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
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def delete(recipe_id):
        """
        刪除一筆食譜記錄。
        :param recipe_id: 食譜 ID
        :return: 成功與否 (boolean)
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
            success = cursor.rowcount > 0
            conn.commit()
            return success
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
