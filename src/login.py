# Демо файл для Pull Request - содержит уязвимость
import os

def unsafe_login(username, password):
    # Уязвимость: SQL injection в логине
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    return query

def debug_info(debug):
    # Уязвимость: Command injection в debug функции
    if debug:
        os.system("echo 'Debug mode enabled'")
