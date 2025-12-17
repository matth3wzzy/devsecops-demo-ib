"""
COMPREHENSIVE VULNERABILITY DEMO FILE
Для тестирования SAST инструментов (Bandit, Semgrep)
Содержит 10 типов уязвимостей безопасности
"""

import os
import sqlite3
import pickle
import subprocess
import json
import yaml
import hashlib
import base64
from flask import Flask, request
import xml.etree.ElementTree as ET

app = Flask(__name__)

# ==================== 1. SQL INJECTION ====================
@app.route('/login', methods=['POST'])
def login():
    """Уязвимость: SQL Injection в веб-приложении"""
    username = request.form['username']
    password = request.form['password']
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # КРИТИЧЕСКАЯ УЯЗВИМОСТЬ 1.1: Конкатенация строк
    query1 = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query1)
    
    # КРИТИЧЕСКАЯ УЯЗВИМОСТЬ 1.2: Еще один вариант
    query2 = "SELECT * FROM users WHERE id = " + request.args.get('id', '')
    cursor.execute(query2)
    
    return "Login processed"

# ==================== 2. COMMAND INJECTION ====================
def execute_backup():
    """Уязвимость: Command Injection"""
    backup_dir = request.args.get('dir', '/tmp')
    
    # КРИТИЧЕСКАЯ УЯЗВИМОСТЬ 2.1: os.system с пользовательским вводом
    os.system(f"tar -czf backup.tar.gz {backup_dir}")
    
    # КРИТИЧЕСКАЯ УЯЗВИМОСТЬ 2.2: subprocess с shell=True
    subprocess.run(f"ls -la {backup_dir}", shell=True)
    
    return "Backup completed"

# ==================== 3. HARDCODED SECRETS ====================
class DatabaseConfig:
    """Уязвимость: Секреты в коде"""
    # КРИТИЧЕСКАЯ УЯЗВИМОСТЬ 3.1: Пароли в коде
    DB_PASSWORD = "SuperSecretDBPassword123!"
    
    # КРИТИЧЕСКАЯ УЯЗВИМОСТЬ 3.2: API ключи
    AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
    AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    
    # КРИТИЧЕСКАЯ УЯЗВИМОСТЬ 3.3: JWT секреты
    JWT_SECRET = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"

# ==================== 4. INSECURE DESERIALIZATION ====================
def load_user_session(session_data):
    """Уязвимость: Небезопасная десериализация"""
    # КРИТИЧЕСКАЯ УЯЗВИМОСТЬ 4.1: pickle.loads
    user_data = pickle.loads(base64.b64decode(session_data))
    
    # КРИТИЧЕСКАЯ УЯЗВИМОСТЬ 4.2: yaml.load
    config = yaml.load(request.data, Loader=yaml.Loader)
    
    return user_data

# ==================== 5. XXE (XML External Entity) ====================
def parse_xml_data(xml_string):
    """Уязвимость: XXE Attack"""
    # КРИТИЧЕСКАЯ УЯЗВИМОСТЬ: Парсинг XML без защиты
    root = ET.fromstring(xml_string)
    return root.tag

# ==================== 6. WEAK CRYPTOGRAPHY ====================
def hash_password(password):
    """Уязвимость: Слабая криптография"""
    # УЯЗВИМОСТЬ 6.1: MD5 - устаревший и небезопасный
    md5_hash = hashlib.md5(password.encode()).hexdigest()
    
    # УЯЗВИМОСТЬ 6.2: SHA1 - также небезопасен
    sha1_hash = hashlib.sha1(password.encode()).hexdigest()
    
    # УЯЗВИМОСТЬ 6.3: Слабый собственный алгоритм
    weak_hash = ''.join(chr(ord(c) ^ 0x42) for c in password)
    
    return md5_hash

# ==================== 7. PATH TRAVERSAL ====================
def read_user_file(filename):
    """Уязвимость: Path Traversal"""
    # КРИТИЧЕСКАЯ УЯЗВИМОСТЬ: Открытие файлов без проверки пути
    with open(f"uploads/{filename}", "r") as f:
        return f.read()

# ==================== 8. INSECURE RANDOMNESS ====================
def generate_token():
    """Уязвимость: Небезопасная генерация случайных чисел"""
    import random
    # УЯЗВИМОСТЬ: random для security-critical операций
    token = random.randint(100000, 999999)
    return str(token)

# ==================== 9. DEBUG CODE IN PRODUCTION ====================
def admin_panel():
    """Уязвимость: Отладочный код в продакшене"""
    # УЯЗВИМОСТЬ: Debug функции доступные в продакшене
    debug_mode = True  # Должно быть False в продакшене!
    
    if debug_mode:
        # Опасные debug операции
        os.system("whoami")
        print("DEBUG: Admin panel accessed")
        
    return "Admin panel"

# ==================== 10. INSECURE DIRECT OBJECT REFERENCE ====================
@app.route('/api/users/<user_id>')
def get_user_profile(user_id):
    """Уязвимость: Insecure Direct Object Reference (IDOR)"""
    # УЯЗВИМОСТЬ: Прямой доступ к объектам без проверки прав
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    
    return json.dumps(cursor.fetchone())

# ==================== SAFE ALTERNATIVES (для сравнения) ====================
def safe_login(username, password):
    """БЕЗОПАСНО: Параметризованные запросы"""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # БЕЗОПАСНО: Использование параметров
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    cursor.execute(query, (username, password))
    
    return cursor.fetchone()

def safe_hash_password(password):
    """БЕЗОПАСНО: Современное хеширование"""
    import bcrypt
    # БЕЗОПАСНО: bcrypt с солью
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed

# ==================== MAIN ====================
if __name__ == "__main__":
    print("=" * 70)
    print("COMPREHENSIVE VULNERABILITY DEMONSTRATION")
    print("=" * 70)
    print("\nТипы уязвимостей в этом файле:")
    print("1. SQL Injection (2 варианта)")
    print("2. Command Injection (2 варианта)")
    print("3. Hardcoded Secrets (пароли, API ключи, JWT)")
    print("4. Insecure Deserialization (pickle, yaml)")
    print("5. XXE (XML External Entity)")
    print("6. Weak Cryptography (MD5, SHA1, custom XOR)")
    print("7. Path Traversal")
    print("8. Insecure Randomness")
    print("9. Debug Code in Production")
    print("10. Insecure Direct Object Reference (IDOR)")
    print("\nТакже включены безопасные альтернативы для сравнения.")
    print("=" * 70)
    
    # ТЕСТ БЕЗОПАСНЫХ ФУНКЦИЙ
    print("\n✅ Безопасные функции доступны для тестирования:")
    print("   • safe_login(username, password)")
    print("   • safe_hash_password(password)")
    
    app.run(debug=False, host='127.0.0.1', port=5000)
