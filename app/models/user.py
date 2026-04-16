from app.database import get_db_connection
from datetime import datetime

class User:
    """
    User 資料模型，對應 users 資料表。
    負責處理會員的 CRUD 與業務邏輯。
    """
    def __init__(self, id, username, email, password_hash, is_admin=0, created_at=None):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.is_admin = is_admin
        self.created_at = created_at
        
    @classmethod
    def _from_row(cls, row):
        if row:
            return cls(**dict(row))
        return None

    @staticmethod
    def create(username, email, password_hash, is_admin=0):
        """
        新增一筆使用者記錄。
        :param username: 使用者名稱
        :param email: 電子信箱
        :param password_hash: 加密後的密碼
        :param is_admin: 是否為管理員 (預設 0)
        :return: 新增的 user_id
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        created_at = datetime.now().isoformat()
        try:
            cursor.execute(
                '''INSERT INTO users (username, email, password_hash, is_admin, created_at)
                   VALUES (?, ?, ?, ?, ?)''',
                (username, email, password_hash, is_admin, created_at)
            )
            conn.commit()
            user_id = cursor.lastrowid
            return user_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """
        取得所有使用者記錄。
        :return: 包含多個 User 實例的列表
        """
        conn = get_db_connection()
        try:
            rows = conn.execute('SELECT * FROM users').fetchall()
            return [User._from_row(row) for row in rows]
        except Exception as e:
            raise e
        finally:
            conn.close()

    @staticmethod
    def get_by_id(user_id):
        """
        依據 ID 取得單筆使用者記錄。
        :param user_id: 使用者 ID
        :return: User 實例或 None
        """
        conn = get_db_connection()
        try:
            row = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
            return User._from_row(row)
        except Exception as e:
            raise e
        finally:
            conn.close()

    @staticmethod
    def get_by_email(email):
        """
        依據 Email 取得單筆使用者記錄 (登入時使用)。
        :param email: 電子信箱
        :return: User 實例或 None
        """
        conn = get_db_connection()
        try:
            row = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
            return User._from_row(row)
        except Exception as e:
            raise e
        finally:
            conn.close()

    @staticmethod
    def update(user_id, username=None, email=None, is_admin=None):
        """
        更新使用者記錄。
        :param user_id: 要更新的使用者 ID
        :param username: 新的使用者名稱 (可選)
        :param email: 新的電子信箱 (可選)
        :param is_admin: 新的管理員權限 (可選)
        :return: 成功與否 (boolean)
        """
        conn = get_db_connection()
        try:
            current_user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
            if not current_user:
                return False
                
            update_username = username if username is not None else current_user['username']
            update_email = email if email is not None else current_user['email']
            update_is_admin = is_admin if is_admin is not None else current_user['is_admin']
            
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE users SET username = ?, email = ?, is_admin = ? WHERE id = ?',
                (update_username, update_email, update_is_admin, user_id)
            )
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def delete(user_id):
        """
        刪除一筆使用者記錄。
        :param user_id: 要刪除的使用者 ID
        :return: 成功與否 (boolean)
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
            success = cursor.rowcount > 0
            conn.commit()
            return success
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
