import sqlite3


class DataBase:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cur = self.connection.cursor()
        self.create_db()

    def create_db(self):
        ''' Создаёт базу юзеров, если такой нет. '''
        try:
            query = ('CREATE TABLE IF NOT EXISTS users('
                     'user_id INTEGER PRIMARY KEY,'
                     'user_name TEXT,'
                     
                     'ref_id INTEGER);')
            self.cur.execute(query)
            self.connection.commit()
        except sqlite3.Error as ex:
            print(f'Ошибка при создании базы: {ex}.')

    def __dell__(self):
        self.cur.close()
        self.connection.close()

    def user_exists(self, user_id):
        ''' Проверяет есть ли юзер в базе. '''
        with self.connection:
            result = self.cur.execute('''
                SELECT *
                FROM users
                WHERE user_id = ?;
            ''', (user_id,)).fetchall()
            return bool(len(result))

    def add_user(self,
                 user_id,
                 user_name=None,
                 referrer_id=0,
                 rang=0):
        ''' Создаёт нового пользователя. '''
        with self.connection:
            return self.cur.execute('''
                INSERT INTO users ('user_id', 'user_name', 'ref_id')
                VALUES (?, ?, ?, ?);
            ''', (user_id, user_name, referrer_id))
    
    def get_users(self):
        ''' Запрос данных пользователя. '''
        with self.connection:
            return self.cur.execute('''
                SELECT user_id
                FROM users;
            ''').fetchall()

    def count_all_users(self):
        with self.connection:
            return self.cur.execute('''
                SELECT COUNT('user_id') as count
                FROM users;
            ''').fetchone()[0]

    def count_referals(self, user_id):
        with self.connection:
            return self.cur.execute('''
                SELECT COUNT('user_id') as count 
                FROM users 
                WHERE ref_id = ?;
            ''', (user_id,)).fetchone()[0]
        
    def get_referals(self, user_id):
        with self.connection:
            return self.cur.execute('''
                SELECT user_id
                FROM users 
                WHERE ref_id = ?;
            ''', (user_id,)).fetchall()
        
    def get_referals_two(self, user_id):
        with self.connection:
            return self.cur.execute('''
                SELECT user_id
                FROM users
                WHERE ref_id = (SELECT user_id
                                FROM users
                                WHERE ref_id = ?);
            ''', (user_id)).fetchall()

    def get_top_users(self):
        with self.connection:
            return self.cur.execute('''
                SELECT ref_id, COUNT('user_id') AS cnt
                FROM users
                GROUP BY ref_id
                ORDER BY cnt DESC
                LIMIT 11
            ''').fetchall()
        
    def add_rang(self, user_id, rang):
        with self.connection:
            return self.cur.execute('''
                UPDATE users
                SET rang = ?
                WHERE user_id = ?;
            ''', (rang, user_id,))
        
    def get_rang_ref(self, user_id):
        with self.connection:
            return self.cur.execute('''
                SELECT SUM('rang') as sum
                FROM users 
                WHERE ref_id = ?;
            ''', (user_id,)).fetchone()[0]
        
    def get_top_rang_users(self):
        with self.connection:
            return self.cur.execute('''
                SELECT user_id, rang
                FROM users
                ORDER BY rang DESC
                LIMIT 10
            ''').fetchall()
        
    def get_pos_rang_user(self, user_id):
        with self.connection:
            return self.cur.execute('''
                SELECT COUNT(*) AS rank
                FROM users 
                WHERE rang >= (SELECT rang
                               FROM users
                               WHERE user_id=?);
            ''', (user_id,)).fetchone()[0]

    def del_table(self):
        with self.connection:
            return self.cur.execute('''
                DROP TABLE IF EXISTS users; 
            ''')
