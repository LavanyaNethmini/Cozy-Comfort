#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Reuse connection logic
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3308,
        user="root",
        password="",
        database="cozy_comfort_db"
    )

@app.route('/users', methods=['GET'])
def get_all_users():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT id, username, email, role FROM users")
    users = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify(users)



# In[2]:


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        return jsonify({'message': f'User with ID {user_id} deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


# In[3]:


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, username, email, role FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404


# In[4]:


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    role = data.get('role')

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE users SET username = %s, email = %s, role = %s WHERE id = %s
        """, (username, email, role, user_id))
        conn.commit()
        return jsonify({'message': 'User updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


# In[5]:


@app.route('/users', methods=['POST'])
def create_user():
    from flask import request  # just in case it's not at top

    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')  # optional: you can omit for now or set default
    role = data.get('role')

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)",
                       (username, email, password or '', role))
        conn.commit()
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


# In[ ]:


if __name__ == '__main__':
    print("\nUser Service Running. Available routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule} -> {rule.endpoint}")
    app.run(port=5001)  #  Use different port from auth_service

