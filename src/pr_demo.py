# Демо для PR
import os
def unsafe_login(username, password):
    query = f"SELECT * FROM users WHERE username=\"\"{username}\"\" AND password=\"\"{password}\"\""
    return query
def debug_info(debug):
    if debug:
        os.system("echo test")

