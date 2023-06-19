import sqlite3

class BotDB:

    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def user_exist(self, user_id):
        result = self.cursor.execute("SELECT `user_id` FROM `users` WHERE `user_id`= ?", (user_id,))
        return bool(len(result.fetchall()))

    def user_add(self, user_id, user_first_name):
        self.cursor.execute("INSERT INTO `users` (`user_id`, `user_first_name`) VALUES (?, ?)", (user_id, user_first_name,))
        return self.connection.commit()

    def get_user(self, user_id):
        result = self.cursor.execute("SELECT `user_id`, `user_first_name` FROM `users` WHERE `user_id`= ?", (user_id,))
        return result.fetchone()

    def close(self):
        self.connection.close()
