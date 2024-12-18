import sqlite3

connection = sqlite3.connect("not_telegram.db")
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS Users")

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')

cursor.execute("CREATE INDEX IF NOT EXISTS idx_username ON Users (username)")

for i in range(10):
    cursor.execute('INSERT INTO Users('
                   'username,'
                   'email,'
                   'age,'
                   'balance)'
                   ' VALUES(?,?,?,?)',
                   (
                       f'User{i + 1}',
                       f'example{i + 1}@gmail.com',
                       (i + 1) * 10,
                       1000
                   )
                   )

cursor.execute("SELECT COUNT(*) FROM Users")

for i in range(1, 11, 2):
    cursor.execute("UPDATE Users  SET balance=? WHERE username=?",
                   (500, f'User{i}'))

for i in range(1, 11, 3):
    cursor.execute('DELETE FROM Users WHERE username=?',
                   (f'User{i}',))

cursor.execute('SELECT * FROM Users WHERE age!=? ', (60,))

result = cursor.fetchall()

for user in result:
    print(f'{user[1]}'
          f' | Почта: {user[2]}'
          f' | Возраст: {user[3]}'
          f' | Баланс: {user[4]}'
          )
cursor.execute("DELETE FROM Users WHERE id=?", (6,))
cursor.execute("SELECT COUNT(*) FROM Users")
total_users = cursor.fetchone()[0]

cursor.execute("SELECT SUM(balance) FROM Users")
total_balance = cursor.fetchone()[0]
print(total_balance / total_users)
connection.commit()

connection.close()
