#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
import mysql.connector

notification_bp = Blueprint("notification", __name__)
CORS(notification_bp)

app = Flask(__name__)
CORS(app)
app.register_blueprint(notification_bp)


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


# In[2]:


@notification_bp.route('/notifications', methods=['POST'])
def create_notification():
    data = request.get_json()
    title = data.get('title')
    message = data.get('message')
    distributor_id = data.get('distributor_id')
    seller_name = data.get('seller_name')
    subtotal = data.get('subtotal')
    placed_on = data.get('placed_on')

    if not title or not message or not distributor_id:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO notifications (title, message, distributor_id, seller_name, subtotal, placed_on)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (title, message, distributor_id, seller_name, subtotal, placed_on))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Notification created'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500



# In[3]:


@notification_bp.route('/notifications', methods=['GET'])
def get_all_notifications():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, title, message, distributor_id, is_read, created_at
            FROM notifications
            ORDER BY created_at DESC
        """)
        notifications = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(notifications), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# In[4]:


@notification_bp.route('/notifications/<int:distributor_id>', methods=['GET'])
def get_notifications(distributor_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, title, message, is_read, created_at
            FROM notifications
            WHERE distributor_id = %s
            ORDER BY created_at DESC
        """, (distributor_id,))
        notifications = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(notifications), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# In[5]:


@notification_bp.route('/notifications/<int:notification_id>/read', methods=['PUT'])
def mark_notification_as_read(notification_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE notifications
            SET is_read = TRUE
            WHERE id = %s
        """, (notification_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Notification marked as read'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# In[ ]:


if __name__ == '__main__':
    app.run(port=5006)

