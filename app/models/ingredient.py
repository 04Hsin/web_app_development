from app.database import get_db_connection

class Ingredient:
    """
    Ingredient 資料模型，對應 ingredients 資料表與 recipe_ingredients 關聯表。
    負責處理食材的 CRUD，以及食譜和食材之間的多對多邏輯。
    """
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
        """
        新增一筆食材記錄。如果已存在，可依賴 UNIQUE 限制報錯或另外處理。
        :param name: 食材名稱
        :return: 新增的 ingredient_id
        """
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
        """
        取得所有食材記錄。
        :return: 包含多個 Ingredient 實例的列表
        """
        conn = get_db_connection()
        try:
            rows = conn.execute('SELECT * FROM ingredients').fetchall()
            return [Ingredient._from_row(row) for row in rows]
        except Exception as e:
            raise e
        finally:
            conn.close()

    @staticmethod
    def get_by_id(ingredient_id):
        """
        依據 ID 取得單筆食材記錄。
        :param ingredient_id: 食材 ID
        :return: Ingredient 實例或 None
        """
        conn = get_db_connection()
        try:
            row = conn.execute('SELECT * FROM ingredients WHERE id = ?', (ingredient_id,)).fetchone()
            return Ingredient._from_row(row)
        except Exception as e:
            raise e
        finally:
            conn.close()

    @staticmethod
    def get_by_name(name):
        """
        依據名稱取得單筆食材記錄。可用於判斷食材是否已存在。
        :param name: 食材名稱
        :return: Ingredient 實例或 None
        """
        conn = get_db_connection()
        try:
            row = conn.execute('SELECT * FROM ingredients WHERE name = ?', (name,)).fetchone()
            return Ingredient._from_row(row)
        except Exception as e:
            raise e
        finally:
            conn.close()

    @staticmethod
    def update(ingredient_id, name):
        """
        更新食材記錄名稱。
        :param ingredient_id: 食材 ID
        :param name: 新的食材名稱
        :return: 成功與否 (boolean)
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('UPDATE ingredients SET name = ? WHERE id = ?', (name, ingredient_id))
            success = cursor.rowcount > 0
            conn.commit()
            return success
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def delete(ingredient_id):
        """
        刪除一筆食材記錄。
        :param ingredient_id: 食材 ID
        :return: 成功與否 (boolean)
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM ingredients WHERE id = ?', (ingredient_id,))
            success = cursor.rowcount > 0
            conn.commit()
            return success
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def add_to_recipe(recipe_id, ingredient_id, quantity=None):
        """
        將食材加入特定食譜，寫入 recipe_ingredients 中介表。
        :param recipe_id: 食譜 ID
        :param ingredient_id: 食材 ID
        :param quantity: 數量或份量字串 (如 100g, 2顆)
        :return: 無回傳值
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES (?, ?, ?)',
                (recipe_id, ingredient_id, quantity)
            )
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def get_by_recipe(recipe_id):
        """
        取得特定食譜的食材關聯清單。
        :param recipe_id: 食譜 ID
        :return: 包含食材 ID, 名稱, 與可用份量的 dict 列表
        """
        conn = get_db_connection()
        try:
            rows = conn.execute(
                '''SELECT i.id, i.name, ri.quantity 
                   FROM ingredients i
                   JOIN recipe_ingredients ri ON i.id = ri.ingredient_id
                   WHERE ri.recipe_id = ?''',
                (recipe_id,)
            ).fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            raise e
        finally:
            conn.close()
