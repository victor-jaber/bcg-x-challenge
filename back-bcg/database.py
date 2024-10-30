import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def init_db():
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_message(role, content):
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO messages (role, content) VALUES (?, ?)', (role, content))
    conn.commit()
    conn.close()

def get_messages():
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT role, content FROM messages ORDER BY timestamp')
    messages = cursor.fetchall()
    conn.close()
    print(f"Messages retrieved from database: {messages}") 
    return messages

def get_messages_dict():
    try:
        conn = sqlite3.connect('chatbot.db')
        cursor = conn.cursor()

        cursor.execute('SELECT role, content FROM messages ORDER BY timestamp')
        
        messages = [{'role': row[0], 'content': row[1]} for row in cursor.fetchall()]
        print(f"Messages retrieved from database: {messages}") 
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        messages = []
    finally:
        conn.close()
    
    return messages

def register_user(name, email, password):
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    hashed_password = generate_password_hash(password)
    try:
        cursor.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  
    finally:
        conn.close()

def verify_user(email, password):
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    if user and check_password_hash(user[0], password):
        return True
    return False