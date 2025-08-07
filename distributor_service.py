#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Blueprint, Flask, jsonify, request
from flask_cors import CORS
import mysql.connector

distributor_bp = Blueprint("distributor", __name__)
CORS(distributor_bp)



# Reuse connection logic
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3308,
        user="root",
        password="",
        database="cozy_comfort_db"
    )





# In[2]:


@distributor_bp.route('/api/orders', methods=['GET'])
def get_distributor_orders():
    distributor_id = request.args.get('distributor_id')

    if not distributor_id:
        return jsonify({"error": "Missing distributor_id"}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT id, customer_name, subtotal, created_at
            FROM orders
            WHERE distributor_id = %s
            ORDER BY created_at DESC
            LIMIT 10
        """
        cursor.execute(query, (distributor_id,))
        rows = cursor.fetchall()

        orders = []
        for row in rows:
            orders.append({
                "id": row['id'],
                "customer_name": row['customer_name'],
                "subtotal": row['subtotal'],
                "created_at": row['created_at'].strftime('%B %d, %Y') if row['created_at'] else None
            })

        cursor.close()
        conn.close()

        return jsonify({"orders": orders}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Failed to fetch orders"}), 500


# In[ ]:


if __name__ == '__main__':
    app.run(port=5004)

