#!/usr/bin/env python
# coding: utf-8

# In[1]:


import nest_asyncio
nest_asyncio.apply()

from flask import Blueprint, Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from datetime import datetime
import requests
import mysql.connector
import os

seller_bp = Blueprint("seller", __name__)
CORS(seller_bp)




def get_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3308,
        user="root",
        password="",
        database="cozy_comfort_db"
    )

@seller_bp.route('/blankets', methods=['GET'])
def get_blankets():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM blanket")
        blankets = cursor.fetchall()
        for blanket in blankets:
            if blanket['image']:
                blanket['image'] = blanket['image'].replace('C:\\wamp64\\www\\cozy-comfort\\images\\', '/images/')
        return jsonify(blankets)
    finally:
        cursor.close()
        connection.close()


# In[2]:


import os

@seller_bp.route('/api/blankets/top-stock', methods=['GET'])
def get_top_stock_blankets():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT name, color, stock, price, image
            FROM blanket
            ORDER BY stock DESC
            LIMIT 3
        """)
        blankets = cursor.fetchall()

        for blanket in blankets:
            # ✅ Extract the filename from the full path
            if blanket['image']:
                filename = os.path.basename(blanket['image'])  # "soft blanket.jpeg"
                blanket['image'] = f'http://localhost:5002/images/{filename}'     # "/images/soft blanket.jpeg"

            # Handle price
            try:
                blanket['price'] = float(blanket['price']) if blanket['price'] is not None else 0.0
            except Exception as e:
                print("Error converting price:", e)
                blanket['price'] = 0.0

        return jsonify(blankets)

    except Exception as e:
        print("API Error:", e)
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()



# In[3]:


from flask import send_from_directory

@seller_bp.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('C:/wamp64/www/cozy-comfort/images', filename)



# In[4]:


@seller_bp.route('/api/seller/<int:seller_id>', methods=['GET'])
def get_seller_profile(seller_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT id, username AS name, email, created_at 
            FROM users 
            WHERE id = %s AND role = 'Seller'
        """, (seller_id,))
        
        seller = cursor.fetchone()
        if seller:
            return jsonify(seller)
        return jsonify({'error': 'Seller not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


# In[5]:


@seller_bp.route('/api/orders', methods=['POST'])
def create_order():
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO orders 
            (seller_id, customer_name, customer_email, customer_phone, customer_address, priority, instructions, subtotal, total, distributor_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data['seller_id'], data['customer_name'], data['customer_email'], data['customer_phone'],
            data['customer_address'], data['priority'], data['instructions'],
            data['subtotal'], data['total'],  data['distributor_id']
        ))
        order_id = cursor.lastrowid

        for item in data['items']:
            cursor.execute("""
                INSERT INTO order_items (order_id, id, quantity, price, subtotal)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                order_id, item['id'], item['quantity'], item['price'], item['subtotal']
            ))

        conn.commit()
        return jsonify({'message': 'Order placed successfully', 'order_id': order_id})

    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()


# In[6]:


@seller_bp.route("/api/orders", methods=["POST"])
def place_order():
    data = request.get_json()

    customer_name = data["customer_name"]
    customer_contact = data["customer_contact"]
    customer_address = data["customer_address"]
    seller_id = data["seller_id"]
    items = data["items"]
    subtotal = data.get("subtotal", 0)

    # Get seller_name from DB
    seller = Seller.query.filter_by(id=seller_id).first()
    seller_name = seller.username if seller else f"Seller {seller_id}"

    # Get distributor_id from first blanket
    first_blanket_id = items[0]["id"]
    blanket = Blanket.query.filter_by(id=first_blanket_id).first()
    if not blanket:
        return jsonify({"error": "Invalid blanket ID"}), 400
    distributor_id = blanket.distributor_id

    # Save order
    order = Order(
        customer_name=customer_name,
        customer_contact=customer_contact,
        customer_address=customer_address,
        seller_id=seller_id,
        distributor_id=distributor_id,
        order_status="Pending"
    )
    db.session.add(order)
    db.session.commit()

    # Save items
    for item in items:
        order_item = OrderItem(
            order_id=order.id,
            blanket_id=item["id"],
            quantity=item["quantity"],
            price=item["price"]
        )
        db.session.add(order_item)
    db.session.commit()

    # ✅ Create notification payload with new columns
    notification_payload = {
        "title": "New Order Received",
        "message": f"{seller_name} placed a new order of Rs.{subtotal:.2f}",
        "distributor_id": distributor_id,
        "seller_name": seller_name,
        "subtotal": subtotal,
        "placed_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        response = requests.post("http://localhost:5004/notifications", json=notification_payload)
        if response.status_code == 201:
            print("Notification sent.")
        else:
            print("Notification failed:", response.text)
    except Exception as e:
        print("Notification error:", str(e))

    return jsonify({"message": "Order placed", "order_id": order.id}), 201




# In[7]:


@seller_bp.route('/api/blankets/all', methods=['GET'])
def get_all_blankets():
    try:
        conn = get_connection()  # Make sure this function exists
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT id, name, color, size, stock, price, image FROM blanket")
        blankets = cursor.fetchall()

        for blanket in blankets:
            # ✅ Extract the filename from the full path
            if blanket['image']:
                filename = os.path.basename(blanket['image'])  # "soft blanket.jpeg"
                blanket['image'] = f'http://localhost:5002/images/{filename}'     # "/images/soft blanket.jpeg"
        
        return jsonify({
            'success': True,
            'data': blankets
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
        
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


# In[8]:


@seller_bp.route('/api/distributors', methods=['GET'])
def get_distributors():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)  # Create cursor
        
        # Execute query THROUGH THE CURSOR
        cursor.execute('''
            SELECT id, username, email
            FROM users 
            WHERE role = 'Distributor'
        ''')
        
        # Fetch results
        distributors = cursor.fetchall()
        
        # Close both cursor and connection
        cursor.close()
        conn.close()
        
        # No need to convert to dict - cursor(dictionary=True) already does this
        return jsonify(distributors)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# In[ ]:


if __name__ == '__main__':
    app.run(port=5002)

