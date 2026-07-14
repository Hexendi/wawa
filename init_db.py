import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shop.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript('''
        DROP TABLE IF EXISTS users;
        DROP TABLE IF EXISTS flags;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS profiles;

        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        );

        CREATE TABLE flags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            flag TEXT NOT NULL
        );

        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL,
            image TEXT
        );

        CREATE TABLE profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            role TEXT NOT NULL,
            email TEXT,
            bio TEXT,
            flag TEXT
        );

        INSERT INTO users (username, password) VALUES ('admin', 'admin123');
        INSERT INTO users (username, password) VALUES ('staff', 'staff456');

        INSERT INTO flags (flag) VALUES ('0xmr{sql_1nj3ct10n_br34ch_p0int}');

        INSERT INTO products (name, description, price, image) VALUES ('Wireless Headphones', 'Premium noise-canceling wireless headphones', 89.99, 'headphones.jpg');
        INSERT INTO products (name, description, price, image) VALUES ('Smart Watch', 'Fitness tracker with heart rate monitor', 149.99, 'watch.jpg');
        INSERT INTO products (name, description, price, image) VALUES ('USB-C Hub', '7-in-1 USB-C hub with HDMI', 34.99, 'hub.jpg');
        INSERT INTO products (name, description, price, image) VALUES ('Mechanical Keyboard', 'RGB backlit mechanical keyboard', 79.99, 'keyboard.jpg');
        INSERT INTO products (name, description, price, image) VALUES ('Bluetooth Speaker', 'Portable waterproof speaker', 59.99, 'speaker.jpg');
        INSERT INTO products (name, description, price, image) VALUES ('Laptop Stand', 'Ergonomic aluminum laptop stand', 29.99, 'stand.jpg');
        INSERT INTO products (name, description, price, image) VALUES ('Webcam HD', '1080p HD webcam with microphone', 44.99, 'webcam.jpg');
        INSERT INTO products (name, description, price, image) VALUES ('Mouse Pad XL', 'Large gaming mouse pad', 19.99, 'mousemat.jpg');

        INSERT INTO profiles (id, username, role, email, bio, flag) VALUES (1, 'admin', 'administrator', 'admin@wawashop.com', 'Platform administrator', '0xmr{1d0r_4dm1n_pr1v_3scal8}');
        INSERT INTO profiles (id, username, role, email, bio, flag) VALUES (123, 'alice', 'user', 'alice@example.com', 'Regular customer', NULL);
        INSERT INTO profiles (id, username, role, email, bio, flag) VALUES (456, 'bob', 'user', 'bob@example.com', 'Premium member', NULL);
    ''')

    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")

if __name__ == '__main__':
    init_db()
