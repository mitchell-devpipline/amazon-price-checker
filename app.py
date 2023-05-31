import psycopg2
from flask import Flask, jsonify, request

conn = psycopg2.connect("dbname='amazon' host='localhost'")
cursor = conn.cursor()
app = Flask(__name__)


def create_all():
    print("Creating all tables...")
    cursor.execute("""
   CREATE TABLE IF NOT EXISTS Categories(
    category_id SERIAL PRIMARY KEY,
    name VARCHAR,
    parent_category_id int,
    amazon_url VARCHAR
 );
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS Products (
    product_id UUID4 PRIMARY KEY
    category_id int,
    upc VARCHAR UNIQUE,
    name VARCHAR,
    description VARCHAR,
    amazon_url VARCHAR UNIQUE,
    amazon_id VARCHAR UNIQUE
    FOREIGN KEY(category_id) REFERENCES Categories(category_id)
);
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS ProductsCategoriesXref (
    category_id int
    product_id int,
    FOREIGN KEY(category_id) REFERENCES Categories(category_id),
    FOREIGN KEY(product_id) REFERENCES Products(product_id)
    PRIMARY KEY(category_id, product_id)
);
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Pricing(
        product_id int,
        date timestamp,
        price float
        FOREIGN KEY(product_id) REFERENCES Products(product_id)
       PRIMARY KEY(product_id, date)
    );
 """)

cursor.execute("""
    CREATE TYPE discounttype as ENUM('amount', 'percent');
    CREATE TYPE coupontype as ENUM('clickable', 'fillable');
 
    CREATE TABLE IF NOT EXISTS Coupons(
        product_id int,
        coupon_id varchar,
        coupon_discount float,
        date timestamp,
        coupon_expiration date,
        discount_type discounttype,
        description varchar,
        type coupontype
        FOREIGN KEY(product_id) REFERENCES Products(product_id)
        PRIMARY KEY(product_id, coupon_id)
    );
""")

conn.commit()
print("All Tables Created")

create_all()
