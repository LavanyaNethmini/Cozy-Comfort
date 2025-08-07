#!/usr/bin/env python
# coding: utf-8

# In[1]:




# In[2]:


from flask import Blueprint, Flask, request, jsonify
from flask_cors import CORS  # Add this import
import mysql.connector
import jwt
import datetime


auth_bp = Blueprint("auth", __name__)
CORS(auth_bp)


# Database connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3308,
        user="root",
        password="",
        database="cozy_comfort_db"
    )

# Test connection
try:
    conn = get_connection()
    print("Connected to cozy_comfort_db successfully!")
    conn.close()
except Exception as e:
    print("Connection failed:", e)


# In[3]:


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)", 
                       (username, email, password, role))
        conn.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()
        conn.close()


# In[4]:


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT id, username, email, role FROM users WHERE email = %s AND password = %s",
            (email, password)
        )
        user = cursor.fetchone()

        if user:
            # Generate token
            token = jwt.encode({
                'user_id': user['id'],
                'role': user['role'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, 'your_secret_key', algorithm='HS256')

            # ✅ Return username & email so frontend can store them
            return jsonify({
                'message': 'Login successful',
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email'],
                    'role': user['role']
                },
                'token': token
            }), 200
        else:
            return jsonify({'message': 'Invalid email or password'}), 401

    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()
        conn.close()



# In[ ]:


if __name__ == '__main__':
    app.run(port=5000)


# In[ ]:




