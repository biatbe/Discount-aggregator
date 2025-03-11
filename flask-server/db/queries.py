from .connection import get_db_connection
from datetime import datetime

def store_products(product):
    conn = get_db_connection()
    cur = conn.cursor()
    today = datetime.today().strftime('%Y-%m-%d')
    for data in product:
        brand = data["brand"]
        sectionName = data["sectionName"]
        name = data["name"]
        oldPrice = data["oldPrice"]
        price = data["price"]
        displayDiscountPercentage = data["displayDiscountPercentage"]
        url = data["url"]
        href = data["href"]
        cur.execute('''
            INSERT INTO products (brand, section_name, name, old_price, price, display_discount_percentage, url, href, last_updated)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (brand, section_name, name, old_price, price) DO NOTHING
        ''', (brand, sectionName, name, oldPrice, price, displayDiscountPercentage, url, href, today))

    conn.commit()
    cur.close()
    conn.close()

def clear_products():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''TRUNCATE TABLE products RESTART IDENTITY;''')
    conn.commit()
    cur.close()
    conn.close()


def get_all_products():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM products;')
    products = cur.fetchall()
    cur.close()
    conn.close()

    return products