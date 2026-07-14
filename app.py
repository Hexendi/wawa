import sqlite3
import os
from flask import Flask, request, render_template, session, redirect, jsonify, make_response

app = Flask(__name__)
app.secret_key = 'w4w4sh0p_sup3r_s3cr3t_k3y_2026'
app.config['SESSION_COOKIE_HTTPONLY'] = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'shop.db')
FILES_DIR = os.path.join(BASE_DIR, 'files')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS flags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            flag TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL,
            image TEXT
        );
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            role TEXT NOT NULL,
            email TEXT,
            bio TEXT,
            flag TEXT
        );
        INSERT OR IGNORE INTO users (id, username, password) VALUES (1, 'admin', 'admin123');
        INSERT OR IGNORE INTO users (id, username, password) VALUES (2, 'staff', 'staff456');
        INSERT OR IGNORE INTO flags (id, flag) VALUES (1, '0xmr{sql_1nj3ct10n_br34ch_p0int}');
        INSERT OR IGNORE INTO products (id, name, description, price, image) VALUES (1, 'Wireless Headphones', 'Premium noise-canceling wireless headphones with 30h battery life', 89.99, 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop');
        INSERT OR IGNORE INTO products (id, name, description, price, image) VALUES (2, 'Smart Watch', 'Fitness tracker with heart rate monitor and GPS', 149.99, 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop');
        INSERT OR IGNORE INTO products (id, name, description, price, image) VALUES (3, 'USB-C Hub', '7-in-1 USB-C hub with HDMI 4K output', 34.99, 'https://images.unsplash.com/photo-1619953942547-233eab5a70d6?w=400&h=400&fit=crop');
        INSERT OR IGNORE INTO products (id, name, description, price, image) VALUES (4, 'Mechanical Keyboard', 'RGB backlit mechanical keyboard with blue switches', 79.99, 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400&h=400&fit=crop');
        INSERT OR IGNORE INTO products (id, name, description, price, image) VALUES (5, 'Bluetooth Speaker', 'Portable waterproof speaker with deep bass', 59.99, 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400&h=400&fit=crop');
        INSERT OR IGNORE INTO products (id, name, description, price, image) VALUES (6, 'Laptop Stand', 'Ergonomic aluminum laptop stand adjustable height', 29.99, 'https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=400&h=400&fit=crop');
        INSERT OR IGNORE INTO products (id, name, description, price, image) VALUES (7, 'Webcam HD', '1080p HD webcam with built-in microphone and privacy cover', 44.99, 'https://images.unsplash.com/photo-1587826081318-eadf5f7d3c7d?w=400&h=400&fit=crop');
        INSERT OR IGNORE INTO products (id, name, description, price, image) VALUES (8, 'Gaming Mouse', 'RGB gaming mouse with 16000 DPI sensor', 54.99, 'https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=400&h=400&fit=crop');
        INSERT OR IGNORE INTO profiles (id, username, role, email, bio, flag) VALUES (1, 'admin', 'administrator', 'admin@wawashop.com', 'Platform administrator', '0xmr{1d0r_4dm1n_pr1v_3scal8}');
        INSERT OR IGNORE INTO profiles (id, username, role, email, bio, flag) VALUES (123, 'alice', 'user', 'alice@example.com', 'Regular customer', NULL);
        INSERT OR IGNORE INTO profiles (id, username, role, email, bio, flag) VALUES (456, 'bob', 'user', 'bob@example.com', 'Premium member', NULL);
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = get_db()
    products = conn.execute('SELECT * FROM products ORDER BY price DESC').fetchall()
    featured = products[:4]
    conn.close()
    return render_template('index.html', featured=featured, products=products)

@app.route('/shop')
def shop():
    conn = get_db()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('shop.html', products=products)

@app.route('/product/<int:pid>')
def product_detail(pid):
    conn = get_db()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (pid,)).fetchone()
    conn.close()
    if not product:
        return redirect('/shop')
    return render_template('product.html', product=product)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'GET':
        return render_template('admin.html')

    username = request.form.get('username', '')
    password = request.form.get('password', '')

    conn = get_db()
    try:
        query = f"SELECT id, username, password FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor = conn.execute(query)
        user = cursor.fetchone()
    except Exception as e:
        conn.close()
        return render_template('admin.html', error=f'Database error: {str(e)}')

    conn.close()

    if user:
        session['logged_in'] = True
        session['username'] = user['username']
        session['user_id'] = user['id']
        return redirect('/dashboard', 303)

    return render_template('admin.html', error='Invalid username or password')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect('/admin')

    conn = get_db()
    product_count = conn.execute('SELECT COUNT(*) FROM products').fetchone()[0]
    user_count = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    conn.close()

    username = session.get('username', '')
    flag = None

    if '0xmr{' in str(username):
        flag = username

    return render_template('dashboard.html',
        username=username,
        product_count=product_count,
        user_count=user_count,
        revenue=12500,
        flag=flag
    )

@app.route('/search')
def search():
    query = request.args.get('q', '')
    resp = make_response()

    conn = get_db()
    if query:
        like_pattern = f'%{query}%'
        results = conn.execute(
            'SELECT * FROM products WHERE name LIKE ? OR description LIKE ?',
            (like_pattern, like_pattern)
        ).fetchall()
    else:
        results = []
    conn.close()

    if '0xmr{' not in str(query):
        resp.set_cookie('flag', '0xmr{xss_c00k13_th3ft_ftw}')

    html = render_template('search.html', query=query, results=results)
    resp.data = html
    return resp

@app.route('/api/files')
def api_files():
    file_id = request.args.get('id', '')
    if not file_id:
        return jsonify({'error': 'Missing id parameter'}), 400

    requested_path = os.path.join(FILES_DIR, file_id)
    requested_path = os.path.normpath(requested_path)

    try:
        with open(requested_path, 'r') as f:
            content = f.read()
        return content, 200, {'Content-Type': 'text/plain'}
    except FileNotFoundError:
        return jsonify({'error': f'File not found: {file_id}'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user/PROFILE')
def api_user_profile():
    user_id = request.args.get('id', '')
    if not user_id:
        return jsonify({'error': 'Missing id parameter'}), 400

    conn = get_db()
    try:
        profile = conn.execute('SELECT * FROM profiles WHERE id = ?', (user_id,)).fetchone()
        conn.close()
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

    if profile:
        return jsonify({
            'id': profile['id'],
            'username': profile['username'],
            'role': profile['role'],
            'email': profile['email'],
            'bio': profile['bio'],
            'flag': profile['flag']
        })

    return jsonify({'error': 'User not found'}), 404

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
