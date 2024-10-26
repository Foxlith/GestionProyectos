from flask import Flask, jsonify, request
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'productos.db'

# Crear la base de datos y tabla solo si no existe
def init_db():
    if not os.path.exists(DATABASE):  # Verifica si la base de datos no existe
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                precio REAL NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

# Inicializar la base de datos
init_db()

# Ruta para obtener todos los productos
@app.route('/productos', methods=['GET'])
def obtener_productos():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return jsonify(productos)

# Ruta para agregar un producto
@app.route('/productos', methods=['POST'])
def agregar_producto():
    nuevo_producto = request.get_json()
    nombre = nuevo_producto.get('nombre')
    precio = nuevo_producto.get('precio')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO productos (nombre, precio) VALUES (?, ?)", (nombre, precio))
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Producto agregado"}), 201

# Ejecuta la aplicación
if __name__ == '__main__':
    app.run(debug=True)