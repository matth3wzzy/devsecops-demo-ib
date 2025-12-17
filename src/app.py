"""
Демонстрационный файл с уязвимостями для тестирования SAST-инструментов
Проект для олимпиады по информационной безопасности
"""

import os
import sqlite3
import pickle
import subprocess

# ==================== УЯЗВИМОСТЬ 1: SQL-инъекция ====================
def get_user_data_unsafe(user_id):
    """
    НЕБЕЗОПАСНО: SQL-инъекция через конкатенацию строк
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # ⚠️ КРИТИЧЕСКАЯ УЯЗВИМОСТЬ: прямое включение пользовательского ввода в SQL
    query = "SELECT * FROM users WHERE id = " + user_id
    cursor.execute(query)
    return cursor.fetchall()

def get_user_data_unsafe_v2(username):
    """
    НЕБЕЗОПАСНО: SQL-инъекция через f-строку
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # ⚠️ ТАКЖЕ УЯЗВИМО: f-строки не защищают от SQLi
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchall()

# ==================== УЯЗВИМОСТЬ 2: Command Injection ====================
def list_files_unsafe(directory):
    """
    НЕБЕЗОПАСНО: Command Injection через os.system
    """
    # ⚠️ КРИТИЧЕСКАЯ УЯЗВИМОСТЬ: выполнение пользовательского ввода
    command = f"ls -la {directory}"
    os.system(command)  # Опасность!

def run_command_unsafe(cmd):
    """
    НЕБЕЗОПАСНО: Command Injection через subprocess
    """
    # ⚠️ ТАКЖЕ УЯЗВИМО: shell=True с пользовательским вводом
    subprocess.run(cmd, shell=True)

# ==================== УЯЗВИМОСТЬ 3: Hardcoded Secrets ====================
def connect_to_database():
    """
    НЕБЕЗОПАСНО: Секреты в коде
    """
    # ⚠️ УЯЗВИМОСТЬ: пароли не должны быть в коде
    db_password = "SuperSecretPassword123!"
    api_key = "sk_live_1234567890abcdef"
    secret_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    
    return f"Connected with password: {db_password}"

# ==================== УЯЗВИМОСТЬ 4: Небезопасная десериализация ====================
def load_user_data(data):
    """
    НЕБЕЗОПАСНО: Десериализация ненадежных данных
    """
    # ⚠️ УЯЗВИМОСТЬ: pickle может выполнить произвольный код
    return pickle.loads(data)

# ==================== УЯЗВИМОСТЬ 5: XSS (для демонстрации) ====================
def generate_html_unsafe(username):
    """
    НЕБЕЗОПАСНО: Потенциальный XSS
    """
    # ⚠️ УЯЗВИМОСТЬ: пользовательский ввод без экранирования
    html = f"<div>Welcome, {username}!</div>"
    return html

# ==================== УЯЗВИМОСТЬ 6: Weak Cryptography ====================
def weak_encryption(password):
    """
    НЕБЕЗОПАСНО: Слабое шифрование
    """
    # ⚠️ УЯЗВИМОСТЬ: XOR - очень слабый алгоритм
    key = 0x42
    encrypted = ''.join(chr(ord(c) ^ key) for c in password)
    return encrypted

# ==================== БЕЗОПАСНЫЕ АНАЛОГИ (для сравнения) ====================
def get_user_data_safe(user_id):
    """
    БЕЗОПАСНО: Параметризованные запросы
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # ✅ БЕЗОПАСНО: параметризованный запрос
    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))
    return cursor.fetchall()

def list_files_safe(directory):
    """
    БЕЗОПАСНО: Без использования shell
    """
    # ✅ БЕЗОПАСНО: использование os.listdir вместо os.system
    return os.listdir(directory)

# ==================== ТЕСТОВЫЙ КОД ====================
if __name__ == "__main__":
    print("=" * 60)
    print("ДЕМОНСТРАЦИОННЫЙ ФАЙЛ ДЛЯ SAST-ПРОВЕРКИ")
    print("Содержит намеренные уязвимости для тестирования:")
    print("1. SQL Injection")
    print("2. Command Injection") 
    print("3. Hardcoded Secrets")
    print("4. Insecure Deserialization")
    print("5. Potential XSS")
    print("6. Weak Cryptography")
    print("=" * 60)
    
    # Пример вызова уязвимых функций (закомментировано для безопасности)
    # user_data = get_user_data_unsafe("1 OR 1=1")
    # list_files_unsafe("/tmp; cat /etc/passwd")
    
    print("\n✅ Файл готов для тестирования Bandit и Semgrep!")
