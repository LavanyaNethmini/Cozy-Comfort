#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Blueprint, Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import mysql.connector

manufacture_bp = Blueprint("manufacture", __name__)
CORS(manufacture_bp)


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


@manufacture_bp.route('/api/blankets/all', methods=['GET'])
def get_all_blankets():
    try:
        conn = get_connection()  # Make sure this function exists
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT id, name, color, size, stock, material, price, image FROM blanket")
        blankets = cursor.fetchall()

        for blanket in blankets:
            # ✅ Extract the filename from the full path
            if blanket['image']:
                filename = os.path.basename(blanket['image'])  # "soft blanket.jpeg"
                blanket['image'] = f'http://localhost:5003/images/{filename}'     # "/images/soft blanket.jpeg"
        
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


# In[3]:


from flask import send_from_directory

@manufacture_bp.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('C:/wamp64/www/cozy-comfort/images', filename)


# In[4]:


@manufacture_bp.route('/inventory-summary', methods=['GET'])
def inventory_summary():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Total blanket types
    cursor.execute("SELECT COUNT(*) as total_types FROM blanket")
    total_types = cursor.fetchone()['total_types']

    # Total inventory (sum of stock)
    cursor.execute("SELECT SUM(stock) as total_inventory FROM blanket")
    total_inventory = cursor.fetchone()['total_inventory']

    # Low stock items (< 20)
    cursor.execute("SELECT COUNT(*) as low_stock FROM blanket WHERE stock < 20")
    low_stock = cursor.fetchone()['low_stock']

    # (Optional) Best seller (static for now)
    best_seller = "Premium Wool"

    cursor.close()
    conn.close()

    return jsonify({
        "total_types": total_types,
        "total_inventory": total_inventory,
        "low_stock": low_stock,
        "best_seller": best_seller
    })


# In[5]:


UPLOAD_FOLDER = os.path.join(os.getcwd(), 'images')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@manufacture_bp.route('/api/blankets/add', methods=['POST'])
def add_blanket():
    try:
        name = request.form['name']
        material = request.form['material']
        color = request.form['color']
        size = request.form['size']
        stock = int(request.form['stock'])
        price = float(request.form['price'])
        image_file = request.files.get('image')
        

        image_path = None
        if image_file:
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            image_file.save(image_path)

        conn = get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO blanket (name, material, color, size, stock, price, image)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, material, color, size, stock, price, image_path))
        conn.commit()

        return jsonify({
            'success': True,
            'message': 'Blanket added successfully'
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


# In[6]:


@manufacture_bp.route('/api/blankets/delete/<int:blanket_id>', methods=['DELETE'])
def delete_blanket(blanket_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Optionally, get and delete image from disk if needed

        query = "DELETE FROM blanket WHERE id = %s"
        cursor.execute(query, (blanket_id,))
        conn.commit()

        return jsonify({
            'success': True,
            'message': f'Blanket with ID {blanket_id} deleted successfully'
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


# In[7]:


# Get single blanket
@manufacture_bp.route('/api/blankets/<int:id>', methods=['GET'])
def get_blanket(id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM blanket WHERE id = %s", (id,))
        blanket = cursor.fetchone()
        
        if blanket:
            if blanket['image']:
                filename = os.path.basename(blanket['image'])
                blanket['image'] = f'http://localhost:5003/images/{filename}'
            
            return jsonify({
                'success': True,
                'data': blanket
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Blanket not found'
            }), 404
            
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

# Update blanket
@manufacture_bp.route('/api/blankets/<int:id>', methods=['PUT'])
def update_blanket(id):
    try:
        data = request.get_json()
        
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
            UPDATE blanket 
            SET name = %s, material = %s, size = %s, color = %s, price = %s, stock = %s
            WHERE id = %s
        """
        cursor.execute(query, (
            data['name'],
            data['material'],
            data['size'],
            data['color'],
            data['price'],
            data['stock'],
            id
        ))
        conn.commit()
        
        return jsonify({
            'success': True,
            'message': 'Blanket updated successfully'
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


@manufacture_bp.route('/api/update-stock/<int:blanket_id>', methods=['PUT'])
def update_stock(blanket_id):
    data = request.get_json()
    new_stock = data.get('stock')

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = "UPDATE blanket SET stock = %s WHERE id = %s"
        cursor.execute(query, (new_stock, blanket_id))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"message": "Stock updated successfully"}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Failed to update stock"}), 500


# In[ ]:


if __name__ == '__main__':
    app.run(port=5003)


# In[ ]:




