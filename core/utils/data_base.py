import sqlite3


class DataBase:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cur = self.connection.cursor()
        self.create_db()

    def create_db(self):
        try:
            query = ('CREATE TABLE IF NOT EXISTS users('
                     'user_id INTEGER PRIMARY KEY,'
                     'user_name TEXT,'
                     'referrer_id INTEGER);')
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
                 user_name,
                 refferer_id,):
        ''' Создаёт нового пользователя. '''
        with self.connection:
            return self.cur.execute('''
                INSERT INTO users ('user_id', 'user_name', ‘refferer_id’)
                VALUES (?, ?, ?);
            ''', (user_id, user_name, refferer_id))
    
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
                WHERE referrer_id = ?;
            ''', (user_id,)).fetchone()[0]
        
    def get_referals(self, user_id):
        with self.connection:
            return self.cur.execute('''
                SELECT user_id
                FROM users 
                WHERE referrer_id = ?;
            ''', (user_id,)).fetchall()

    def get_top_users(self):
        with self.connection:
            return self.cur.execute('''
                SELECT `referrer_id`, COUNT(*) AS `cnt`
                FROM `users`
                GROUP BY `referrer_id`
                ORDER BY `cnt` DESC
                LIMIT 11
            ''').fetchall()
