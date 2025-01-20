import time

import psycopg2
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# Database Configuration
DB_HOST = "localhost"
DB_PORT = "5432"
DB_USER = "postgres"
DB_PASSWORD = "1234"
DB_NAME = "art-marketplace-platform"
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ORM Models
class Category(Base):
    __tablename__ = 'category'
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    products = relationship("Product", back_populates="category")

class Seller(Base):
    __tablename__ = 'seller'
    seller_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    number = Column(Integer, nullable=False)
    products = relationship("Product", back_populates="seller")

class Product(Base):
    __tablename__ = 'product'
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    category_id = Column(Integer, ForeignKey('category.category_id'), nullable=False)
    seller_id = Column(Integer, ForeignKey('seller.seller_id'), nullable=False)
    category = relationship("Category", back_populates="products")
    seller = relationship("Seller", back_populates="products")

# Database Operations
class Model:
    def __init__(self):
        Base.metadata.create_all(engine)
        self.session = SessionLocal()

    def add_category(self, name):
        try:
            category = Category(name=name)
            self.session.add(category)
            self.session.commit()
        except Exception as e:
            print(f"Error adding category: {e}")
            self.session.rollback()

    def update_category(self, category_id, name):
        try:
            category = self.session.query(Category).filter_by(category_id=category_id).first()
            if category:
                category.name = name
                self.session.commit()
        except Exception as e:
            print(f"Error updating category: {e}")
            self.session.rollback()

    def delete_category(self, category_id):
        try:
            self.session.query(Category).filter_by(category_id=category_id).delete()
            self.session.commit()
        except Exception as e:
            print(f"Error deleting category: {e}")
            self.session.rollback()

    def get_all_categories(self):
        try:
            categories = self.session.query(Category).all()
            return [(c.category_id, c.name) for c in categories]
        except Exception as e:
            print(f"Error retrieving categories: {e}")
            return []

    def add_seller(self, name, number):
        try:
            seller = Seller(name=name, number=number)
            self.session.add(seller)
            self.session.commit()
        except Exception as e:
            print(f"Error adding seller: {e}")
            self.session.rollback()

    def update_seller(self, seller_id, name, number):
        try:
            seller = self.session.query(Seller).filter_by(seller_id=seller_id).first()
            if seller:
                seller.name = name
                seller.number = number
                self.session.commit()
        except Exception as e:
            print(f"Error updating seller: {e}")
            self.session.rollback()

    def delete_seller(self, seller_id):
        try:
            self.session.query(Seller).filter_by(seller_id=seller_id).delete()
            self.session.commit()
        except Exception as e:
            print(f"Error deleting seller: {e}")
            self.session.rollback()

    def get_all_sellers(self):
        try:
            sellers = self.session.query(Seller).all()
            return [(s.seller_id, s.name, s.number) for s in sellers]
        except Exception as e:
            print(f"Error retrieving sellers: {e}")
            return []

    def add_product(self, name, category_id, seller_id):
        try:
            product = Product(name=name, category_id=category_id, seller_id=seller_id)
            self.session.add(product)
            self.session.commit()
        except Exception as e:
            print(f"Error adding product: {e}")
            self.session.rollback()

    def update_product(self, product_id, name, category_id, seller_id):
        try:
            product = self.session.query(Product).filter_by(product_id=product_id).first()
            if product:
                product.name = name
                product.category_id = category_id
                product.seller_id = seller_id
                self.session.commit()
        except Exception as e:
            print(f"Error updating product: {e}")
            self.session.rollback()

    def delete_product(self, product_id):
        try:
            self.session.query(Product).filter_by(product_id=product_id).delete()
            self.session.commit()
        except Exception as e:
            print(f"Error deleting product: {e}")
            self.session.rollback()

    def get_all_products(self):
        try:
            products = self.session.query(Product).all()
            return [(p.product_id, p.name, p.category_id, p.seller_id) for p in products]
        except Exception as e:
            print(f"Error retrieving products: {e}")
            return []
    
    def generate_sample_data(self):
        try:
            with self.conn.cursor() as c:
                # Generate sample categories
                c.execute('''
                    INSERT INTO category (name)
                    SELECT 'Category ' || i
                    FROM generate_series(1, 10) AS i
                    ON CONFLICT DO NOTHING;
                ''')

                # Generate sample sellers
                c.execute('''
                    INSERT INTO seller (name, number)
                    SELECT 'Seller ' || i, (1000000000 + i)
                    FROM generate_series(1, 10) AS i
                    ON CONFLICT DO NOTHING;
                ''')

                # Generate sample products with valid foreign keys
                c.execute('''
                    INSERT INTO product (name, category_id, seller_id)
                    SELECT 'Product ' || i, 
                           (SELECT category_id FROM category ORDER BY RANDOM() LIMIT 1),
                           (SELECT seller_id FROM seller ORDER BY RANDOM() LIMIT 1)
                    FROM generate_series(1, 20) AS i
                    ON CONFLICT DO NOTHING;
                ''')

                self.conn.commit()
        except Exception as e:
            print(f"Error generating sample data: {e}")
    
    def query_top_categories(self, min_products):
        try:
            start_time = time.time()
            with self.conn.cursor() as c:
                c.execute('''
                    SELECT category.name, COUNT(product.product_id) AS product_count
                    FROM category
                    JOIN product ON category.category_id = product.category_id
                    GROUP BY category.name
                    HAVING COUNT(product.product_id) >= %s
                    ORDER BY product_count DESC;
                ''', (min_products,))
                results = c.fetchall()
            execution_time = (time.time() - start_time) * 1000
            return results, execution_time
        except Exception as e:
            print(f"Error executing query: {e}")
            return [], 0

    def query_seller_products(self, seller_id):
        try:
            start_time = time.time()
            with self.conn.cursor() as c:
                c.execute('''
                    SELECT seller.name, product.name
                    FROM seller
                    JOIN product ON seller.seller_id = product.seller_id
                    WHERE seller.seller_id = %s
                    ORDER BY product.name;
                ''', (seller_id,))
                results = c.fetchall()
            execution_time = (time.time() - start_time) * 1000
            return results, execution_time
        except Exception as e:
            print(f"Error executing query: {e}")
            return [], 0

    def query_category_seller_summary(self):
        try:
            start_time = time.time()
            with self.conn.cursor() as c:
                c.execute('''
                    SELECT category.name AS category_name, seller.name AS seller_name, COUNT(product.product_id) AS product_count
                    FROM category
                    JOIN product ON category.category_id = product.category_id
                    JOIN seller ON seller.seller_id = product.seller_id
                    GROUP BY category.name, seller.name
                    ORDER BY category_name, seller_name;
                ''')
                results = c.fetchall()
            execution_time = (time.time() - start_time) * 1000
            return results, execution_time
        except Exception as e:
            print(f"Error executing query: {e}")
            return [], 0
