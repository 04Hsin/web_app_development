from app.database import get_db_connection
from datetime import datetime

class User:
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
        conn = get_db_connection()
        rows = conn.execute('SELECT * FROM users').fetchall()
        conn.close()
        return [User._from_row(row) for row in rows]

    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        row = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        return User._from_row(row)

    @staticmethod
    def get_by_email(email):
        conn = get_db_connection()
        row = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        return User._from_row(row)

    @staticmethod
    def update(user_id, username=None, email=None, is_admin=None):
        conn = get_db_connection()
        current_user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        if not current_user:
            conn.close()
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
        conn.close()
        return True

    @staticmethod
    def delete(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
